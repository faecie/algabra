class Solution:
    _FIRST_ROW = 0

    def convert(self, s: str, num_rows: int) -> str:
        result = ['' for _ in range(len(s))]

        ix = 0
        row = 0
        while row < num_rows:
            pace = max(2 * (num_rows - 1), 1)
            letter = row
            while letter < len(s):
                result[ix] = s[letter]
                ix += 1
                if self._FIRST_ROW < row < num_rows - 1:
                    pair_ix = letter + 2 * num_rows - 2 * row - 2
                    if pair_ix < len(s):
                        result[ix] = s[pair_ix]
                        ix += 1
                letter += pace
            row += 1

        return ''.join(result)
