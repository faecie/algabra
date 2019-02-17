def decrease_counts(counts, freq):
    if counts[freq] == 1:
        del counts[freq]
    else:
        counts[freq] -= 1

def increase_counts(counts, freq):
    if freq == 0:
        return
    if freq in counts:
        counts[freq] += 1
    else:
        counts[freq] = 1

def is_valid(s):
    frequencies = dict()
    counts = dict()
    for l in s:
        if l in frequencies:
            decrease_counts(counts, frequencies[l])
        frequencies[l] = frequencies[l] + 1 if l in frequencies else 1
        increase_counts(counts, frequencies[l])
    if len(counts) > 2:
        return 'NO'
    elif len(counts) <= 1:
        return 'YES'

    tmp = counts.copy()
    for freq, count in counts.items():
        decrease_counts(tmp, freq)
        if freq > 1:
            increase_counts(tmp, freq - 1)
        if len(tmp) <= 1:
            return 'YES'
        if freq > 1:
            decrease_counts(tmp, freq - 1)
        increase_counts(tmp, freq)

    return 'NO'


def anagram_count(n, s):
    count = n

    for i in range(1, n):
        count += 1 if s[i] == s[i-1] else 0
