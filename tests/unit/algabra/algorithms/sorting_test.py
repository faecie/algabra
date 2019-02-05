import random
import unittest

import algabra.algorithms.sorting as sorting


class QuickSortTestCase(unittest.TestCase):

    def test_sorting(self) -> None:
        items_count = 100
        items = random.sample(list(range(items_count)), items_count)
        sorting.QuickSort.sort(items)

        assert all(items[i] < items[i + 1] for i in range(len(items) - 1))

    def test_sorting_one_item(self) -> None:
        items = [7]
        sorting.QuickSort.sort(items)

        assert items == [7]

    def test_sorting_empty_list(self) -> None:
        items = []
        sorting.QuickSort.sort(items)

        assert not items

    def test_sorting_sorted_list(self) -> None:
        items_count = 100
        items = list(range(items_count))
        target_items = list(items)

        sorting.QuickSort.sort(target_items)

        assert items == target_items


if __name__ == '__main__':
    unittest.main()
