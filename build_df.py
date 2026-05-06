from extract_json_data import *
from extract_gmail_data import *
import daily_summary
import compare_messages
import auth
import os


def load(from_csv=None):
    if not from_csv:
        from_csv = []

    failed = []
    names = {"messages", "intensives", "events", "mailbox", "text_messages",
             "msg_pairwise_similarity", "day_source_msg_stats"}
    result = {name: None for name in names}

    if "messages" not in from_csv:
        intensives = build_dataframe_json("raw_data/intensives.json", "intensives")
        events = build_dataframe_json("raw_data/events.json", "events")
        mailbox = build_dataframe_gmail(auth.build_service(), "mailbox")

        messages = pd.concat([intensives, events, mailbox], axis=0, ignore_index=True)
        messages = messages.sort_values('date').reset_index(drop=True)
        messages['id'] = messages.index

        messages['day'] = pd.to_datetime(messages['date']).dt.floor('D')

        messages = messages[
            ~(
                    ((messages['content'].isna()) & (messages['type'] == 'text'))
                    | (messages['type'] == 'other')
            )
        ]

        messages = messages[['id', 'source_id', 'source', 'type', 'date', 'day', 'content', 'content_structured']]

        result["intensives"] = intensives
        result["events"] = events
        result["mailbox"] = mailbox
        result["messages"] = messages

    else:
        if os.path.exists('csv/intensives.csv'):
            intensives = pd.read_csv('csv/intensives.csv')
            intensives['date'] = pd.to_datetime(intensives['date'], utc=True, errors="coerce")
            result['intensives'] = intensives
        else:
            failed.append("intensives")

        if os.path.exists('csv/events.csv'):
            events = pd.read_csv('csv/events.csv')
            events['date'] = pd.to_datetime(events['date'], utc=True, errors="coerce")
            result['events'] = events
        else:
            failed.append("events")

        if os.path.exists('csv/mailbox.csv'):
            mailbox = pd.read_csv('csv/mailbox.csv')
            mailbox['date'] = pd.to_datetime(mailbox['date'], utc=True, errors="coerce")
            result['mailbox'] = mailbox
        else:
            failed.append("mailbox")

        if os.path.exists('csv/messages.csv'):
            messages = pd.read_csv("csv/messages.csv")
            messages['date'] = pd.to_datetime(messages['date'], utc=True, errors="coerce")
            messages['day'] = pd.to_datetime(messages['date']).dt.floor('D')
            result['messages'] = messages
        else:
            failed.append("messages")

    if "messages" in failed:
        print("Failed to load messages")
        return None
    else:
        if "text_messages" not in from_csv:
            text_messages = messages[messages['type'] == 'text'].copy()
            text_messages['words_count'] = text_messages['content'].apply(lambda x: len(x.split(' ')))
            text_messages = text_messages[text_messages['words_count'] > 1]
            text_messages = text_messages[['id', 'source_id', 'source', 'date', 'day', 'words_count', 'content', 'content_structured']]

            result["text_messages"] = text_messages
        else:
            if os.path.exists('csv/text_messages.csv'):
                text_messages = pd.read_csv("csv/text_messages.csv")
                text_messages['date'] = pd.to_datetime(text_messages['date'], utc=True, errors="coerce")
                text_messages['day'] = pd.to_datetime(text_messages['day'], utc=True, errors="coerce")
                result['text_messages'] = text_messages
            else:
                failed.append("text_messages")

        if "msg_pairwise_similarity" not in from_csv:
                if "text_messages" not in failed:
                    msg_pairwise_similarity = compare_messages.pairwise(text_messages)
                    msg_pairwise_similarity['day'] = pd.to_datetime(msg_pairwise_similarity['day']).dt.floor('D')
                    result["msg_pairwise_similarity"] = msg_pairwise_similarity
                else:
                    failed.append("msg_pairwise_similarity")
        else:
            if os.path.exists('csv/msg_pairwise_similarity.csv'):
                msg_pairwise_similarity = pd.read_csv("csv/msg_pairwise_similarity.csv")
                msg_pairwise_similarity['day'] = pd.to_datetime(msg_pairwise_similarity['day'], utc=True, errors="coerce")
                result["msg_pairwise_similarity"] = msg_pairwise_similarity
            else:
                failed.append("msg_pairwise_similarity")

        if "day_source_msg_counts" not in from_csv:
            if "text_messages" not in failed and "msg_pairwise_similarity" not in failed:
                day_source_msg_counts = daily_summary.msg_count(messages, text_messages)
                day_source_msg_stats = daily_summary.duplication_rate(msg_pairwise_similarity, day_source_msg_counts)
                result["day_source_msg_stats"] = day_source_msg_stats
            else:
                failed.append("day_source_msg_stats")
        else:
            if os.path.exists('csv/day_source_msg_stats.csv'):
                day_source_msg_stats = pd.read_csv("csv/day_source_msg_stats.csv")
                day_source_msg_stats['day'] = pd.to_datetime(day_source_msg_stats['day'], utc=True, errors="coerce")
                result["day_source_msg_stats"] = day_source_msg_stats
            else:
                failed.append("day_source_msg_stats")

    return result
