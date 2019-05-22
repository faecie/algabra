import math


def count_consecutive(n):
    count = 0
    for length in range(2, math.ceil(math.sqrt(2 * n))):
        start = (2 * n - length**2 + length) / (2 * length)
        count += 1 if float(start).is_integer() else 0
        if float(start).is_integer():
            print(length)

    return count
