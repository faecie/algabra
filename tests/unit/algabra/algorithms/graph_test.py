import typing
import unittest

import algabra.algorithms.graph as graphsalgs
import algabra.datastructures.graph as mygraph


def _connect_every_vertex(graph: mygraph.GraphInterface,
                          vertices: typing.List[mygraph.Vertex],
                          exclusions: typing.List[int] = None) -> None:
    exclusions = [] if exclusions is None else exclusions
    for vertex_row in vertices:
        graph.add_vertex(vertex_row)
        for vertex_column in vertices:
            row_excluded = vertex_row.get_key() in exclusions
            col_excluded = vertex_column.get_key() in exclusions
            edge_excluded = row_excluded or col_excluded
            if vertex_row != vertex_column and not edge_excluded:
                graph.add_edge(vertex_row, vertex_column)


def _connect_components(graph: mygraph.AdjacencyListGraph,
                        components: typing.List[
                            typing.Sequence[mygraph.Vertex]
                        ]) -> None:
    for component in components:
        previous_key = None
        for key in component:
            if previous_key is not None:
                graph.add_edge(previous_key, key)

            previous_key = key


class BreadthFirstSearchTestCase(unittest.TestCase):

    def test_search_shortest_path(self) -> None:
        graph = mygraph.AdjacencyListGraph()
        vertices_count = 100
        expected_path = [14, 8, 10, 2, 43, 25, 55, 53, 5, 13]
        vertices = [graphsalgs.BFSVertex(key) for key in range(vertices_count)]
        _connect_every_vertex(graph, vertices, expected_path)

        expected_path[len(expected_path):len(expected_path) + 1] = [19, 3]
        expected_path.reverse()
        previous_point = None
        for point in expected_path:
            if previous_point is not None:
                graph.add_edge(
                    graph.get_vertex(previous_point), graph.get_vertex(point))
            previous_point = point

        shortest_path = graphsalgs.shortest_path(graph, graph.get_vertex(3),
                                                 graph.get_vertex(14))
        target_path = [v.get_key() for v in shortest_path]
        assert target_path == expected_path

        no_path = graphsalgs.shortest_path(graph, graph.get_vertex(2),
                                           graph.get_vertex(54))
        assert no_path.is_empty()

    def test_one_node_route(self) -> None:
        graph = mygraph.AdjacencyListGraph()
        vertex = graphsalgs.BFSVertex(2)
        graph.add_vertex(graphsalgs.BFSVertex(2))

        target = graphsalgs.shortest_path(graph, vertex, vertex)
        target_path = [target.pop().get_key()]

        assert target.is_empty()
        assert target_path == [2]

    def test_vertex_queue_fifo(self) -> None:
        expected = [1, 2]
        target = graphsalgs.VertexQueue()
        for i in expected:
            target.queue(graphsalgs.BFSVertex(i))

        for i in expected:
            assert i == target.deque()._key

        assert target.is_empty()

    def test_vertex_stack_lifo(self) -> None:
        expected = [1, 2]
        target = graphsalgs.VertexStack()
        for i in expected:
            target.push(graphsalgs.BFSVertex(i))

        expected.reverse()
        for i in expected:
            assert i == target.pop()._key

        assert target.is_empty()


class DepthFirstSearchTestCase(unittest.TestCase):

    def test_depth_first_search(self) -> None:
        graph = mygraph.AdjacencyListGraph()
        vertices_count = 10
        vertices = [graphsalgs.DFSVertex(key) for key in range(vertices_count)]
        _connect_every_vertex(graph, vertices, [3])
        graphsalgs.depth_first_search(graph)

        assert graph.get_vertex(3).ascendant is None
        assert graph.get_vertex(5).ascendant is not None
        assert graph.get_vertex(6).ascendant.begin < graph.get_vertex(2).begin
        assert graph.get_vertex(6).ascendant.end > graph.get_vertex(2).end

    def test_topological_sort_fails_with_cycles(self) -> None:
        graph = mygraph.AdjacencyListGraph()

        v = [graphsalgs.DFSVertex(key) for key in (0, 1, 2, 3, 4, 5)]
        _connect_components(graph, [
            (v[0], v[1]),
            (v[1], v[2], v[3]),
            (v[3], v[2], v[4], v[5]),
        ])

        with self.assertRaises(RuntimeError):
            graphsalgs.topological_sort(graph)

    def test_topological_sort(self) -> None:
        graph = mygraph.AdjacencyListGraph()
        v = [graphsalgs.DFSVertex(key) for key in (0, 1, 2, 3, 4, 5)]
        _connect_components(graph, [
            (v[1], v[2], v[3]),
            (v[0], v[3]),
            (v[4], v[5], v[3]),
        ])

        target_keys = graphsalgs.topological_sort(graph)
        assert [4, 5, 0, 1, 2, 3] == target_keys


if __name__ == '__main__':
    unittest.main()
