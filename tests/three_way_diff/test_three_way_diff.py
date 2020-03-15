from json import dumps, loads
from os import path, remove
from unittest import TestCase
from src.three_way_diff.levenshtein import get_operations
from src.three_way_diff.three_way_diff import (_compute_accuracy,
                                               _find_element, _format_input,
                                               _parse_operations,
                                               _three_way_diff_compute,
                                               three_way_diff_JSON)
from test_class import TestClass


class ThreeWayDiffTest(TestCase):
    TEST_RESULTS_LOCATION = ''
    TEST_BASE_STRING_CAPS = TestClass.TEST_STRING_BASE.upper()
    TEST_OPERATION_LIST = [('replace', index, index)
                           for index in range(TestClass.TEST_BASE_LEN)]
    TEST_OPERATION_LIST_HALF = TEST_OPERATION_LIST[:TestClass.TEST_BASE_LEN // 2]
    TEST_OPERATION_LIST_EXTRA = TEST_OPERATION_LIST[:TestClass.TEST_BASE_LEN // 2] + [
        ('replace', 3, 3),
        ('replace', 4, 4)
    ]
    TEST_OPERATION_LIST_DOUBLE = TEST_OPERATION_LIST[:-2] + [
        ('replace', 4, 4),
        ('replace', 5, 5)
    ]
    TEST_OPERATION_LIST_NOTHING = [
        ('nothing', 2, 2),
        ('nothing', 3, 3)
    ]
    TEST_OPERATION_LIST_EXTRA_NOTHING = TEST_OPERATION_LIST_HALF + \
        TEST_OPERATION_LIST_NOTHING
    TEST_REPLACE_GROUP = TestClass.TEST_LIST_BASE[:-2] + [
        'double', 'false']
    TEST_REPEATED = ['test' if element ==
                     'string' else element for element in TestClass.TEST_LIST_BASE]
    TEST_REPLACE_REPEATED = ['false' if element ==
                             'test' else element for element in TestClass.TEST_LIST_REPLACE]
    TEST_REPEATED_MULTIPLE = TEST_REPEATED + ['list', 'test']
    TEST_REPLACE_REPEATED_MULTIPLE = TEST_REPLACE_REPEATED + \
        ['list', 'false']

    def tearDown(self):
        if self.TEST_RESULTS_LOCATION:
            remove(self.TEST_RESULTS_LOCATION)

    def test__format_input_returns_expected(self):
        lowered = _format_input(self.TEST_BASE_STRING_CAPS,
                                self.TEST_BASE_STRING_CAPS)
        expected = (TestClass.TEST_LIST_BASE, TestClass.TEST_LIST_BASE)

        self.assertEqual(lowered, expected)

    def test_accuracy_returns_expected_without_nothing_operation(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_HALF, TestClass.TEST_LIST_BASE)
        expected = 0.5

        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_rounded_up_correctly(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_EXTRA, TestClass.TEST_LIST_BASE)
        expected = 0.17

        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_rounded_down_correctly(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_EXTRA[:4], TestClass.TEST_LIST_BASE)
        expected = 0.33
        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_expected_with_nothing_operation(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_EXTRA_NOTHING, TestClass.TEST_LIST_BASE)
        expected = 0.5

        self.assertEqual(expected, accuracy)

    def test__find_element_returns_expected_without_nested(self):
        found_index = _find_element(TestClass.TEST_LIST_BASE, 'test')
        expected_index = TestClass.TEST_LIST_BASE.index('test')

        self.assertEqual(expected_index, found_index)

    def test__find_element_returns_expected_with_nested(self):
        searched = ['tested', 3]
        to_search = TestClass.TEST_LIST_BASE + [['tested', 3]]
        found_index = _find_element(to_search, 'tested')
        expected_index = to_search.index(searched)

        self.assertEqual(expected_index, found_index)

    def test_parse_returns_expected_with_same(self):
        correct, diff = _parse_operations(TestClass.TEST_LIST_BASE, TestClass.TEST_LIST_BASE,
                                          get_operations(TestClass.TEST_LIST_BASE, TestClass.TEST_LIST_BASE))
        expected_correct = TestClass.TEST_LIST_BASE
        expected_diff = {}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_replace(self):
        correct, diff = _parse_operations(TestClass.TEST_LIST_REPLACE, TestClass.TEST_LIST_BASE,
                                          get_operations(TestClass.TEST_LIST_REPLACE, TestClass.TEST_LIST_BASE))
        expected_correct = TestClass.TEST_LIST_BASE[:-1]
        expected_diff = {'false': 'string'}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_insert(self):
        correct, diff = _parse_operations(TestClass.TEST_LIST_INSERT, TestClass.TEST_LIST_BASE,
                                          get_operations(TestClass.TEST_LIST_INSERT, TestClass.TEST_LIST_BASE))
        expected_correct = TestClass.TEST_LIST_BASE[:-1]
        expected_diff = {'': 'string'}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_delete(self):
        correct, diff = _parse_operations(TestClass.TEST_LIST_DELETE, TestClass.TEST_LIST_BASE,
                                          get_operations(TestClass.TEST_LIST_DELETE, TestClass.TEST_LIST_BASE))
        expected_correct = TestClass.TEST_LIST_BASE
        expected_diff = {'extra': ''}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_replace_groups(self):
        correct, diff = _parse_operations(self.TEST_REPLACE_REPEATED, self.TEST_REPEATED,
                                          get_operations(self.TEST_REPLACE_REPEATED, TestClass.TEST_LIST_BASE))
        expected_correct = [
            element for element in self.TEST_REPLACE_REPEATED if element != 'false']
        expected_diff = {'false': ['test', 2]}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_replace_groups_multiple(self):
        base = self.TEST_REPEATED_MULTIPLE
        correct, diff = _parse_operations(self.TEST_REPLACE_REPEATED_MULTIPLE, base,
                                          get_operations(self.TEST_REPLACE_REPEATED_MULTIPLE, base))
        expected_correct = [
            element for element in self.TEST_REPLACE_REPEATED if element != 'false']
        expected_diff = {'false': ['test', 3]}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_replace_multiple_for_same(self):
        correct, diff = _parse_operations(self.TEST_REPLACE_REPEATED, TestClass.TEST_LIST_BASE,
                                          get_operations(self.TEST_REPLACE_REPEATED, TestClass.TEST_LIST_BASE))
        expected_correct = [
            element for element in self.TEST_REPLACE_REPEATED if element != 'false']
        expected_diff = {'false': ['test', 'string']}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_replace_multiple_for_same(self):
        base = TestClass.TEST_LIST_BASE + ['list', 'test']
        correct, diff = _parse_operations(self.TEST_REPLACE_REPEATED_MULTIPLE, base,
                                          get_operations(self.TEST_REPLACE_REPEATED_MULTIPLE, base))
        expected_correct = [
            element for element in base if element not in ['test', 'string']]
        expected_diff = {'false': ['string', ['test', 2]]}

        self.assertEqual(set(expected_correct), set(correct))
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_replace_multiple_for_same_list_multiple_first(self):
        comparable = ['not', 'is', 'not', 'is', 'not', 'is', 'not']
        base = ['it', 'is', 'it', 'is', 'are', 'is', 'it']
        correct, diff = _parse_operations(comparable, base,
                                          get_operations(comparable, base))
        expected_correct = ['is']
        expected_diff = {'not': [['it', 3], 'are']}

        self.assertEqual(set(expected_correct), set(correct))
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_replace_multiple_list(self):
        comparable = ['not', 'is', 'not', 'is', 'not']
        base = ['it', 'is', 'a', 'is', 'test']
        correct, diff = _parse_operations(comparable, base,
                                          get_operations(comparable, base))
        expected_correct = ['is']
        expected_diff = {'not': ['it', 'a', 'test']}

        self.assertEqual(set(expected_correct), set(correct))
        self.assertEqual(expected_diff, diff)

    def test_json_computed_correctly_string(self):
        comparable, base = _format_input(
            TestClass.TEST_STRING_REPLACE, TestClass.TEST_STRING_BASE)
        operations = get_operations(comparable,
                                    base)
        result = _three_way_diff_compute(TestClass.TEST_STRING_REPLACE,
                                         TestClass.TEST_STRING_REPLACE,
                                         TestClass.TEST_STRING_BASE)

        comparable_result, comparable_diff = _parse_operations(comparable,
                                                               base,
                                                               operations)

        assert result['correct']['comparable1'] == comparable_result
        assert result['correct']['comparable2'] == comparable_result
        assert result['diff']['comparable1'] == comparable_diff
        assert result['diff']['comparable2'] == comparable_diff

        accuracy = _compute_accuracy(operations, base)
        assert result['accuracy']['comparable1'] == accuracy
        assert result['accuracy']['comparable2'] == accuracy

    def test_json_file_created_string(self):
        three_way_diff_JSON(
            'comparable1', 'comparable2', 'base')
        self.TEST_RESULTS_LOCATION = 'results.json'

        assert path.exists(self.TEST_RESULTS_LOCATION)
