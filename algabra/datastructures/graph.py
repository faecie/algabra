from __future__ import annotations

import abc
import typing


class GraphInterface(abc.ABC):

    @abc.abstractmethod
    def add_vertex(self, vertex: Vertex) -> None:
        pass

    @abc.abstractmethod
    def get_vertex(self, key: int) -> typing.Optional[Vertex]:
        pass

    @abc.abstractmethod
    def add_edge(self, vertex_from: Vertex, vertex_to: Vertex) -> None:
        pass

    @abc.abstractmethod
    def vertex_has_edge_with(self, vertex: Vertex, target: Vertex) -> bool:
        pass


class AdjacencyListGraph(GraphInterface, typing.Iterable):
    __slots__ = ['_vertices']

    def __init__(self) -> None:
        self._vertices = dict()

    def __iter__(self) -> typing.Iterator[Vertex]:
        for vertex in self._vertices:
            yield vertex

    def add_vertex(self, vertex: Vertex) -> None:
        key = vertex.get_key()
        if key not in self._vertices:
            self._vertices[key] = AdjacentVerticesList(vertex)

    def get_vertex(self, key: int) -> typing.Optional[Vertex]:
        if key in self._vertices:
            return self._vertices[key].get_vertex()
        else:
            return None

    def add_edge(self, vertex_from: Vertex, vertex_to: Vertex) -> None:
        vertex_froms_edges = self._require_edges(vertex_from)
        self._require_edges(vertex_to)

        vertex_froms_edges.add_adjacent(vertex_to)

    def vertex_has_edge_with(self, vertex: Vertex, target: Vertex) -> bool:
        vertex_edges = self.get_edges(vertex)

        if vertex_edges is not None:
            return vertex_edges.has_edge_with(target)

        return False

    def get_edges(self,
                  vertex: Vertex) -> typing.Optional[AdjacentVerticesList]:
        if vertex.get_key() in self._vertices:
            return self._vertices[vertex.get_key()]
        else:
            return None

    def _require_edges(self, vertex: Vertex) -> AdjacentVerticesList:
        result = self.get_edges(vertex)
        if result is not None and result.get_vertex() != vertex:
            raise WrongVertexException(vertex)
        if result is None:
            self.add_vertex(vertex)
            result = self.get_edges(vertex)

        return result


class AdjacencyMatrixGraph(GraphInterface):
    __slots__ = ['_vertices', '_edges']

    def __init__(self) -> None:
        self._vertices = dict()
        self._edges = dict()

    def add_vertex(self, vertex: Vertex) -> None:
        self._edges[vertex.get_key()] = dict()
        for key in self._vertices.keys():
            self._edges[key][vertex.get_key()] = False
            self._edges[vertex.get_key()][key] = False

        self._vertices[vertex.get_key()] = vertex

    def get_vertex(self, key: int) -> typing.Optional[Vertex]:
        return self._vertices[key] if key in self._vertices else None

    def add_edge(self, vertex_from: Vertex, vertex_to: Vertex) -> None:
        self._require_vertex(vertex_to)
        self._require_vertex(vertex_from)

        self._edges[vertex_from.get_key()][vertex_to.get_key()] = True

    def vertex_has_edge_with(self, vertex: Vertex, target: Vertex) -> bool:
        vertex_key = vertex.get_key()
        target_key = target.get_key()
        if vertex_key in self._edges and target_key in self._edges[vertex_key]:
            return self._edges[vertex_key][target_key]

        return False

    def _require_vertex(self, vertex: Vertex) -> Vertex:
        result = self.get_vertex(vertex.get_key())
        if result is not None and result != vertex:
            raise WrongVertexException(vertex)

        if result is None:
            self.add_vertex(vertex)
            result = self.get_vertex(vertex.get_key())

        return result


class Vertex:
    __slots__ = '_key'

    def __init__(self, key: int) -> None:
        self._key = key

    def get_key(self):
        return self._key


class AdjacentVerticesList(typing.Iterable):
    __slots__ = '_sentinel', '_master_vertex'

    def __init__(self, vertex: Vertex) -> None:
        self._master_vertex = vertex
        self._sentinel = SentinelEdge(vertex)

    def __iter__(self):
        next_vertex = self._sentinel._next

        while not isinstance(next_vertex, SentinelEdge):
            yield next_vertex

            next_vertex = next_vertex._next

    def get_vertex(self) -> Vertex:
        return self._master_vertex

    def add_adjacent(self, vertex: Vertex) -> None:
        if not self.has_edge_with(vertex):
            new_edge = Edge(vertex)
            new_edge._prev, new_edge._next = self._sentinel._prev, self._sentinel
            self._sentinel._prev._next = new_edge
            self._sentinel._prev = new_edge

    def has_edge_with(self, vertex: Vertex) -> bool:
        for edge in self:
            if edge.get_vertex() == vertex:
                return True

        return False


class Edge:
    __slots__ = ['_vertex', '_prev', '_next']

    def __init__(self, vertex: Vertex) -> None:
        self._vertex = vertex

    def get_vertex(self) -> Vertex:
        return self._vertex


class SentinelEdge(Edge):

    def __init__(self, vertex: Vertex) -> None:
        super().__init__(vertex)
        self._next = self._prev = self


class WrongVertexException(Exception):

    def __init__(self, vertex: Vertex) -> None:
        super().__init__('Vertex with key: %s, %s is not in a graph' %
                         (vertex.get_key(), repr(vertex)))
