import pandas as pd
import src.compare_messages as compare


def build_daily_stats(messages):
    text_messages = get_text_messages(messages)
    # ["id", "source_id", "source", "date", "day", "words_count", "length_category", "content", "content_structured"]

    daily_stats = get_daily_counts(messages, text_messages)
    # ["day", "source", "total", "text", "short", "standard", "long", "words_count", "duplicates"]

    # Expand index: add missing (day, source) pairs
    daily_stats = add_missing_index(daily_stats)

    daily_stats = merge_rolling_avg(daily_stats)
    # ["day", "source", "total", "text", "short", "standard", "long", "words_count", "duplicates",
    # "total_7d_avg", "text_7d_avg", "short_7d_avg", "standard_7d_avg", "long_7d_avg", "words_count_7d_avg", "duplicates_7d_avg"]

    return daily_stats


def add_text_summary(messages):
    text_messages = get_text_messages(messages)

    messages = (
        messages
        .merge(
            text_messages[["id", "words_count", "length_category"]],
            how="left",
            on="id"
        )
    )

    messages = messages[(
            (messages["type"] != "text") |
            (messages["type"] == "text") & (messages["words_count"] > 1)
    )]

    return messages


def get_text_messages(messages):
    text_messages = (
        messages[messages["type"] == "text"].copy()
    )

    text_messages = (
        text_messages[text_messages["content"].notna()]
    )

    text_messages["words_count"] = (
        text_messages["content"]
        .apply(lambda x: len(x.split(" ")))
    )

    text_messages["length_category"] = (
        text_messages["words_count"]
        .apply(categorize_length)
    )

    text_messages = (
        text_messages[[
            "id",
            "source_id",
            "source",
            "date",
            "day",
            "words_count",
            "length_category",
            "content",
            "content_structured"]]
    )

    return text_messages


def get_daily_counts(messages, text_messages):
    """
    Aggregate daily communication statistics by (day, source).

    The resulting statistics include:
    - total number of messages
    - number of text messages
    - number of words
    - counts of message length categories
    - number of duplicate messages
    """

    daily_text = (
        text_messages
        .groupby(["day", "source"])
        .size()
        .reset_index(name="text")
    )

    daily_total = (
        messages
        .groupby(["day", "source"])
        .size()
        .reset_index(name="total")
    )

    daily_words_count = (
        text_messages
        .groupby(["day", "source"])["words_count"]
        .sum()
        .reset_index(name="words_count")
    )

    daily_lengths = (
        text_messages
        .groupby(["day", "source", "length_category"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    pairwise = compare.pairwise(text_messages)

    daily_duplicates = duplication_rate(pairwise)

    daily_stats = (
        daily_total
        .merge(daily_text, on=["day", "source"], how="left")
        .merge(daily_lengths, on=["day", "source"], how="left")
        .merge(daily_words_count, on=["day", "source"], how="left")
        .merge(daily_duplicates, on=["day", "source"], how="left")
        .fillna(0)
    )

    # daily_stats["duplication_rate"] = (
    #     round(daily_stats["duplicates"] / daily_stats["text"], 2)
    # )

    daily_stats = (
        daily_stats[[
            "day",
            "source",
            "total",
            "text",
            "short",
            "standard",
            "long",
            "words_count",
            "duplicates"
        ]]
    )

    return daily_stats


def add_missing_index(daily_stats):
    """
    Add missing (day, source) combinations to a daily statistics.
    Missing combinations are added with values filled as 0.
    """

    all_days = pd.date_range(
        start=daily_stats["day"].min(),
        end=daily_stats["day"].max(),
        freq="D"
    )

    all_sources = daily_stats["source"].unique()

    full_index = pd.MultiIndex.from_product(
        [all_days, all_sources],
        names=["day", "source"]
    )

    daily_stats = (
        daily_stats
        .set_index(["day", "source"])
        .reindex(full_index, fill_value=0)
        .reset_index()
    )

    daily_stats = daily_stats.sort_values(["source", "day"])

    return daily_stats


def merge_rolling_avg(daily_stats):
    """
    Calculate 7-day rolling averages for communication metrics grouped by source.

    For each source, computes backward-looking 7-day rolling averages
    (current day + previous 6 days) for message activity metrics and
    appends them as new columns with the `_7d_avg` suffix.
    """

    rolling_cols = [
        "total",
        "text",
        "short",
        "standard",
        "long",
        "words_count",
        "duplicates"
    ]

    daily_stats[[f"{c}_7d_avg" for c in rolling_cols]] = (
        daily_stats
        .groupby("source")[rolling_cols]
        .transform(
            lambda x:
                round(
                    x.rolling(
                        window=7,
                        min_periods=1
                    ).mean()
                , 2)
        )
    )

    return daily_stats


def duplication_rate(pairwise): #, text_messages):
    """
    Identifies text messages that have at least one similar match with a message
    from another source on the same day, and computes duplication statistics.

    Returns a DataFrame with the columns
        ["day", "source", "duplicates"]

    duplicates: number of text messages per (day, source) that were
      marked as duplicates in at least one other source on the same day
    """

    similar_pairs = pairwise[pairwise["is_similar"]]

    # Collect duplicated message ids for source_1
    left = similar_pairs[["day", "source_1", "source_id_1"]].rename(
        columns={"source_1": "source", "source_id_1": "msg_id"}
    )

    # Collect duplicated message ids for source_2
    right = similar_pairs[["day", "source_2", "source_id_2"]].rename(
        columns={"source_2": "source", "source_id_2": "msg_id"}
    )

    # Combine both sides
    duplicates_msgs = pd.concat([left, right], ignore_index=True)

    # keep unique (day, source, message_id)
    duplicates_msgs = duplicates_msgs.drop_duplicates()

    # count duplicated messages per (day, source)
    duplicates_counts = (
        duplicates_msgs.groupby(["day", "source"])
        .size()
        .reset_index(name="duplicates")
    )

    return duplicates_counts


def categorize_length(n):
    if n < 50:
        return "short"
    elif n < 150:
        return "standard"
    else:
        return "long"