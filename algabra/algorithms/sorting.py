import abc
import random
import typing


class SortInterface(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def sort(elements: typing.MutableSequence):
        pass


class QuickSort(SortInterface):

    @staticmethod
    def sort(items: typing.MutableSequence):
        first_last_stack = [(0, len(items) - 1)]

        while first_last_stack:
            first, last = first_last_stack.pop()
            pivot = QuickSort._partition(items, first, last)

            if pivot + 1 < last:
                first_last_stack.append((pivot + 1, last))

            if pivot - 1 > first:
                first_last_stack.append((first, pivot - 1))

    @staticmethod
    def _partition(items: typing.MutableSequence, first: int, last: int) -> int:
        if first >= last:
            return first

        rand_ix = random.randint(first, last)
        items[last], items[rand_ix] = items[rand_ix], items[last]
        pivot_element = items[last]
        pivot = first - 1

        for next_item in range(first, last):
            if items[next_item] <= pivot_element:
                pivot += 1
                items[next_item], items[pivot] = items[pivot], items[next_item]
        items[pivot + 1], items[last] = items[last], items[pivot + 1]

        return pivot + 1
