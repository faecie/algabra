import unittest
import algabra.leetcode.zigzag_conversion as zigzag


class MyTestCase(unittest.TestCase):

    def test_1(self):
        """
        P   A   H   N
        A P L S I I G
        Y   I   R
        """
        solution = zigzag.Solution()
        actual = solution.convert("PAYPALISHIRING", 3)

        self.assertEqual("PAHNAPLSIIGYIR", actual)

    def test_2(self):
        """
        P     I    N
        A   L S  I G
        Y A   H R
        P     I
        """
        solution = zigzag.Solution()
        actual = solution.convert("PAYPALISHIRING", 4)

        self.assertEqual("PINALSIGYAHRPI", actual)

    def test_3(self):
        solution = zigzag.Solution()
        actual = solution.convert("A", 1)

        self.assertEqual("A", actual)


if __name__ == '__main__':
    unittest.main()
