import pandas as pd


def copypaste_len(text, other):
    words_test = text.split(" ")
    words_other = other.split(" ")

    longest = 0

    for i in range(len(words_test)):
        for j in range(len(words_other)):
            l = 0
            while i + l < len(words_test) and j + l < len(words_other) and words_test[i + l] == words_other[j + l]:
                l += 1
            if l > longest:
                longest = l

    return longest


def pairwise(text_messages):
    """
    `Performs pairwise comparison of text messages within each day.

    Compares messages from different sources and computes a similarity
    based on the longest consecutive overlap (measured in number of words)
    between two messages.

    Returns a DataFrame with the columns
        ["id", "day", "copypaste_len", "words_count_1", "words_count_2",
        "is_similar", "source_1", "source_2", "source_id_1", "source_id_2", "content_1" , "content_2"]
    where

    - id: unique identifier of the comparison
    - day: the day of the messages
    - copypaste_len: similarity score between two messages
    - is_similar: boolean flag indicating whether the score exceeds the threshold
    - source_1, source_2: sources of the compared messages
    - source_id_1, source_id_2: original message identifiers per source
    - content_1, content_2: message contents being compared
    - words_count_1, words_count_2: words count in two messages
    """

    threshold = 41
    daily_comparisons = []

    for day, group in text_messages.groupby("day"):
        pairs = (group
                  .merge(group, how="cross", suffixes=("_1", "_2"))
                  .query("source_1 != source_2")
                  .query("id_1 < id_2")
                  )
        if pairs.empty:
            continue

        pairs["copypaste_len"] = [copypaste_len(a, b) for a, b in zip(pairs["content_1"], pairs["content_2"])]
        pairs["is_similar"] = pairs["copypaste_len"] > threshold
        daily_comparisons.append(pairs)

    pairwise_messages = pd.concat(daily_comparisons, ignore_index=True)
    pairwise_messages["day"] = pairwise_messages["day_1"]
    pairwise_messages["id"] = pairwise_messages.index
    pairwise_messages = pairwise_messages[["id", "day", "copypaste_len", "words_count_1", "words_count_2", "is_similar",
                                           "source_1", "source_2", "id_1", "id_2", "source_id_1", "source_id_2",
                                           "content_1" , "content_2"]]

    return pairwise_messages
