import unittest

import algabra.algorithms.unionfind as uf


class ConnectedCellsTestCase(unittest.TestCase):
    def test_connected_cell_0(self):
        count = uf.connected_cell([
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [1, 0, 0, 0],
        ])

        assert count == 5

    def test_connected_cell_6(self):
        count = uf.connected_cell([
            [0, 1, 0, 0, 0, 0, 1, 1, 0],
            [1, 1, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 1],
            [0, 1, 1, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0],
        ])

        assert count == 29



if __name__ == '__main__':
    unittest.main()
