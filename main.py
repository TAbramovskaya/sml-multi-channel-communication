import build_df
import export_df
import pandas as pd


pd.set_option('display.max_columns', None)


if __name__ == "__main__":

    result = build_df.load()
    # To load from CSV use from_csv argument. Full list of file names is
    # ["messages", "intensives", "events", "mailbox", "text_messages", "msg_pairwise_similarity", "day_source_msg_stats"]

    for name, df in result.items():
        if df is not None:
            export_df.to_csv(df, name)

    export_df.to_jsonl(result['text_messages'], sources=['events'])

    cropped = export_df.to_csv_cropped(result)