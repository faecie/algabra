import abc
import math
import typing


class Heap(abc.ABC):
    __slots__ = ['_heap', '_heap_size']

    def __init__(self, input_data: typing.Iterable) -> None:
        self._heap = list(input_data)
        self._heap_size = len(self._heap)

        for index in range(math.floor((self._heap_size - 1) / 2), -1, -1):
            self._heapify(index)

    @staticmethod
    def _parent(index: int) -> int:
        return math.floor((index - 1) / 2)

    @staticmethod
    def _left(index: int) -> int:
        return 2 * index + 1

    @staticmethod
    def _right(index: int) -> int:
        return 2 * index + 2

    @classmethod
    def get_sorted_list(cls, unsorted_list: typing.Iterable) -> list:
        inner_heap = cls(unsorted_list)
        for index in range(len(inner_heap._heap) - 1, 0, -1):
            inner_heap._swap(0, index)
            inner_heap._heap_size -= 1
            inner_heap._heapify(0)

        return inner_heap._heap

    @abc.abstractmethod
    def _is_higher(self, one: int, other: int) -> bool:
        pass

    def _heapify(self, index: int) -> None:
        iterate = True
        while iterate:
            left = self._left(index)
            right = self._right(index)
            highest = index

            if self._in_heap(left) and self._is_higher(left, index):
                highest = left

            if self._in_heap(right) and self._is_higher(right, highest):
                highest = right

            if highest != index:
                self._swap(highest, index)
                index = highest
            else:
                iterate = False

    def _in_heap(self, index: int) -> bool:
        return index < self._heap_size

    def _swap(self, first: int, second: int) -> None:
        first_value = self._heap[first]
        self._heap[first] = self._heap[second]
        self._heap[second] = first_value


class MaxHeap(Heap):

    def _is_higher(self, one: int, other: int) -> bool:
        return self._heap[one] > self._heap[other]


class MinHeap(Heap):

    def _is_higher(self, one: int, other: int) -> bool:
        return self._heap[one] < self._heap[other]
