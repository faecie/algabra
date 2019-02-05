import math
import typing


def binary_search(items: typing.Sequence, value: int) -> typing.Optional[int]:
    """
    Classic implementation of Binary Search

    Get a middle point of a list and if the value is greater than searching -
    do the same with a left part or with right part if the value is less

    :param items: MUST be already sorted sequence of integers
    :param value: Is the integer value that we want to find
    :return: The key of the value in the sequence or None if its not in it
    """
    first, last = 0, len(items) - 1
    while last > first:
        middle = last - math.floor((last - first) / 2)

        if items[middle] == value:
            return middle

        if items[middle] < value:
            first = middle
        else:
            last = middle - 1

    return None
