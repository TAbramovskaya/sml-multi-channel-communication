import build_df
import export_df
import analysis.llm as llm
import pandas as pd


pd.set_option('display.max_columns', None)


if __name__ == "__main__":

    # result = build_df.load()
    # Use the from_csv argument to load (some) data from a CSV files. Here is the full list of DataFrames
    # that can be loaded from existing files.
    # ["messages", "intensives", "events", "mailbox", "text_messages", "msg_pairwise_similarity", "day_source_msg_stats"]

    for name, df in result.items():
        if df is not None:
            export_df.to_csv(df, name)


    cropped = export_df.to_many_csv_cropped(result)
    txt_msg_events_cropped = export_df.to_jsonl_cropped(result['text_messages'], sources=['events'])

    llm.process("analysis/input.jsonl", "analysis/output.jsonl")
