import random
import unittest
import abc
import typing

import algabra.algorithms.sorting as sorting


class BaseSortingTests(abc.ABC):

    def test_sorting(self) -> None:
        items_count = 100
        items = random.sample(list(range(items_count)), items_count)
        self._sort(items)

        assert all(items[i] < items[i + 1] for i in range(len(items) - 1))

    def test_sorting_one_item(self) -> None:
        items = [7]
        self._sort(items)

        assert items == [7]

    def test_sorting_empty_list(self) -> None:
        items = []
        self._sort(items)

        assert not items

    def test_sorting_sorted_list(self) -> None:
        items_count = 100
        items = list(range(items_count))
        target_items = list(items)

        self._sort(target_items)

        assert items == target_items

    @abc.abstractmethod
    def _sort(self, items: typing.MutableSequence) -> None:
        pass


class QuickSortTestCase(BaseSortingTests, unittest.TestCase):

    def _sort(self, items: typing.MutableSequence) -> None:
        sorting.QuickSort.sort(items)


class InsertionSortTestCase(BaseSortingTests, unittest.TestCase):

    def _sort(self, items: typing.MutableSequence) -> None:
        sorting.InsertionSort.sort(items)


if __name__ == '__main__':
    unittest.main()
