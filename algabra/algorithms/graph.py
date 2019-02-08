from __future__ import annotations

import collections
import enum
import typing

import algabra.datastructures.graph as mygraph


def breadth_first_search(graph: mygraph.AdjacencyListGraph,
                         start_vertex: BFSVertex) -> None:
    start_vertex.color = Color.GREY
    start_vertex.distance = 0

    search_queue = VertexQueue()
    search_queue.queue(start_vertex)

    while not search_queue.is_empty():
        vertex = search_queue.deque()

        for edge in graph.get_edges(vertex):
            if edge.get_vertex().color == Color.WHITE:
                edge.get_vertex().color = Color.GREY
                edge.get_vertex().distance = vertex.distance + 1
                edge.get_vertex().predecessor = vertex
                search_queue.queue(edge.get_vertex())

        vertex.color = Color.BLACK


def shortest_path(graph: mygraph.AdjacencyListGraph, start_from: BFSVertex,
                  to: BFSVertex) -> VertexStack:
    breadth_first_search(graph, start_from)
    path = VertexStack()

    if to == start_from:
        path.push(start_from)
        return path

    if to.predecessor is None:
        return path

    next_vertex = to
    while next_vertex != start_from:
        if next_vertex.predecessor is None:
            return VertexStack()

        path.push(next_vertex)
        next_vertex = next_vertex.predecessor
    path.push(start_from)

    return path


class VertexQueue:
    __slots__ = '_dequeue', '_size'

    def __init__(self) -> None:
        self._dequeue = collections.deque()
        self._size = 0

    def deque(self) -> BFSVertex:
        result = self._dequeue.popleft()
        self._size -= 1

        return result

    def queue(self, item: BFSVertex) -> None:
        self._dequeue.append(item)
        self._size += 1

    def is_empty(self) -> bool:
        return self._size == 0


class VertexStack(typing.Iterable):
    __slots__ = '_dequeue', '_size'

    def __init__(self) -> None:
        self._dequeue = collections.deque()
        self._size = 0

    def __iter__(self) -> typing.Iterator[BFSVertex]:
        while not self.is_empty():
            yield self.pop()

    def pop(self) -> BFSVertex:
        result = self._dequeue.pop()
        self._size -= 1

        return result

    def push(self, item: BFSVertex) -> None:
        self._dequeue.append(item)
        self._size += 1

    def is_empty(self) -> bool:
        return self._size == 0


class Color(enum.Enum):
    WHITE = 1
    GREY = 2
    BLACK = 3


class BFSVertex(mygraph.Vertex):
    __slots__ = 'color', 'distance', 'predecessor'

    def __init__(self,
                 key: int,
                 color: Color = Color.WHITE,
                 distance: typing.Optional[int] = None,
                 predecessor: typing.Optional[mygraph.Vertex] = None) -> None:
        super().__init__(key)
        self.predecessor = predecessor
        self.distance = distance
        self.color = color
