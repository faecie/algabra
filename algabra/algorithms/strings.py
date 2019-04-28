def _decrease_counts(counts, freq):
    if counts[freq] == 1:
        del counts[freq]
    else:
        counts[freq] -= 1


def _increase_counts(counts, freq):
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
            _decrease_counts(counts, frequencies[l])
        frequencies[l] = frequencies[l] + 1 if l in frequencies else 1
        _increase_counts(counts, frequencies[l])
    if len(counts) > 2:
        return 'NO'
    elif len(counts) <= 1:
        return 'YES'

    tmp = counts.copy()
    for freq, count in counts.items():
        _decrease_counts(tmp, freq)
        if freq > 1:
            _increase_counts(tmp, freq - 1)
        if len(tmp) <= 1:
            return 'YES'
        if freq > 1:
            _decrease_counts(tmp, freq - 1)
        _increase_counts(tmp, freq)

    return 'NO'


def anagram_count(n, s):
    count = n
    i = 0
    next_length = 1
    while i < n:
        if i + 1 < n and s[i + 1] == s[i]:
            next_length += 1
        elif i + 2 < n and s[i + 2] == s[i]:
            j = i + 2
            upto = j + next_length
            while j < min(upto, len(s)):
                if s[j] == s[j - next_length - 1]:
                    count += 1
                else:
                    upto = j + 1
                j += 1
            count += int((next_length * (next_length - 1)) / 2)
            next_length = 1
        else:
            count += int((next_length * (next_length - 1)) / 2)
            next_length = 1
        i += 1
    return count


def longest_common_subsequence(s1, s2):
    suffixes = [[0] * (len(s1) + 1) for _ in range(2)]

    ix1 = 1
    for letter1 in s1:
        ix2 = 1
        for letter2 in s2:
            if letter1 == letter2:
                suffixes[ix1][ix2] = suffixes[int(not ix1)][ix2 - 1] + 1
            else:
                suffixes[ix1][ix2] = max(suffixes[int(not ix1)][ix2],
                                         suffixes[ix1][ix2 - 1])
            ix2 += 1
        ix1 = int(not ix1)

    return suffixes[int(not ix1)][ix2 - 1]


class Encodings:
    _DECIMAL = 10
    _LAST_IN_ALPHABET = 26

    def find_encodings(self, code: int) -> int:
        """
        Given a string of digits, count the number of possible decodings
        
        For example:
        find_encodings('111') = 3, because '111' can be decoded as 'aaa', 'ak', 
        'ka'.
        find_encodings('1111') = 'aaaa', 'aka', 'kk', 'aak', 'kaa'
        find_encodings('1234') = 3, because '1234' can be decoded as 'abcd', 
        'lcd', 'awd'.
        :param code: 
        :return: 
        """
        code_str = str(code)
        if len(code_str) == 0:
            return 0

        predecessors = [0, 1]
        for ix in range(1, len(code_str)):
            letter = int(code_str[ix - 1]) * self._DECIMAL + int(code_str[ix])
            current = predecessors[-1] + (max(
                predecessors[0], 1) if letter <= self._LAST_IN_ALPHABET else 0)
            predecessors[0], predecessors[-1] = predecessors[-1], current

        return predecessors[-1]
