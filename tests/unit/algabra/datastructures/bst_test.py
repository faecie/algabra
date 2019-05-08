import unittest
import random

import algabra.datastructures.bst as bst


class BinarySearchTreeTestCase(unittest.TestCase):

    @staticmethod
    def create_bst(from_list: list):
        my_bst = bst.BinarySearchTree()
        for key in from_list:
            my_bst.insert(bst.Node(key))

        return my_bst

    def test_empty(self) -> None:
        my_bst = bst.BinarySearchTree()

        assert not my_bst.maximum()

    def test_inorder_traversal(self) -> None:
        sorted_list = list(range(50))
        unsorted_list = random.sample(sorted_list, 50)

        my_bst = self.create_bst(unsorted_list)

        test_list = [node.key for node in my_bst]
        assert sorted_list == test_list

    def test_insert_delete(self) -> None:
        unsorted_list = random.sample(range(500), 500)
        my_bst = self.create_bst(unsorted_list)

        for delete_key in unsorted_list[1:100]:
            bst_node = my_bst.search(delete_key)
            predecessor = my_bst.predecessor(bst_node)

            # haven't found time to find better place
            # to properly test all the cases of predecessor operation
            assert predecessor is None or predecessor.key < delete_key

            my_bst.delete(bst_node)

        result = [node.key for node in my_bst]
        assert all(result[i] < result[i + 1] for i in range(len(result) - 1))

    def test_get_maximum_minimum(self) -> None:
        unsorted_list = random.sample(range(500), 500)

        my_bst = self.create_bst(unsorted_list)
        maximum_node = my_bst.maximum()
        minimum_node = my_bst.minimum()

        assert maximum_node.key == 499
        assert minimum_node.key == 0

    def test_get_successor_predecessor(self) -> None:
        unsorted_list = random.sample(range(500), 500)
        random.shuffle(unsorted_list)

        my_bst = self.create_bst(unsorted_list)
        successor = my_bst.successor(my_bst.search(375))
        predecessor = my_bst.predecessor(my_bst.search(243))

        assert successor.key == 376
        assert predecessor.key == 242


class AVLTreeTestCase(unittest.TestCase):

    def test_insertion_left_right_case(self) -> None:
        avl = bst.AVLTree()
        keys = 10, 6, 11, 1, 8, 9
        for key in keys:
            avl.insert(bst.AVLNode(key))

        assert self._tree_is_balanced(avl)

    def test_insertion_left_case(self) -> None:
        avl = bst.AVLTree()
        keys = 10, 7, 4, 1, 5, 8, 11
        for key in keys:
            avl.insert(bst.AVLNode(key))

        assert self._tree_is_balanced(avl)

    def test_insertion_right_case(self) -> None:
        avl = bst.AVLTree()
        keys = 10, 9, 20, 15, 25, 21, 26
        for key in keys:
            avl.insert(bst.AVLNode(key))

    def test_insertion_right_left_case(self) -> None:
        avl = bst.AVLTree()
        keys = 10, 9, 20, 15, 25, 14
        for key in keys:
            avl.insert(bst.AVLNode(key))

        assert self._tree_is_balanced(avl)

    def test_deletion(self) -> None:
        avl = bst.AVLTree()
        keys = 10, 9, 20, 15, 25, 26, 14
        for key in keys:
            avl.insert(bst.AVLNode(key))

        node = avl.search(26)
        avl.delete(node)

        assert self._tree_is_balanced(avl)

    def _tree_is_balanced(self, tree: bst.AVLTree) -> bool:
        for node in tree:
            try:
                delta = abs(node.parent.left.height - node.parent.right.height)
                if delta > bst.AVLTree.MAX_HEIGHT_DELTA:
                    return False
            except AttributeError:
                pass

        return True


if __name__ == '__main__':
    unittest.main()
