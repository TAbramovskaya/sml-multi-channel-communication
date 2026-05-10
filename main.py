from src import export_df, build_df, msg_summary
import src.ai_analysis.llm as llm
import src.ai_analysis.postprocess_llm_results as postprocess


def get_messages(from_csv):

    result = build_df.load(from_csv)

    if result["messages"] is None:
        print("Failed to load messages")
        return None

    return result


def ai_analysis(messages):
    llm_input = "src/ai_analysis/input.jsonl"
    llm_output = "src/ai_analysis/output.jsonl"

    text_messages = msg_summary.get_text_messages(result["messages"])
    txt_msg_cropped = export_df.to_jsonl(text_messages, output_path=llm_input)

    llm.process(llm_input, llm_output)

    txt_msg_cropped = postprocess.add_features(txt_msg_cropped, llm_output)

    return txt_msg_cropped


def export_to_vis(result):
    messages = result["messages"][["id", "source_id", "source", "type", "day", "words_count", "length_category"]]
    daily_stats = result["daily_stats"]

    export_df.to_csv(daily_stats, "!dailystats")
    export_df.to_csv(messages, "!messages")


if __name__ == "__main__":

    # File "data/csv/messages.csv" is mandatory if from_csv=True
    result = get_messages(from_csv=True)

    if result is not None:
        print(result["messages"].columns)
        result["messages"] = msg_summary.add_text_summary(result["messages"])
        result["daily_stats"] = msg_summary.build_daily_stats(result["messages"])
        result["llm_analysis_output"] = ai_analysis(result["messages"])

        for name, df in result.items():
            if df is not None:
                export_df.to_csv(df, name)

        export_to_vis(result)

