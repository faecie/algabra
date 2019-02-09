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


def depth_first_search(graph: mygraph.AdjacencyListGraph,
                       vertex_visitor: typing.Optional[VertexVisitor] = None,
                       edge_visitor: typing.Optional[EdgeVisitor] = None
                       ) -> None:
    if vertex_visitor is None:
        vertex_visitor = VertexVisitor()
    if edge_visitor is None:
        edge_visitor = EdgeVisitor()

    order = 0
    ascendants = VertexStack()
    descendants = VertexStack()

    for vertex in graph:
        if vertex.color == Color.WHITE:
            descendants.push(vertex)

        while not descendants.is_empty():
            order += 1
            descendant = descendants.pop()
            descendant.begin = order
            vertex_visitor.start_visiting(descendant)

            for edge in graph.get_edges(descendant):
                edge_visitor.visit(edge)
                if edge.get_vertex().color == Color.WHITE:
                    edge.get_vertex().ascendant = descendant
                    descendants.push(edge.get_vertex())

            ascendants.push(descendant)

        while not ascendants.is_empty():
            order += 1
            ascendant = ascendants.pop()
            ascendant.end = order
            vertex_visitor.stop_visiting(ascendant)


def topological_sort(graph: mygraph.AdjacencyListGraph) -> typing.List[int]:
    vertex_visitor = TopologicalSortVertexVisitor()
    edge_visitor = DAGEdgeVisitor()
    depth_first_search(graph, vertex_visitor, edge_visitor)
    return [vertex.get_key() for vertex in vertex_visitor.get_sorted()]


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


class DFSVertex(mygraph.Vertex):
    __slots__ = 'color', 'begin', 'end', 'ascendant'

    def __init__(self,
                 key: int,
                 color: Color = Color.WHITE,
                 begin: typing.Optional[int] = None,
                 end: typing.Optional[int] = None,
                 ascendant: typing.Optional[mygraph.Vertex] = None) -> None:
        super().__init__(key)
        self.ascendant = ascendant
        self.begin = begin
        self.end = end
        self.color = color


class VertexVisitor:
    def start_visiting(self, vertex: DFSVertex) -> None:
        vertex.color = Color.GREY

    def stop_visiting(self, vertex: DFSVertex) -> None:
        vertex.color = Color.BLACK


class EdgeVisitor:
    def visit(self, edge: mygraph.Edge) -> None:
        return


class DAGEdgeVisitor(EdgeVisitor):

    def visit(self, edge: mygraph.Edge) -> None:
        super().visit(edge)
        vertex = edge.get_vertex()
        if vertex.color == Color.GREY:
            raise RuntimeError(
                'Vertex %s has cycle reference.' % vertex.get_key())


class TopologicalSortVertexVisitor(VertexVisitor):
    __slots__ = '_vertex_stack'

    def __init__(self) -> None:
        super().__init__()
        self._vertex_stack = VertexStack()

    def stop_visiting(self, vertex: DFSVertex) -> None:
        super().stop_visiting(vertex)
        self._vertex_stack.push(vertex)

    def get_sorted(self) -> typing.Iterator[DFSVertex]:
        while not self._vertex_stack.is_empty():
            yield self._vertex_stack.pop()


class VertexQueue:
    __slots__ = '_dequeue', '_size'

    def __init__(self) -> None:
        self._dequeue = collections.deque()
        self._size = 0

    def deque(self) -> typing.Union[BFSVertex, DFSVertex, mygraph.Vertex]:
        result = self._dequeue.popleft()
        self._size -= 1

        return result

    def queue(self,
              item: typing.Union[BFSVertex, DFSVertex, mygraph.Vertex]) -> None:
        self._dequeue.append(item)
        self._size += 1

    def is_empty(self) -> bool:
        return self._size == 0


class VertexStack(typing.Iterable):
    __slots__ = '_dequeue', '_size'

    def __init__(self) -> None:
        self._dequeue = collections.deque()
        self._size = 0

    def __iter__(self) -> typing.Iterator[
        typing.Union[BFSVertex, DFSVertex, mygraph.Vertex]]:
        while not self.is_empty():
            yield self.pop()

    def pop(self) -> typing.Union[BFSVertex, DFSVertex, mygraph.Vertex]:
        result = self._dequeue.pop()
        self._size -= 1

        return result

    def push(self,
             item: typing.Union[BFSVertex, DFSVertex, mygraph.Vertex]) -> None:
        self._dequeue.append(item)
        self._size += 1

    def is_empty(self) -> bool:
        return self._size == 0
