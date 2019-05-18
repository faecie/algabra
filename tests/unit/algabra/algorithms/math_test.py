import unittest
import algabra.leetcode.square_root as sr


class PerfectSquareRootTest(unittest.TestCase):

    def test_count_min_squares(self) -> None:
        solution = sr.PerfectSquareRoot()
        result = solution.num_squares(28)

        assert result == 4
