from unittest import TestCase
from test_class import TestClass
from src.three_way_diff.levenshtein import get_operations, get_levenshtein_distance_matrix
from numpy import array, equal, zeros


class LevenshteinTest(TestCase):
    TEST_EXPECTED_ARRAY = array([
        [0, 1, 2, 3, 4, 5, 6],
        [1, 0, 1, 2, 3, 4, 5],
        [2, 1, 0, 1, 2, 3, 4],
        [3, 2, 1, 0, 1, 2, 3],
        [4, 3, 2, 1, 0, 1, 2],
        [5, 4, 3, 2, 1, 0, 1],
        [6, 5, 4, 3, 2, 1, 1]
    ])
    TEST_EMPTY_STRING = ''
    TEST_EMPTY_LIST = []
    TEST_ZERO_ARRAY = zeros((1, 1))
    TEST_BASE_STRING_CAPS = TestClass.TEST_STRING_BASE.upper()
    TEST_BASE_STRING_LEN = len(TestClass.TEST_STRING_BASE)
    TEST_BASE_LIST_CAPS = [element.upper()
                           for element in TestClass.TEST_LIST_BASE]

    def test_levenshtein_distance_returns_expected(self):
        distance = get_levenshtein_distance_matrix(
            TestClass.TEST_LIST_REPLACE, TestClass.TEST_LIST_BASE)
        equal_distance = equal(distance, self.TEST_EXPECTED_ARRAY).all()

        assert equal_distance

    def test_levenshtein_distance_returns_zero_array_with_empty_lists(self):
        distance = get_levenshtein_distance_matrix(
            self.TEST_EMPTY_LIST, self.TEST_EMPTY_LIST)
        equal_distance = equal(distance, self.TEST_ZERO_ARRAY).all()

        assert equal_distance

    def test_operations_returns_empty_with_empty_lists(self):
        operations = get_operations(self.TEST_EMPTY_LIST, self.TEST_EMPTY_LIST)

        self.assertEqual(self.TEST_EMPTY_LIST, operations)

    def test_operations_returns_all_nothing_with_equal(self):
        operations = get_operations(
            TestClass.TEST_LIST_BASE, TestClass.TEST_LIST_BASE)

        self.assertEqual(TestClass.TEST_OPERATION_LIST_EQUAL, operations)

    def test_operations_returns_expected_replace(self):
        operations = get_operations(
            TestClass.TEST_LIST_REPLACE, TestClass.TEST_LIST_BASE)

        expected = TestClass.TEST_OPERATION_LIST_REPLACE

        self.assertEqual(expected, operations)

    def test_operations_returns_expected_insert(self):
        operations = get_operations(
            TestClass.TEST_LIST_INSERT, TestClass.TEST_LIST_BASE)

        expected = TestClass.TEST_OPERATION_LIST_INSERT

        self.assertEqual(expected, operations)

    def test_operations_returns_expected_delete(self):
        operations = get_operations(
            TestClass.TEST_LIST_DELETE, TestClass.TEST_LIST_BASE)

        expected = TestClass.TEST_OPERATION_LIST_DELETE

        self.assertEqual(expected, operations)
