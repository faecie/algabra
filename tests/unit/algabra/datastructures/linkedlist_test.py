import unittest

import algabra.datastructures.linkedlist as mylinkedlist


class LinkedListTestCase(unittest.TestCase):

    def test_empty_list(self) -> None:
        my_list = mylinkedlist.LinkedList()

        assert my_list.maximum() is None

    def test_list_with_one_node(self) -> None:
        my_list = mylinkedlist.LinkedList()
        my_list.insert(mylinkedlist.Node(22))

        assert my_list.maximum().key == 22
        assert my_list.minimum().key == 22
        assert my_list.successor(my_list.minimum()) is None
        assert my_list.predecessor(my_list.maximum()) is None

    def test_search_node_key(self) -> None:
        my_list = mylinkedlist.LinkedList()

        for key in range(50):
            my_list.insert(mylinkedlist.Node(key))

        my_node = my_list.search(45)
        successor = my_list.successor(my_node)
        predecessor = my_list.predecessor(my_node)
        assert successor.key == 46
        assert predecessor.key == 44

        my_list.delete(my_node)
        assert my_list.search(45) is None
        assert my_list.predecessor(successor).key == 44
        assert my_list.successor(predecessor).key == 46


if __name__ == '__main__':
    unittest.main()
