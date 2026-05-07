import build_df
import export_df
import analysis.llm as llm
import analysis.postprocess_llm_results as postprocess


if __name__ == "__main__":

    result = build_df.load()
    # Use the from_csv argument to load (some) data from a CSV files. Here is the full list of DataFrames
    # that can be loaded from existing files.
    # ["messages", "intensives", "events", "mailbox", "text_messages", "msg_pairwise_similarity", "day_source_msg_stats"]

    for name, df in result.items():
        if df is not None:
            export_df.to_csv(df, name)

    cropped = export_df.to_many_csv_cropped(result)

    txt_msg_cropped = export_df.to_jsonl_cropped(result['text_messages'], output_path='analysis/input.jsonl')

    llm.process("analysis/input.jsonl", "analysis/output.jsonl")

    txt_msg_cropped = postprocess.add_features(txt_msg_cropped, "analysis/output.jsonl")

    export_df.to_csv(txt_msg_cropped, "cropped/!txt_msg_llm")
