import unittest
import random
import algabra.datastructures.heap as my_heap


class HeapTestCase(unittest.TestCase):

    def test_sorting_asc(self):
        items_count = 100
        sorted_list = list(range(items_count))
        unsorted_list = random.sample(sorted_list, items_count)

        assert my_heap.MaxHeap.get_sorted_list(unsorted_list) == sorted_list

    def test_sorting_desc(self):
        items_count = 100
        sorted_list = list(range(items_count, 0, -1))
        unsorted_list = random.sample(sorted_list, items_count)

        assert my_heap.MinHeap.get_sorted_list(unsorted_list) == sorted_list


if __name__ == '__main__':
    unittest.main()
