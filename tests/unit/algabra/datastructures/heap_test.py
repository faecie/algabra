import math
import random
import unittest

import algabra.datastructures.heap as my_heap


class HeapTestCase(unittest.TestCase):

    def test_sorting_asc(self) -> None:
        items_count = 100
        sorted_list = list(range(items_count))
        unsorted_list = random.sample(sorted_list, items_count)

        assert my_heap.MaxHeap.get_sorted_list(unsorted_list) == sorted_list

    def test_sorting_desc(self) -> None:
        items_count = 100
        sorted_list = list(range(items_count, 0, -1))
        unsorted_list = random.sample(sorted_list, items_count)

        assert my_heap.MinHeap.get_sorted_list(unsorted_list) == sorted_list

    def test_sort_extracting_desc(self) -> None:
        items_count = 100
        sorted_list = list(range(items_count, 0, -1))
        max_heap = my_heap.MaxHeap(random.sample(sorted_list, items_count))
        target_list = _get_sorted_by_extracting(max_heap)

        assert target_list == sorted_list

    def test_sort_extracting_asc(self) -> None:
        items_count = 100
        sorted_list = list(range(items_count))
        min_heap = my_heap.MinHeap(random.sample(sorted_list, items_count))
        target_list = _get_sorted_by_extracting(min_heap)

        assert target_list == sorted_list

    def test_increase_key(self) -> None:
        items_count = 100
        max_heap = my_heap.MaxHeap(
            random.sample(list(range(items_count)), items_count))

        max_heap.promote_key(93, 90)
        assert max_heap.extract_highest() == 99

        max_heap.promote_key(11, 100)
        assert max_heap.extract_highest() == 100

    def test_decrease_key(self) -> None:
        items_count = 100
        min_heap = my_heap.MinHeap(
            random.sample(list(range(items_count)), items_count))

        min_heap.promote_key(85, 9)
        assert min_heap.extract_highest() == 0

        min_heap.promote_key(66, -1)
        assert min_heap.extract_highest() == -1

    def test_demote_fails(self) -> None:
        items_count = 100
        min_heap = my_heap.MinHeap(
            random.sample(list(range(items_count)), items_count))

        with self.assertRaises(TypeError):
            min_heap.promote_key(44, 100)

    def test_create_inserting(self) -> None:
        items_count = 100
        max_heap = my_heap.MaxHeap([])
        for value in random.sample(list(range(items_count)), items_count):
            max_heap.insert(value)

        result = _get_sorted_by_extracting(max_heap)
        assert all(result[i] > result[i + 1] for i in range(len(result) - 1))

    def test_inserting(self) -> None:
        items_count = 100
        max_heap = my_heap.MaxHeap(
            random.sample(list(range(items_count)), items_count))

        max_heap.insert(101)
        assert max_heap.get_highest() == 101

        max_heap.insert(100)
        assert max_heap.get_highest() == 101

        max_heap.extract_highest()
        assert max_heap.get_highest() == 100


class FibonacciHeapTestCase(unittest.TestCase):

    def test_empty_heap(self) -> None:
        heap = my_heap.MaxFibonacciHeap()
        assert not heap.extract_highest()

    def test_sort_desc(self) -> None:
        heap = my_heap.MaxFibonacciHeap()
        items_count = 100
        for value in random.sample(list(range(items_count)), items_count):
            heap.insert(my_heap.FibonacciHeapNode(value))

        target = _get_sorted_by_extracting(heap)
        assert all(target[i] > target[i + 1] for i in range(len(target) - 1))

    def test_sort_asc(self) -> None:
        heap = my_heap.MinFibonacciHeap()
        items_count = 100
        for value in random.sample(list(range(items_count)), items_count):
            heap.insert(my_heap.FibonacciHeapNode(value))

        target = _get_sorted_by_extracting(heap)
        assert all(target[i] < target[i + 1] for i in range(len(target) - 1))

    def test_union(self) -> None:
        heap1 = my_heap.MinFibonacciHeap()
        heap2 = my_heap.MinFibonacciHeap()
        items_count = 100

        count = 0
        for value in random.sample(list(range(items_count)), items_count):
            if count < items_count / 2:
                heap1.insert(my_heap.FibonacciHeapNode(value))
            else:
                heap2.insert(my_heap.FibonacciHeapNode(value))
            count += 1

        target_heap = my_heap.MinFibonacciHeap.union(heap1, heap2)
        assert len(target_heap) == 100

        target_list = _get_sorted_by_extracting(target_heap)
        assert len(target_list) == 100

        assert all(target_list[i] < target_list[i + 1] for i in range(100 - 1))

    def test_decrease(self) -> None:
        heap = my_heap.MinFibonacciHeap()
        items_count = 1000
        self._extract_promote_sequences(heap, items_count)

        target = _get_sorted_by_extracting(heap)
        for i in range(len(target) - 1):
            if target[i] > target[i + 1]:
                msg = 'Value %d is bigger than %s' % (target[i], target[i + 1])
                self.fail(msg)

    def test_increase(self) -> None:
        heap = my_heap.MaxFibonacciHeap()
        items_count = 1000
        self._extract_promote_sequences(heap, items_count)

        target = _get_sorted_by_extracting(heap)
        for i in range(len(target) - 1):
            if target[i] < target[i + 1]:
                msg = 'Value %d is less than %s' % (target[i], target[i + 1])
                self.fail(msg)

    def test_delete(self) -> None:
        heap = my_heap.MaxFibonacciHeap()
        items_count = 1000
        values = random.sample(list(range(items_count)), items_count)
        nodes_collection = [my_heap.FibonacciHeapNode(i) for i in values]
        for node in nodes_collection:
            heap.insert(node)

        target_index = math.floor(items_count / random.randint(0, items_count))
        target_node = nodes_collection[target_index]
        heap.delete(target_node)

        target_list = _get_sorted_by_extracting(heap)
        assert target_list.count(target_node._key) == 0

    def _extract_promote_sequences(self, heap, items_count):
        values = random.sample(list(range(items_count)), items_count)
        nodes_collection = [my_heap.FibonacciHeapNode(i) for i in values]
        for node in nodes_collection:
            heap.insert(node)
        extract = True
        extracted_nodes = list()
        for node in nodes_collection:
            if extract:
                extracted = heap._extract_highest_node()
                extracted_nodes.append(extracted)
                extract = False
            elif extracted_nodes.count(node) == 0:
                level = random.randint(1, items_count)
                heap.promote_key(node, heap._promote_value(node._key, level))
                extract = True


def _get_sorted_by_extracting(heap: my_heap.AbstractHeap) -> list:
    target_list = []
    max_item = heap.extract_highest()
    while max_item is not None:
        target_list.append(max_item)
        max_item = heap.extract_highest()
    return target_list


if __name__ == '__main__':
    unittest.main()
