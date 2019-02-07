import abc
import unittest

import algabra.datastructures.graph as my_graph


class BaseGraphTestCase(abc.ABC):

    def test_empty_graph(self) -> None:
        graph = self._get_graph()
        vertex = graph.get_vertex(1)

        assert vertex is None

    def test_add_vertices(self) -> None:
        graph = self._get_graph()
        graph.add_vertex(my_graph.Vertex(1))
        graph.add_vertex(my_graph.Vertex(5))

        vertex = graph.get_vertex(5)

        assert vertex.get_key() == 5

    def test_add_edges(self) -> None:
        graph = self._get_graph()
        vertex1 = my_graph.Vertex(1)
        vertex2 = my_graph.Vertex(7)
        vertex3 = my_graph.Vertex(5)

        graph.add_edge(vertex1, vertex3)
        graph.add_edge(vertex2, vertex1)
        graph.add_edge(vertex2, vertex3)
        graph.add_edge(vertex3, vertex2)

        assert graph.vertex_has_edge_with(vertex3, vertex2)
        assert graph.vertex_has_edge_with(vertex2, vertex3)
        assert not graph.vertex_has_edge_with(vertex3, vertex1)

    def test_wrong_vertex(self) -> None:
        graph = self._get_graph()
        vertex = my_graph.Vertex(1)
        graph.add_vertex(vertex)
        wrong_vertex = my_graph.Vertex(1)

        graph.add_edge(wrong_vertex, my_graph.Vertex(666))

    def test_wrong_edge(self) -> None:
        graph = self._get_graph()
        vertex = my_graph.Vertex(1)
        graph.add_vertex(vertex)
        wrong_vertex = my_graph.Vertex(1)

        graph.add_edge(my_graph.Vertex(666), wrong_vertex)

    @abc.abstractmethod
    def _get_graph(self) -> my_graph.GraphInterface:
        pass


class AdjacencyListGraphTestCase(BaseGraphTestCase, unittest.TestCase):

    def _get_graph(self) -> my_graph.GraphInterface:
        return my_graph.AdjacencyListGraph()

    def test_wrong_vertex(self) -> None:
        with self.assertRaises(my_graph.WrongVertexException):
            super().test_wrong_vertex()

    def test_wrong_edge(self) -> None:
        with self.assertRaises(my_graph.WrongVertexException):
            super().test_wrong_edge()


class AdjacencyMatrixGraphTestCase(BaseGraphTestCase, unittest.TestCase):

    def _get_graph(self) -> my_graph.GraphInterface:
        return my_graph.AdjacencyMatrixGraph()

    def test_wrong_vertex(self) -> None:
        with self.assertRaises(my_graph.WrongVertexException):
            super().test_wrong_vertex()

    def test_wrong_edge(self) -> None:
        with self.assertRaises(my_graph.WrongVertexException):
            super().test_wrong_edge()


if __name__ == '__main__':
    unittest.main()
