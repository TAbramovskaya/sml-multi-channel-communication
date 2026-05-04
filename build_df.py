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
    gmail = build_dataframe_gmail(mailbox_service, mailbox_label)

    intensives.to_csv("csv/intensives.csv")
    events.to_csv("csv/events.csv")
    gmail.to_csv("csv/gmail.csv")

    messages = pd.concat([intensives, events, gmail], axis=0, ignore_index=True)
    # messages = messages.drop(columns=["content_structured"])
    messages = messages.sort_values("date")
    messages.to_csv("csv/messages.csv")

    return messages


def from_csv():
    intensives = pd.read_csv("csv/intensives.csv")
    events = pd.read_csv("csv/events.csv")
    gmail = pd.read_csv("csv/gmail.csv")
    messages = pd.read_csv("csv/messages.csv")

    intensives["date"] = pd.to_datetime(intensives["date"])
    events["date"] = pd.to_datetime(events["date"])
    gmail["date"] = pd.to_datetime(gmail["date"])
    messages["date"] = pd.to_datetime(messages["date"])

    return messages