import pandas as pd


def msg_count(messages, text_messages):
    text_counts = text_messages.groupby(['day', 'source']).size().reset_index(name='text_count')
    all_counts = messages.groupby(['day', 'source']).size().reset_index(name='all_count')
    msg_counts = all_counts.merge(text_counts, how='left', on=['day', 'source']).fillna(0)

    return msg_counts


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
