def copypaste_score(text, other):
    words_test = text.split(' ')
    words_other = other.split(' ')

    i = 0
    j = 0
    l = 0
    longest = 0

    while i < len(words_test):
        wt = words_test[i]
        while j < len(words_other):
            wo = words_other[j]
            while wt == wo:
                l += 1
                if i + l < len(words_test) and j + l < len(words_other):
                    wt = words_test[i + l]
                    wo = words_other[j + l]
                else:
                    break
            if l > longest:
                longest = max(longest, l)
                print(f'test: {words_test[i:i + l]}')
                print(f'other: {words_other[j:j + l]}')
            l = 0
            j += 1
        i += 1

    return longest, len(words_test), len(words_other)





