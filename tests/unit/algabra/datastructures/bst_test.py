import unittest
import random

import algabra.datastructures.bst as bst


class MyTestCase(unittest.TestCase):

    def test_empty(self) -> None:
        my_bst = bst.BinarySearchTree()

        assert not my_bst.maximum()

    def test_inorder_traversal(self) -> None:
        sorted_list = list(range(50))
        unsorted_list = list(sorted_list)
        random.shuffle(unsorted_list)

        my_bst = self.create_bst(unsorted_list)

        test_list = [node.key for node in my_bst]
        assert sorted_list == test_list

    def test_insert_delete(self) -> None:
        unsorted_list = list(range(500))
        random.shuffle(unsorted_list)

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
        unsorted_list = list(range(500))
        random.shuffle(unsorted_list)

        my_bst = self.create_bst(unsorted_list)
        maximum_node = my_bst.maximum()
        minimum_node = my_bst.minimum()

        assert maximum_node.key == 499
        assert minimum_node.key == 0

    def test_get_successor_predecessor(self) -> None:
        unsorted_list = list(range(500))
        random.shuffle(unsorted_list)

        my_bst = self.create_bst(unsorted_list)
        successor = my_bst.successor(my_bst.search(375))
        predecessor = my_bst.predecessor(my_bst.search(243))

        assert successor.key == 376
        assert predecessor.key == 242

    def create_bst(self, from_list: list):
        my_bst = bst.BinarySearchTree()
        for key in from_list:
            my_bst.insert(bst.Node(key))

        return my_bst


if __name__ == '__main__':
    unittest.main()
