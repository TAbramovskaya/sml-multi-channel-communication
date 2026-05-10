from extract_json_data import *
from extract_gmail_data import *
import auth
import os


def load(from_csv=False):
    names = {"messages", "intensives", "events", "mailbox"}
    result = {name: None for name in names}

    if not from_csv:
        intensives = build_dataframe_json("raw_data/intensives.json", "intensives")
        events = build_dataframe_json("raw_data/events.json", "events")
        mailbox = build_dataframe_gmail(auth.build_service(), "mailbox")

        messages = get_messages_from_sources(intensives, events, mailbox)

        result["intensives"] = intensives
        result["events"] = events
        result["mailbox"] = mailbox
        result["messages"] = messages

    else:
        if os.path.exists("csv/messages.csv"):
            keep_cols = ["id", "source_id", "source", "type", "date", "day", "content", "content_structured"]
            messages = pd.read_csv("csv/messages.csv")

            messages["date"] = (
                pd.to_datetime(
                    messages["date"], utc=True, errors="coerce"
                )
            )

            messages["day"] = (
                pd.to_datetime(messages["date"])
                .dt.floor("D")
            )

            messages = messages[[col for col in keep_cols if col in messages.columns]]

            result["messages"] = messages

        required_files = {"csv/intensives.csv", "csv/events.csv", "csv/mailbox.csv"}
        missing_files = [
            path for path in required_files
            if not os.path.exists(path)
        ]

        if not missing_files:
            intensives = pd.read_csv("csv/intensives.csv")
            intensives["date"] = (
                pd.to_datetime(
                    intensives["date"], utc=True, errors="coerce"
                )
            )
            result["intensives"] = intensives

            events = pd.read_csv("csv/events.csv")
            events["date"] = (
                pd.to_datetime(
                    events["date"], utc=True, errors="coerce")
            )
            result["events"] = events

            mailbox = pd.read_csv("csv/mailbox.csv")
            mailbox["date"] = (
                pd.to_datetime(
                    mailbox["date"], utc=True, errors="coerce")
            )
            result["mailbox"] = mailbox

        if result["messages"] is None:
            messages = get_messages_from_sources(intensives, events, mailbox)

            result["messages"] = messages

        print("Missing DataFrames: ", [name for name in names if result[name] is None])

    return result


def get_messages_from_sources(intensives, events, mailbox):
    messages = pd.concat([intensives, events, mailbox], axis=0, ignore_index=True)
    messages = messages.sort_values("date").reset_index(drop=True)
    messages["id"] = messages.index

    messages["day"] = pd.to_datetime(messages["date"]).dt.floor("D")

    messages = messages[
        ~(
                ((messages["content"].isna()) & (messages["type"] == "text"))
                | (messages["type"] == "other")
        )
    ]

    messages = messages[["id", "source_id", "source", "type", "date", "day", "content", "content_structured"]]

    return messages
