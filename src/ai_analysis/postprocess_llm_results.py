import pandas as pd
import json
import src.ai_analysis.postprocess_config as config


def add_features(df, path):
    results = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            results[row["id"]] = row

    df["author"] = (
        df["id"]
        .map(
            lambda x: results.get(x, {}).get("author")
        )
    )

    df["author"] = (
        df["author"]
        .apply(
            lambda x: config.aliases.get(x, x)
        )
    )

    for tag in ["tag_intent", "tag_content", "tag_delivery_style"]:
        df[tag] = df["id"].map(lambda x: results.get(x, {}).get(tag))

    for tag in ["tag_intent", "tag_content", "tag_delivery_style"]:
        df[tag] = df[tag].apply(lambda x: config.tags_rus_eng[tag].get(x, x))

    df["transformation_score"] = (
        df["id"]
        .map(
            lambda x: results.get(x, {}).get("transformation_score")
        )
    )

    df["transformation_type"] = (
        pd.cut(
            df["transformation_score"],
            bins=config.transformation_bins,
            labels=config.transformation_labels,
            include_lowest=True
        )
    )

    df = df[["id", "source_id", "source", "date", "day", "words_count",
             "transformation_score", "transformation_type", "author",
             "tag_intent", "tag_content", "tag_delivery_style"]]

    return df
