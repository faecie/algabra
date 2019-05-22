import unittest
import algabra.algorithms.math as mymath


class ConsecutiveNumbersTest(unittest.TestCase):

    def test_find_consecutive_numbers_test(self) -> None:
        number = mymath.count_consecutive(5)

        assert number == 1

    def test_find_consecutive_numbers_test1(self) -> None:
        number = mymath.count_consecutive(15)

        assert number == 3

    def test_find_consecutive_numbers_test2(self) -> None:
        number = mymath.count_consecutive(21)

        assert number == 3
