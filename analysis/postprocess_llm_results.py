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
    df["transformation_score"] = df["id"].map(lambda x: results.get(x, {}).get("transformation_score"))
    df["author"] = df["id"].map(lambda x: results.get(x, {}).get("author"))
    df["author"] = df["author"].apply(lambda x: config.aliases.get(x, x))

    df["tags"] = df["id"].map(lambda x: (results.get(x, {}).get("tags") or [None, None, None]))
    df[["tag_1", "tag_2", "tag_3"]] = pd.DataFrame(df["tags"].tolist(), index=df.index)
    df.drop(columns=["tags"], inplace=True)

    for tag in ["tag_1", "tag_2", "tag_3"]:
        df[tag] = df[tag].apply(lambda x: config.tags_eng.get(x, x))

    bins = [0, 20, 40, 60, 80, 100]
    labels = [
        "minimal edits",
        "light edits",
        "structural changes",
        "strong rewrite",
        "heavy reconstruction"
    ]

    df["transformation_type"] = pd.cut(df["transformation_score"], bins=bins, labels=labels, include_lowest=True)


    return df
