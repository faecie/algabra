import math
import enum


class SquareSum(enum.IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4


class PrimeFactorization:
    __slots__ = ['_number']

    def __init__(self, number: int) -> None:
        self._number = number

    @staticmethod
    def _create_sieve(n: int) -> list:
        spf = [0 for _ in range(n + 1)]
        spf[1] = 1
        for i in range(2, n + 1):
            spf[i] = i
        for i in range(4, n + 1, 2):
            spf[i] = 2

        for i in range(3, math.ceil(math.sqrt(n))):
            if spf[i] == i:
                for j in range(i * i, n + 1, i):
                    if spf[j] == j:
                        spf[j] = i

        return spf

    def get_factorization(self) -> dict:
        res = dict()
        spf = self._create_sieve(self._number)
        temp = self._number
        while temp != 1:
            res[spf[temp]] = res[spf[temp]] + 1 if spf[temp] in res else 1
            temp //= spf[temp]

        return res


class PerfectSquareRoot:

    def num_squares(self, n: int) -> int:
        if self._is_square(n):
            return SquareSum.ONE
        if self.is_four_squares(n):
            return SquareSum.FOUR
        if self.is_two_squares(n):
            return SquareSum.TWO

        return SquareSum.THREE

    @staticmethod
    def is_four_squares(n) -> bool:
        """
        Lagrange's four-square theorem
        
        :link: https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem
        """
        for k in range(math.ceil(math.log(n, 4))):
            if (n / 4**k - 7) % 8 == 0:
                return True
        return False

    def is_two_squares(self, n) -> bool:
        """
        Girard, Fermat and Euler Two-square theorem
        
        :link: https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem
        """
        factorization = PrimeFactorization(n)
        for f, power in factorization.get_factorization().items():
            if power % 2 != 0 and (3 - f) % 4 == 0:
                return False
        return True

    @staticmethod
    def _is_square(n: int) -> bool:
        if n - math.floor(math.sqrt(n))**2 == 0:
            return True
