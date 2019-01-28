import typing
import unittest

import algabra.datastructures.array as myarray


class FixedArrayTestCase(unittest.TestCase):

    def test_create_empty_fixed_array(self) -> None:
        fixed_array = myarray.FixedArray()
        assert not fixed_array

    def test_create_fixed_array(self) -> None:
        fixed_array = myarray.FixedArray(5)
        assert not fixed_array

    def test_create_fixed_array_with_elements(self) -> None:
        fixed_array = myarray.FixedArray([1, 2, 3, 'eggs'])
        assert len(fixed_array) == 4

    def test_can_not_extend(self) -> None:
        fixed_array = myarray.FixedArray(4)

        fixed_array[3] = 'eggs'
        assert fixed_array[3] == 'eggs'
        with self.assertRaises(IndexError):
            fixed_array[4] = 'spam'


class RubberArrayTestCase(unittest.TestCase):

    def test_create_empty(self) -> None:
        rubber_array = myarray.RubberArray()

        assert not rubber_array

    def test_extend_array(self) -> None:
        rubber_array = myarray.RubberArray(['eggs', 'spam'])
        assert len(rubber_array) == 2

        rubber_array[3] = 'guido'
        assert len(rubber_array) > 2

    def test_array_reducing(self) -> None:
        rubber_array = myarray.RubberArray([i for i in range(100)])

        assert rubber_array[80] == 80

        self._pop_n_items(rubber_array, 20)
        assert rubber_array[80] is None

        self._pop_n_items(rubber_array, 79)
        assert rubber_array[1] is None

        with self.assertRaises(IndexError):
            print(rubber_array[80])

    @staticmethod
    def _pop_n_items(array: typing.MutableSequence, n_items: int) -> None:
        array_length = len(array)
        for i in range(array_length, array_length - n_items, -1):
            del array[i - 1]


if __name__ == '__main__':
    unittest.main()
