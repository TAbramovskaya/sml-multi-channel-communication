import pandas as pd
import json
import os


def to_csv(df, name, prefix="data/csv/"):
    path = prefix + name + ".csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def to_jsonl(df,
             day_start="2026-01-01",
             day_end="2026-04-30",
             col="content_structured",
             sources=None,
             output_path="src/ai_analysis/input.jsonl"):
    """
    Export filtered message data to a JSONL file.

    Filters messages by date range and source.
    Then writes one JSON object per line containing message id and selected text column.

    Example line:
        {"id": 123, "text": "Message content here"}
    """

    if sources is None:
        sources = ["events", "intensives", "mailbox"]

    df = df.copy()
    start = pd.to_datetime(day_start, utc=True)
    end = pd.to_datetime(day_end, utc=True) + pd.Timedelta(days=1)

    df = df[(df["day"] >= start)
            & (df["day"] < end)
            & (df["source"].isin(sources))]

    with open(output_path, "w", encoding="utf-8") as f:
        for i, row in df.iterrows():
            record = {
                "id": row["id"],
                "text": row[col]
            }
            if record["text"]:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return df
