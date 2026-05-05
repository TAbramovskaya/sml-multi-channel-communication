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
    text_messages = text_messages[['id', 'source_id', 'source', 'day', 'content']]

    # ---
    # Option 1: Update pairwise message comparison from current DataFrame
    pairwise_msg_similarity = compare_messages.pairwise(text_messages)
    export_csv.from_df(pairwise_msg_similarity, names=["pairwise_msg_similarity"])

    # Option 2: Load data from ready-made CSV files:
    # pairwise_msg_similarity = pd.read_csv("csv/pairwise_msg_similarity.csv")
    # pairwise_msg_similarity["day"] = pd.to_datetime(pairwise_msg_similarity["day"]).dt.floor('D')
    # #---

    msg_counts = daily_summary.msg_count(messages, text_messages)

    similarity_summary = daily_summary.similar_count(pairwise_msg_similarity, msg_counts)
    export_csv.from_df(similarity_summary, names=["similarity_summary.csv"])

