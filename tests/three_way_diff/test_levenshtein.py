from unittest import TestCase
from test_class import TestClass
from src.three_way_diff.levenshtein import _lower_input, get_operations, get_levenshtein_distance_matrix
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

    def test__lower_input_returns_expected_lists(self):
        lowered = _lower_input(self.TEST_BASE_LIST_CAPS,
                               self.TEST_BASE_LIST_CAPS)
        expected = (TestClass.TEST_LIST_BASE, TestClass.TEST_LIST_BASE)

        self.assertEqual(lowered, expected)

    def test__lower_input_returns_expected_strings(self):
        lowered = _lower_input(self.TEST_BASE_STRING_CAPS,
                               self.TEST_BASE_STRING_CAPS)
        expected = (TestClass.TEST_STRING_BASE, TestClass.TEST_STRING_BASE)

        self.assertEqual(lowered, expected)

    def test_levenshtein_distance_returns_expected_strings(self):
        distance = get_levenshtein_distance_matrix(
            TestClass.TEST_STRING_REPLACE, TestClass.TEST_STRING_BASE)
        equal_distance = equal(distance, self.TEST_EXPECTED_ARRAY).all()

        assert equal_distance

    def test_levenshtein_distance_returns_expected_lists(self):
        distance = get_levenshtein_distance_matrix(
            TestClass.TEST_LIST_REPLACE, TestClass.TEST_LIST_BASE)
        equal_distance = equal(distance, self.TEST_EXPECTED_ARRAY).all()

        assert equal_distance

    def test_levenshtein_distance_returns_zero_array_with_empty_lists(self):
        distance = get_levenshtein_distance_matrix(
            self.TEST_EMPTY_LIST, self.TEST_EMPTY_LIST)
        equal_distance = equal(distance, self.TEST_ZERO_ARRAY).all()

        assert equal_distance

    def test_levenshtein_distance_returns_zero_array_with_empty_strings(self):
        distance = get_levenshtein_distance_matrix(
            self.TEST_EMPTY_STRING, self.TEST_EMPTY_STRING)
        equal_distance = equal(distance, self.TEST_ZERO_ARRAY).all()

        assert equal_distance

    def test_operations_returns_empty_with_empty_lists(self):
        operations = get_operations(self.TEST_EMPTY_LIST, self.TEST_EMPTY_LIST)

        self.assertEqual(self.TEST_EMPTY_LIST, operations)

    def test_operations_returns_empty_with_empty_strings(self):
        operations = get_operations(
            self.TEST_EMPTY_STRING, self.TEST_EMPTY_STRING)

        self.assertEqual(self.TEST_EMPTY_LIST, operations)

    def test_operations_returns_all_nothing_with_equal_strings(self):
        operations = get_operations(
            TestClass.TEST_STRING_BASE, TestClass.TEST_STRING_BASE)

        self.assertEqual(TestClass.TEST_OPERATION_LIST_EQUAL, operations)

    def test_operations_returns_all_nothing_with_equal_lists(self):
        operations = get_operations(
            TestClass.TEST_LIST_BASE, TestClass.TEST_LIST_BASE)

        self.assertEqual(TestClass.TEST_OPERATION_LIST_EQUAL, operations)

    def test_operations_returns_expected_replace_strings(self):
        operations = get_operations(
            TestClass.TEST_STRING_REPLACE, TestClass.TEST_STRING_BASE)

        expected = TestClass.TEST_OPERATION_LIST_REPLACE

        self.assertEqual(expected, operations)

    def test_operations_returns_expected_replace_lists(self):
        operations = get_operations(
            TestClass.TEST_LIST_REPLACE, TestClass.TEST_LIST_BASE)

        expected = TestClass.TEST_OPERATION_LIST_REPLACE

        self.assertEqual(expected, operations)

    def test_operations_returns_expected_insert_strings(self):
        operations = get_operations(
            TestClass.TEST_STRING_INSERT, TestClass.TEST_STRING_BASE)

        expected = TestClass.TEST_OPERATION_LIST_INSERT

        self.assertEqual(expected, operations)

    def test_operations_returns_expected_insert_lists(self):
        operations = get_operations(
            TestClass.TEST_LIST_INSERT, TestClass.TEST_LIST_BASE)

        expected = TestClass.TEST_OPERATION_LIST_INSERT

        self.assertEqual(expected, operations)

    def test_operations_returns_expected_delete_strings(self):
        operations = get_operations(
            TestClass.TEST_STRING_DELETE, TestClass.TEST_STRING_BASE)

        expected = TestClass.TEST_OPERATION_LIST_DELETE

        self.assertEqual(expected, operations)

    def test_operations_returns_expected_delete_lists(self):
        operations = get_operations(
            TestClass.TEST_LIST_DELETE, TestClass.TEST_LIST_BASE)

        expected = TestClass.TEST_OPERATION_LIST_DELETE

        self.assertEqual(expected, operations)
