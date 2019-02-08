import unittest

import algabra.algorithms.graph as graphsalgs
import algabra.datastructures.graph as mygraph


class BreadthFirstSearchTestCase(unittest.TestCase):

    def test_search_shortest_path(self) -> None:
        graph = mygraph.AdjacencyListGraph()
        vertices_count = 100
        expected_path = [14, 8, 10, 2, 43, 25, 55, 53, 5, 13]
        vertices = [graphsalgs.BFSVertex(key) for key in range(vertices_count)]
        for vertex_row in vertices:
            graph.add_vertex(vertex_row)
            for vertex_column in vertices:
                row_excluded = vertex_row.get_key() in expected_path
                col_excluded = vertex_column.get_key() in expected_path
                edge_excluded = row_excluded or col_excluded
                if vertex_row != vertex_column and not edge_excluded:
                    graph.add_edge(vertex_row, vertex_column)

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

    def test_vertex_stack_filo(self) -> None:
        expected = [1, 2]
        target = graphsalgs.VertexStack()
        for i in expected:
            target.push(graphsalgs.BFSVertex(i))

        expected.reverse()
        for i in expected:
            assert i == target.pop()._key

        assert target.is_empty()


if __name__ == '__main__':
    unittest.main()
