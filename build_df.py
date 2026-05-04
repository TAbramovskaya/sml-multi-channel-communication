from extract_json_data import *
from extract_gmail_data import *
import auth


def from_raw_data():
    intensives_file = "raw_data/intensives_simulative_bot.json"
    intensives_label = "intensives"

    events_file = "raw_data/events_simulative_bot.json"
    events_label = "events"

    mailbox_service = auth.build_service()
    mailbox_label = "mailbox"

    intensives = build_dataframe_json(intensives_file, intensives_label)
    events = build_dataframe_json(events_file, events_label)
    mailbox = build_dataframe_gmail(mailbox_service, mailbox_label)

    intensives.to_csv("csv/intensives.csv", index=False)
    events.to_csv("csv/events.csv", index=False)
    mailbox.to_csv("csv/gmail.csv", index=False)

    messages = pd.concat([intensives, events, mailbox], axis=0, ignore_index=True)
    messages = messages.sort_values("date").reset_index(drop=True)
    messages["id"] = messages.index

    messages = messages[["id", "source_id", "source", "type", "date", "content", "content_structured"]]

    messages.to_csv("csv/messages.csv", index=False)

    return messages, intensives, events, mailbox


def from_csv():
    intensives = pd.read_csv("csv/intensives.csv")
    events = pd.read_csv("csv/events.csv")
    mailbox = pd.read_csv("csv/gmail.csv")

    intensives["date"] = pd.to_datetime(intensives["date"])
    events["date"] = pd.to_datetime(events["date"])
    mailbox["date"] = pd.to_datetime(mailbox["date"])

    messages = pd.read_csv("csv/messages.csv")
    messages["date"] = pd.to_datetime(messages["date"])

    return messages, intensives, events, mailbox