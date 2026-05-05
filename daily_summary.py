import pandas as pd


def msg_count(messages, text_messages):
    """
    Counts the number of messages for each (day, source) pair.
    Returns a DataFrame with the columns ['id', 'day', 'source', 'text_count', 'total_count']
    """

    text_counts = text_messages.groupby(['day', 'source']).size().reset_index(name='text_count')
    total_counts = messages.groupby(['day', 'source']).size().reset_index(name='total_count')
    msg_counts = total_counts.merge(text_counts, how='left', on=['day', 'source']).fillna(0)
    msg_counts['id'] = msg_counts.index
    msg_counts = msg_counts[['id', 'day', 'source', 'text_count', 'total_count']]

    return msg_counts


def duplication_rate(pairwise, msg_counts):
    """
    Extends message counts with duplication metrics per (day, source).

    Identifies text messages that have at least one similar match with a message
    from another source on the same day, and computes duplication statistics.

    Returns a DataFrame with the columns
        ['id', 'day', 'source', 'text_count', 'total_count', 'duplicates_count', 'duplication_rate']
    where the following additional ones are:
    - duplicates_count: number of text messages per (day, source) that were
      marked as duplicates in at least one other source on the same day
    - duplication_rate: proportion of duplicated messages among all text messages
      for the given (day, source), calculated as duplicates_count / text_count
    """

    similar_pairs = pairwise[pairwise['is_similar']]

    # Collect duplicated message ids for source_1
    left = similar_pairs[['day', 'source_1', 'source_id_1']].rename(
        columns={'source_1': 'source', 'source_id_1': 'msg_id'}
    )

    # Collect duplicated message ids for source_2
    right = similar_pairs[['day', 'source_2', 'source_id_2']].rename(
        columns={'source_2': 'source', 'source_id_2': 'msg_id'}
    )

    # Combine both sides
    duplicates_msgs = pd.concat([left, right], ignore_index=True)

    # keep unique (day, source, message_id)
    duplicates_msgs = duplicates_msgs.drop_duplicates()
    duplicates_msgs.to_csv('duplicates_msgs.csv', index=False)

    # count duplicated messages per (day, source)
    duplicates_counts = (
        duplicates_msgs.groupby(['day', 'source'])
        .size()
        .reset_index(name='duplicates_count')
    )

    result = msg_counts.merge(duplicates_counts, on=['day', 'source'], how='left').fillna(0)

    result['duplication_rate'] = (
        result['duplicates_count'] / result['text_count']
    )

    result = result[['id', 'day', 'source', 'text_count', 'total_count', 'duplicates_count', 'duplication_rate']]

    return result


def similar_count(pairwise, msg_counts):
    similar_counts = (
        pairwise[pairwise['is_similar']]
        .assign(
            source_a=lambda df: df[['source_1', 'source_2']].min(axis=1),
            source_b=lambda df: df[['source_1', 'source_2']].max(axis=1),
        )
        .groupby(['day', 'source_a', 'source_b'])
        .size()
        .reset_index(name='similar_count')
    )

    similar_counts = (similar_counts
                         .merge(
                            msg_counts.rename(columns={'source': 'source_a', 'text_count': 'msg_count_a'}),
                            on=['day', 'source_a'],
                            how='left'
                        ).merge(
                            msg_counts.rename(columns={'source': 'source_b', 'text_count': 'msg_count_b'}),
                            on=['day', 'source_b'],
                            how='left'
                        ))

    # Duplicate ratio shows how much messages overlap relative to volume
    similar_counts['duplication_ratio'] = (
        (2 * similar_counts['similar_count']) / (similar_counts['msg_count_a'] + similar_counts['msg_count_b'])
    )

    return similar_counts
