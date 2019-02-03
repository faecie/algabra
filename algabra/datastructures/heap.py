from __future__ import annotations

import abc
import math
import typing

import scipy.constants


class AbstractHeap(abc.ABC):

    @abc.abstractmethod
    def get_highest(self) -> int:
        pass

    @abc.abstractmethod
    def extract_highest(self):
        pass

    @abc.abstractmethod
    def promote_key(self, element, new_value: int) -> None:
        old_value = self.get_value(element)
        if not self._is_higher(new_value, old_value):
            raise TypeError(
                'New value %d must be higher in a priority than old value %d' %
                (new_value, old_value))

    @abc.abstractmethod
    def insert(self, value) -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def _is_higher(cls, one, other) -> bool:
        pass

    @abc.abstractmethod
    def get_value(self, item):
        pass


class Heap(AbstractHeap):
    __slots__ = '_heap', '_heap_size'

    def __init__(self, input_data: typing.Iterable[int]) -> None:
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
    def get_sorted_list(cls, unsorted_list: typing.Iterable[int]) -> list:
        inner_heap = cls(unsorted_list)
        for index in range(len(inner_heap._heap) - 1, 0, -1):
            inner_heap._swap(0, index)
            inner_heap._heap_size -= 1
            inner_heap._heapify(0)

        return inner_heap._heap

    def get_highest(self) -> int:
        return self._heap[0]

    def extract_highest(self) -> typing.Optional[int]:
        if self._heap_size < 1:
            return None
        result = self._heap[0]
        self._heap[0] = self._heap[self._heap_size - 1]
        self._heap_size -= 1
        self._heapify(0)

        return result

    def promote_key(self, index: int, new_value: int) -> None:
        super().promote_key(index, new_value)

        self._heap[index] = new_value
        self._sift_up(index)

    def insert(self, value: int) -> None:
        self._heap_size += 1
        self._heap.append(value)
        self._sift_up(self._heap_size - 1)

    def get_value(self, item: int) -> int:
        return self._heap[item]

    def _sift_up(self, index: int) -> None:
        while index > 0 and not self._index_higher(self._parent(index), index):
            parent = self._parent(index)
            self._swap(parent, index)
            index = parent

    def _heapify(self, index: int) -> None:
        iterate = True
        while iterate:
            left = self._left(index)
            right = self._right(index)
            highest = index

            if self._in_heap(left) and self._index_higher(left, index):
                highest = left

            if self._in_heap(right) and self._index_higher(right, highest):
                highest = right

            if highest != index:
                self._swap(highest, index)
                index = highest
            else:
                iterate = False

    def _index_higher(self, one: int, other: int) -> bool:
        return self._is_higher(self._heap[one], self._heap[other])

    def _in_heap(self, index: int) -> bool:
        return index < self._heap_size

    def _swap(self, first: int, second: int) -> None:
        first_value = self._heap[first]
        self._heap[first] = self._heap[second]
        self._heap[second] = first_value


class MaxHeap(Heap):

    @classmethod
    def _is_higher(cls, one: int, other: int) -> bool:
        return one > other


class MinHeap(Heap):

    @classmethod
    def _is_higher(cls, one: int, other: int) -> bool:
        return one < other


class FibonacciHeap(AbstractHeap, typing.Sized):
    __slots__ = '_highest', '_nodes_count'

    def __init__(self, node: FibonacciHeapNode = None) -> None:
        self._highest = node
        self._nodes_count = 0

    def __len__(self) -> int:
        return self._nodes_count

    @classmethod
    def _is_higher(cls, one: typing.Union[FibonacciHeapNode, int, None],
                   other: typing.Union[FibonacciHeapNode, int, None]) -> bool:
        if one is None or other is None:
            return False

        one = one._key if isinstance(one, FibonacciHeapNode) else one
        other = other._key if isinstance(other, FibonacciHeapNode) else other

        return cls._is_value_higher(one, other)

    @staticmethod
    @abc.abstractmethod
    def _is_value_higher(one: int, other: int) -> bool:
        pass

    @abc.abstractmethod
    def _promote_value(self, key: int, level: typing.Optional[int] = 1) -> int:
        pass

    @staticmethod
    def _remove_from_root_list(node: FibonacciHeapNode):
        node._left._right = node._right
        node._right._left = node._left

        node._left = node._right = None

    @staticmethod
    def _exchange_roots(one: FibonacciHeapNode,
                        other: FibonacciHeapNode) -> None:
        other_around_one = one._left == other and one._right == other
        one_around_other = other._left == one and other._right == one
        if other_around_one != one_around_other:
            raise Exception(
                'List is broken on nodes %d and %d' % (one._key, other._key))

        if one == other or other_around_one:
            return

        one_adjacent_other = one._right == other and other._left == one
        other_adjacent_one = one._left == other and other._right == one
        are_adjacent = one_adjacent_other or other_adjacent_one

        if other._right == one:
            one, other = other, one

        swapper_vector = one._left, other._left, one._right, other._right

        if are_adjacent:
            one._left = swapper_vector[2]
            other._left = swapper_vector[0]
            one._right = swapper_vector[3]
            other._right = swapper_vector[1]
        else:
            one._left = swapper_vector[1]
            other._left = swapper_vector[0]
            one._right = swapper_vector[3]
            other._right = swapper_vector[2]

        one._left._right = one
        one._right._left = one
        other._left._right = other
        other._right._left = other

    @classmethod
    def union(cls, one: FibonacciHeap, other: FibonacciHeap) -> FibonacciHeap:
        result = cls()
        result._highest = one._highest

        result._merge_with_root(other)
        if cls._is_higher(other._highest, one._highest):
            result._highest = other._highest

        result._nodes_count = one._nodes_count + other._nodes_count

        return result

    def insert(self, node: FibonacciHeapNode):
        node._degree = 0
        node._parent = None
        node._child = None
        node._mark = False

        self._insert_in_root_list(node)

        self._nodes_count += 1

    def get_highest(self) -> int:
        return self._highest._key

    def _extract_highest_node(self) -> typing.Optional[FibonacciHeapNode]:
        result = self._highest
        if result is not None:
            child = result._child
            terminal = False
            while child is not None and not terminal:
                terminal = child._right == child
                next_child = child._right
                result._remove_child(child)
                self._insert_in_root_list(child)
                child._parent = None
                child = next_child

            next_root = result._right
            self._remove_from_root_list(result)

            if result == next_root:
                self._highest = None
            else:
                self._highest = next_root
                self._consolidate()
            self._nodes_count -= 1

        return None if result is None else result

    def extract_highest(self) -> typing.Optional[int]:
        result = self._extract_highest_node()

        return None if result is None else result._key

    def promote_key(self, node: FibonacciHeapNode, new_value: int) -> None:
        super().promote_key(node, new_value)

        node._key = new_value

        parent = node._parent
        if parent is not None and self._is_higher(node, parent):
            node._mark = True
            self._cut(node)

        if self._is_higher(node, self._highest):
            self._highest = node

    def delete(self, node: FibonacciHeapNode) -> None:
        if self._highest is not None:
            self.promote_key(node, self._promote_value(self._highest._key))
            self.extract_highest()

    def get_value(self, node: FibonacciHeapNode) -> typing.Optional[int]:
        return None if node is None else node._key

    def _cut(self, node: FibonacciHeapNode) -> None:
        target = node
        parent = target._parent
        iterate = True
        while parent and iterate:
            if target._mark:
                parent._remove_child(target)
                self._insert_in_root_list(target)
                target._mark = False
                target = parent
                parent = parent._parent
            else:
                target._mark = True
                iterate = False

    def _consolidate(self) -> None:
        nodes_per_degree = [None] * self._get_max_degrees_count()

        terminal = False
        next_node = self._highest
        while next_node != terminal and next_node is not None:
            terminal = next_node if not terminal else terminal
            degree = next_node._degree
            while nodes_per_degree[degree] is not None:
                same_degree_node = nodes_per_degree[degree]

                if self._is_higher(same_degree_node, next_node):
                    if terminal == same_degree_node:
                        terminal = same_degree_node._right
                    self._exchange_roots(next_node, same_degree_node)
                    next_node, same_degree_node = same_degree_node, next_node

                if terminal == same_degree_node:
                    terminal = same_degree_node._right
                self._remove_from_root_list(same_degree_node)
                next_node._add_child(same_degree_node)
                same_degree_node._mark = False

                nodes_per_degree[degree] = None
                degree += 1

            nodes_per_degree[degree] = next_node
            next_node = next_node._right

        self._highest = None
        for node in nodes_per_degree:
            if node is not None:
                self._insert_in_root_list(node)

    def _get_max_degrees_count(self) -> int:
        return math.floor(math.log(self._nodes_count, scipy.constants.golden))

    def _insert_in_root_list(self, node: FibonacciHeapNode):
        node._parent = None
        if self._highest is not None:
            self._highest.add_neighbour(node)
            if self._is_higher(node, self._highest):
                self._highest = node
        else:
            self._highest = node
            node._left = node._right = node

    def _merge_with_root(self, other_root: FibonacciHeap) -> None:
        if other_root._highest is not None:
            if self._highest is not None:
                self_right_neighbor = self._highest._right
                self._highest._right = other_root._highest._right
                other_root._highest._right._left = self._highest

                other_root._highest._right = self_right_neighbor
                self_right_neighbor._left = other_root._highest
            else:
                self._highest = other_root._highest


class FibonacciHeapNode:
    __slots__ = [
        '_degree',
        '_mark',
        '_parent',
        '_child',
        '_left',
        '_right',
        '_key',
    ]

    def __init__(self,
                 key: int,
                 parent: FibonacciHeapNode = None,
                 child: FibonacciHeapNode = None) -> None:
        self._left = self._right = self
        self._key = key
        self._degree = 0
        self._mark = False
        self._child = child
        self._parent = parent

    def add_neighbour(self, node: FibonacciHeapNode) -> None:
        node._right, node._left = self._right, self

        self._right._left = node
        self._right = node

        node._parent = self._parent

    def _remove_child(self, node: FibonacciHeapNode) -> None:
        if node._parent != self or self._child is None:
            raise ValueError('%d has not a child %d' % (self._key, node._key))

        if self._child == node and node._right == node._left == node:
            self._child = None
        else:
            node._left._right, node._right._left = node._right, node._left
            self._child = node._right

        node._right = node._left = node._parent = None

        self._degree -= 1

    def _add_child(self, node: FibonacciHeapNode) -> None:
        if self._child is None:
            self._child = node
            node._right = node._left = node
            node._parent = self
        else:
            self._child.add_neighbour(node)

        self._degree += 1


class MinFibonacciHeap(FibonacciHeap):

    @staticmethod
    def _is_value_higher(one: int, other: int) -> bool:
        return one < other

    def _promote_value(self, key: int, level: typing.Optional[int] = 1) -> int:
        return key - level


class MaxFibonacciHeap(FibonacciHeap):

    @staticmethod
    def _is_value_higher(one: int, other: int) -> bool:
        return one > other

    def _promote_value(self, key: int, level: typing.Optional[int] = 1) -> int:
        return key + level
