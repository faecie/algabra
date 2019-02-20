import unittest

import algabra.algorithms.trees as trees


class SwapNodesAlgoTestCase(unittest.TestCase):
    """
        Swap Nodes [Algo]

        You are given a tree of n nodes where nodes are indexed from [1..n]
        and it is rooted at 1. You have to perform t swap operations on it,
        and after each swap operation print the in-order traversal of
        the current state of the tree.

        @link: https://www.hackerrank.com/challenges/swap-nodes-algo
    """

    def test_sample_input_0(self) -> None:
        """
             1   [s]        1    [s]       1
           / \      ->   / \        ->  / \
          2   3 [s]     3   2  [s]     2   3
        """

        indexes = [[2, 3], [-1, -1], [-1, -1]]
        queries = [1, 1]

        result = []
        tree = trees.Tree.build_tree(indexes)
        for coeff in queries:
            tree.swap(coeff)
            result.append([i for i in tree.traverse_inorder()])

        assert [[3, 1, 2], [2, 1, 3]] == result

    def test_sample_input_1(self) -> None:
        indexes = [
            [2, 3], [4, 5], [6, -1], [-1, 7], [8, 9], [10, 11], [12, 13],
            [-1, 14], [-1, -1], [15, -1], [16, 17], [-1, -1], [-1, -1],
            [-1, -1], [-1, -1], [-1, -1], [-1, -1]
        ]
        queries = [2, 3]

        result = []
        tree = trees.Tree.build_tree(indexes)
        for coeff in queries:
            tree.swap(coeff)
            result.append([i for i in tree.traverse_inorder()])

        expected = [
            [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3, 10, 15, 6, 17, 11, 16],
            [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3, 17, 11, 16, 6, 10, 15]
        ]

        assert expected == result

    def test_sample_input_2(self) -> None:
        indexes = [
            [2, 3], [4, -1], [5, -1], [6, -1], [7, 8], [-1, 9], [-1, -1],
            [10, 11], [-1, -1], [-1, -1], [-1, -1],
        ]
        queries = [2, 4]

        result = []
        tree = trees.Tree.build_tree(indexes)
        for coeff in queries:
            tree.swap(coeff)
            result.append([i for i in tree.traverse_inorder()])

        expected = [
            [2, 9, 6, 4, 1, 3, 7, 5, 11, 8, 10],
            [2, 6, 9, 4, 1, 3, 7, 5, 10, 8, 11],
        ]

        assert expected == result

    def test_swap(self) -> None:
        indexes = [[1, 2], [-1, 3], [4, -1], [-1, -1], [2, -1], [-1, -1]]
        tree = trees.Tree.build_tree(indexes)
        tree.swap(2)

        assert tree.root.left.left.key == 3
        assert tree.root.right.right.left.key == 2

    def test_build_tree(self) -> None:
        indexes = [[1, 2], [-1, 3], [4, -1], [-1, -1], [2, -1], [-1, -1]]
        tree = trees.Tree.build_tree(indexes)

        assert isinstance(tree.root.right.right, trees.SentinelNode)
        assert tree.root.left.right.key == 3
        assert isinstance(tree.root.left.right.left, trees.SentinelNode)
        assert isinstance(tree.root.left.right.left, trees.SentinelNode)
        assert tree.root.right.left.left.key == 2
        assert isinstance(tree.root.right.left.left.left,
                          trees.SentinelNode)


if __name__ == '__main__':
    unittest.main()
