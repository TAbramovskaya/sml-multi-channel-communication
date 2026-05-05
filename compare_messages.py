import pandas as pd


def copypaste_score(text, other):
    words_test = text.split(' ')
    words_other = other.split(' ')

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
    daily_comparisons = []

    for day, group in text_messages.groupby('day'):
        pairs = (group
                  .merge(group, how='cross', suffixes=('_1', '_2'))
                  .query('source_1 != source_2')
                  .query('id_1 < id_2')
                  )
        if pairs.empty:
            continue

        pairs['copypaste_score'] = [copypaste_score(a, b) for a, b in zip(pairs['content_1'], pairs['content_2'])]
        pairs['is_similar'] = pairs['copypaste_score'] > 41
        daily_comparisons.append(pairs)

    pairwise_messages = pd.concat(daily_comparisons, ignore_index=True)
    pairwise_messages['day'] = pairwise_messages['day_1']
    pairwise_messages['id'] = pairwise_messages.index
    pairwise_messages = pairwise_messages[['id', 'day', 'copypaste_score', 'is_similar', 'source_1', 'source_2', 'source_id_1', 'source_id_2', 'content_1' , 'content_2']]

    return pairwise_messages
