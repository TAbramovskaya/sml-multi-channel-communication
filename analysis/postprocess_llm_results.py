import pandas as pd
import json
import analysis.postprocess_config as config

def add_features(df, path):
    results = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            results[row["id"]] = row

    # map results into dataframe

    df["author"] = df["id"].map(lambda x: results.get(x, {}).get("author"))
    df["author"] = df["author"].apply(lambda x: config.aliases.get(x, x))

    df["tag_intent"] = df["id"].map(lambda x: results.get(x, {}).get("tag_intent", "other"))
    df["tag_content"] = df["id"].map(lambda x: results.get(x, {}).get("tag_content", "other"))
    df["tag_delivery_style"] = df["id"].map(lambda x: results.get(x, {}).get("tag_delivery_style", "other"))

    for tag in ["tag_intent", "tag_content", "tag_delivery_style"]:
        df[tag] = df[tag].apply(lambda x: config.tags_rus_eng[tag].get(x, x))

    df["transformation_score"] = df["id"].map(lambda x: results.get(x, {}).get("transformation_score"))
    bins = [0, 20, 40, 60, 80, 100]
    labels = [
        "minimal edits",
        "light edits",
        "structural changes",
        "strong rewrite",
        "heavy reconstruction"
    ]

    df["transformation_type"] = pd.cut(df["transformation_score"], bins=bins, labels=labels, include_lowest=True)

    df = df[["id", "source_id", "source", "date", "day", "words_count",
             "transformation_score", "transformation_type", "author",
             "tag_intent", "tag_content", "tag_delivery_style"]]

    return df
