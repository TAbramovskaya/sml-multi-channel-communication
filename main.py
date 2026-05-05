import build_df
import export_csv
import compare_messages
import daily_summary
import pandas as pd

pd.set_option('display.max_columns', None)


if __name__ == "__main__":
    # ---
    # Option 1: Update data from raw JSON files and current emails and export data to CSV files:
    messages, intensives, events, mailbox = build_df.from_raw_data()
    export_csv.from_df(messages, intensives, events, mailbox, names=["messages", "intensives", "events", "mailbox"])

    #Option 2: Load data from ready-made CSV files:
    messages, *_ = build_df.from_csv()
    # ---

    messages['day'] = pd.to_datetime(messages['date']).dt.floor('D')

    # Remove empty text messages and messages typed as 'other'
    messages = messages[
                  ~(
                    ((messages['content'].isna()) & (messages['type'] == 'text'))
                    | (messages['type'] == 'other')
                    )
                ]

    text_messages = messages[messages['type'] == 'text'].copy()
    text_messages['len'] = text_messages['content'].apply(lambda x: len(x.split(' ')))
    text_messages = text_messages[['id', 'source_id', 'source', 'day', 'content', 'len']]

    # ---
    # Option 1: Update pairwise message comparison from current DataFrame
    # msg_pairwise_similarity = compare_messages.pairwise(text_messages)
    # export_csv.from_df(msg_pairwise_similarity, names=["msg_pairwise_similarity"])

    # Option 2: Load data from ready-made CSV files:
    msg_pairwise_similarity = pd.read_csv("csv/msg_pairwise_similarity.csv")
    msg_pairwise_similarity['day'] = pd.to_datetime(msg_pairwise_similarity['day']).dt.floor('D')
    #---

    day_source_msg_counts = daily_summary.msg_count(messages, text_messages)

    day_source_msg_stats = daily_summary.duplication_rate(msg_pairwise_similarity, day_source_msg_counts)
    export_csv.from_df(day_source_msg_stats, names=["day_source_msg_stats"])
