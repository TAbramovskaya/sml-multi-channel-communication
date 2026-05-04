import build_df
import pandas as pd
from compare_messages import *

pd.set_option('display.max_columns', None)


if __name__ == "__main__":
    # ---
    # Option 1: Update data from raw JSON files and current emails and export data to CSV files:
    # messages, *_ = build_df.from_raw_data()

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
    # pairwise_messages = pairwise_similarity_table(text_messages)

    # Option 2: Load data from ready-made CSV files:
    pairwise_messages = pd.read_csv("csv/pairwise_messages.csv")
    pairwise_messages["day"] = pd.to_datetime(pairwise_messages["day"]).dt.floor('D')
    #---


    similarity_summary = similar_count(pairwise_messages)
    similarity_summary.to_csv("csv/similarity_summary.csv", index=False)

