import unittest

import algabra.algorithms.bsearch as bsearch


class BinarySearchTestCase(unittest.TestCase):

    def test_basic_searching(self) -> None:
        items_count = 1000
        target_list = list(range(items_count))
        result = bsearch.binary_search(target_list, 123)

        assert result == 123

    def test_search_not_found(self) -> None:
        result1 = bsearch.binary_search([2, 3], 4)
        assert result1 is None

        result2 = bsearch.binary_search([2, 3], 1)
        assert result2 is None

    def test_search_not_found_among(self) -> None:
        result = bsearch.binary_search([1, 4], 3)
        assert result is None

    def test_search_in_empty_list(self) -> None:
        result = bsearch.binary_search([], 5)
        assert result is None

    def test_search_no_result(self) -> None:
        result = bsearch.binary_search([1, 2, 3, 4, 6], 5)
        assert result is None

    def test_search_first_item(self) -> None:
        result = bsearch.binary_search([1, 2, 3, 4, 6], 1)
        assert result == 0


if __name__ == '__main__':
    unittest.main()
