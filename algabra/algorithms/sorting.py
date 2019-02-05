import abc
import random
import typing


class SortInterface(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def sort(items: typing.MutableSequence):
        pass


class InsertionSort(SortInterface):

    @staticmethod
    def sort(items: typing.MutableSequence):
        InsertionSort._sort(items, 0, len(items))

    @staticmethod
    def _sort(items: typing.MutableSequence, start: int, stop: int) -> None:
        for item_index in range(start + 1, stop):
            item = items[item_index]

            prev_item_index = item_index - 1
            while prev_item_index >= 0 and items[prev_item_index] > item:
                items[prev_item_index + 1] = items[prev_item_index]
                prev_item_index -= 1

            items[prev_item_index + 1] = item


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


class QuickWithInsertionSort(QuickSort):
    _INSERTION_SORT_BORDER = 30

    @staticmethod
    def sort(items: typing.MutableSequence):
        first_last_stack = [(0, len(items) - 1)]

        while first_last_stack:
            first, last = first_last_stack.pop()

            elements_count = last - first
            is_easy = QuickWithInsertionSort._is_insertion_sort(elements_count)

            if is_easy:
                InsertionSort._sort(items, first, last + 1)
                pivot = last
            else:
                pivot = QuickSort._partition(items, first, last)

            if pivot + 1 < last:
                first_last_stack.append((pivot + 1, last))

            if pivot - 1 > first and not is_easy:
                first_last_stack.append((first, pivot - 1))

    @staticmethod
    def _is_insertion_sort(elements_count: int) -> bool:
        return elements_count <= QuickWithInsertionSort._INSERTION_SORT_BORDER
