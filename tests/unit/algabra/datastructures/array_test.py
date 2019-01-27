import unittest

import algabra.datastructures.array as myarray


class FixedArrayTestCase(unittest.TestCase):

    def test_create_empty_fixed_array(self) -> None:
        fixed_array = myarray.FixedArray()
        assert not fixed_array

    def test_create_fixed_array(self) -> None:
        fixed_array = myarray.FixedArray(5)
        assert len(fixed_array) == 5

    def test_create_fixed_array_with_elements(self) -> None:
        fixed_array = myarray.FixedArray([1, 2, 3, 'eggs'])
        assert len(fixed_array) == 4

    def test_can_not_extend(self) -> None:
        fixed_array = myarray.FixedArray(4)

        fixed_array[3] = 'eggs'
        assert fixed_array[3] == 'eggs'
        with self.assertRaises(IndexError):
            fixed_array[4] = 'spam'

    def test_can_not_reduce(self) -> None:
        fixed_array = myarray.FixedArray(['eggs', 'spam'])
        del fixed_array[1]

        assert fixed_array[1] is None
        assert len(fixed_array) == 2


if __name__ == '__main__':
    unittest.main()
