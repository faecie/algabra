import typing


class Solution(object):

    def word_break(self, s: str, word_dict: typing.List[str]) -> bool:
        dp = {'': True}
        for i in range(1, len(s) + 1):
            if s[:i] in dp:
                continue
            for j in range(i, 0, -1):
                if s[j:i] not in dp:
                    dp[s[j:i]] = s[j:i] in word_dict
                if s[:j] not in dp:
                    dp[s[:j]] = s[:j] in word_dict
                if dp[s[:j]] and dp[s[j:i]]:
                    dp[s[:i]] = True
                    break
                else:
                    dp[s[:i]] = False

        return dp[s]
