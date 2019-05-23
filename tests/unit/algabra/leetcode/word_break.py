import unittest
import algabra.leetcode.wordbreak as wb


class WordBreakTestCase(unittest.TestCase):

    def test_case1(self):
        solution = wb.Solution()
        assert solution.word_break('leetcode', ['leet', 'code'])

    def test_case2(self):
        solution = wb.Solution()
        assert solution.word_break('applepenapple', ['apple', 'pen'])

    def test_case3(self):
        solution = wb.Solution()
        assert not solution.word_break('catsandog',
                                       ["cats", "dog", "sand", "and", "cat"])

    def test_case4(self):
        solution = wb.Solution()
        assert solution.word_break('aaaaaaa', ["aaaa", "aaa"])

    def test_case5(self):
        solution = wb.Solution()
        assert not solution.word_break(
            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab',
            [
                "a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa",
                "aaaaaaaa", "aaaaaaaaa", "aaaaaaaaaa"
            ])


if __name__ == '__main__':
    unittest.main()
