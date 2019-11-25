from unittest import TestCase
from json import dumps, loads
from test_class import TestClass
from os import remove, path
from src.three_way_diff.three_way_diff import _parse_operations, \
    _compute_accuracy, _find_element, three_way_diff_compute, three_way_diff_JSON, three_way_diff_HTML
from src.three_way_diff.levenshtein import get_operations


class ThreeWayDiffTest(TestCase):
    TEST_RESULTS_LOCATION = ''
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
    TEST_STRING_REPLACE_GROUP = TestClass.TEST_STRING_BASE[:-2] + 'ff'
    TEST_LIST_REPLACE_GROUP = TestClass.TEST_LIST_BASE[:-2] + [
        'double', 'false']
    TEST_STRING_REPEATED = TestClass.TEST_STRING_BASE.replace('t', 's')
    TEST_LIST_REPEATED = ['test' if element ==
                          'string' else element for element in TestClass.TEST_LIST_BASE]
    TEST_STRING_REPLACE_REPEATED = TestClass.TEST_STRING_REPLACE.replace(
        's', 'f')
    TEST_LIST_REPLACE_REPEATED = ['false' if element ==
                                  'test' else element for element in TestClass.TEST_LIST_REPLACE]
    TEST_STRING_REPEATED_MULTIPLE = TEST_STRING_REPEATED + 'ps'
    TEST_LIST_REPEATED_MULTIPLE = TEST_LIST_REPEATED + ['list', 'test']
    TEST_STRING_REPLACE_REPEATED_MULTIPLE = TEST_STRING_REPLACE_REPEATED + 'pf'
    TEST_LIST_REPLACE_REPEATED_MULTIPLE = TEST_LIST_REPLACE_REPEATED + \
        ['list', 'false']
    TEST_STRING_REPLACE_DIFFERENT_MULTIPLE_GROUP = TestClass.TEST_STRING_BASE.replace(
        's', 'f').replace('p', 'f') + 'ftf'

    def tearDown(self):
        if self.TEST_RESULTS_LOCATION:
            remove(self.TEST_RESULTS_LOCATION)

    def test_accuracy_returns_expected_without_nothing_list(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_HALF, TestClass.TEST_LIST_BASE)
        expected = 0.5

        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_expected_without_nothing_string(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_HALF, TestClass.TEST_STRING_BASE)
        expected = 0.5

        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_rounded_up_correctly_string(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_EXTRA, TestClass.TEST_STRING_BASE)
        expected = 0.17

        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_rounded_up_correctly_list(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_EXTRA, TestClass.TEST_STRING_BASE)
        expected = 0.17

        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_rounded_down_correctly_string(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_EXTRA[:4], TestClass.TEST_STRING_BASE)
        expected = 0.33

        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_rounded_down_correctly_list(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_EXTRA[:4], TestClass.TEST_STRING_BASE)
        expected = 0.33
        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_expected_with_nothing_string(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_EXTRA_NOTHING, TestClass.TEST_STRING_BASE)
        expected = 0.5

        self.assertEqual(expected, accuracy)

    def test_accuracy_returns_expected_with_nothing_list(self):
        accuracy = _compute_accuracy(
            self.TEST_OPERATION_LIST_EXTRA_NOTHING, TestClass.TEST_STRING_BASE)
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

    def test_parse_returns_expected_with_same_string(self):
        correct, diff = _parse_operations(TestClass.TEST_STRING_BASE, TestClass.TEST_STRING_BASE,
                                          get_operations(TestClass.TEST_STRING_BASE, TestClass.TEST_STRING_BASE))
        expected_correct = list(TestClass.TEST_STRING_BASE)
        expected_diff = {}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_same_list(self):
        correct, diff = _parse_operations(TestClass.TEST_LIST_BASE, TestClass.TEST_LIST_BASE,
                                          get_operations(TestClass.TEST_LIST_BASE, TestClass.TEST_LIST_BASE))
        expected_correct = TestClass.TEST_LIST_BASE
        expected_diff = {}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_string_replace(self):
        correct, diff = _parse_operations(TestClass.TEST_STRING_REPLACE, TestClass.TEST_STRING_BASE,
                                          get_operations(TestClass.TEST_STRING_REPLACE, TestClass.TEST_STRING_BASE))
        expected_correct = list(TestClass.TEST_STRING_BASE)[:-1]
        expected_diff = {'f': 't'}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_replace(self):
        correct, diff = _parse_operations(TestClass.TEST_LIST_REPLACE, TestClass.TEST_LIST_BASE,
                                          get_operations(TestClass.TEST_LIST_REPLACE, TestClass.TEST_LIST_BASE))
        expected_correct = TestClass.TEST_LIST_BASE[:-1]
        expected_diff = {'false': 'string'}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_string_insert(self):
        correct, diff = _parse_operations(TestClass.TEST_STRING_INSERT, TestClass.TEST_STRING_BASE,
                                          get_operations(TestClass.TEST_STRING_INSERT, TestClass.TEST_STRING_BASE))
        expected_correct = list(TestClass.TEST_STRING_BASE)[:-1]
        expected_diff = {'': 't'}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_insert(self):
        correct, diff = _parse_operations(TestClass.TEST_LIST_INSERT, TestClass.TEST_LIST_BASE,
                                          get_operations(TestClass.TEST_LIST_INSERT, TestClass.TEST_LIST_BASE))
        expected_correct = TestClass.TEST_LIST_BASE[:-1]
        expected_diff = {'': 'string'}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_string_delete(self):
        correct, diff = _parse_operations(TestClass.TEST_STRING_DELETE, TestClass.TEST_STRING_BASE,
                                          get_operations(TestClass.TEST_STRING_DELETE, TestClass.TEST_STRING_BASE))
        expected_correct = list(TestClass.TEST_STRING_BASE)
        expected_diff = {'e': ''}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_delete(self):
        correct, diff = _parse_operations(TestClass.TEST_LIST_DELETE, TestClass.TEST_LIST_BASE,
                                          get_operations(TestClass.TEST_LIST_DELETE, TestClass.TEST_LIST_BASE))
        expected_correct = TestClass.TEST_LIST_BASE
        expected_diff = {'extra': ''}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_string_replace_groups(self):
        correct, diff = _parse_operations(self.TEST_STRING_REPLACE_REPEATED, self.TEST_STRING_REPEATED,
                                          get_operations(self.TEST_STRING_REPLACE_REPEATED, TestClass.TEST_STRING_BASE))
        expected_correct = list(self.TEST_STRING_REPEATED.replace('s', ''))
        expected_diff = {'f': ['s', 2]}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_replace_groups(self):
        correct, diff = _parse_operations(self.TEST_LIST_REPLACE_REPEATED, self.TEST_LIST_REPEATED,
                                          get_operations(self.TEST_LIST_REPLACE_REPEATED, TestClass.TEST_LIST_BASE))
        expected_correct = [
            element for element in self.TEST_LIST_REPLACE_REPEATED if element != 'false']
        expected_diff = {'false': ['test', 2]}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_string_replace_groups_multiple(self):
        correct, diff = _parse_operations(self.TEST_STRING_REPLACE_REPEATED_MULTIPLE, self.TEST_STRING_REPEATED_MULTIPLE,
                                          get_operations(self.TEST_STRING_REPLACE_REPEATED_MULTIPLE, self.TEST_STRING_REPEATED_MULTIPLE))
        expected_correct = list(
            self.TEST_STRING_REPEATED_MULTIPLE.replace('s', ''))
        expected_diff = {'f': ['s', 3]}

        self.assertEqual(set(expected_correct), set(correct))
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_replace_groups_multiple(self):
        correct, diff = _parse_operations(self.TEST_LIST_REPLACE_REPEATED_MULTIPLE, self.TEST_LIST_REPEATED_MULTIPLE,
                                          get_operations(self.TEST_LIST_REPLACE_REPEATED_MULTIPLE, self.TEST_LIST_REPEATED_MULTIPLE))
        expected_correct = [
            element for element in self.TEST_LIST_REPLACE_REPEATED if element != 'false']
        expected_diff = {'false': ['test', 3]}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_string_replace_multiple_for_same(self):
        correct, diff = _parse_operations(self.TEST_STRING_REPLACE_REPEATED, TestClass.TEST_STRING_BASE,
                                          get_operations(self.TEST_STRING_REPLACE_REPEATED, TestClass.TEST_STRING_BASE))
        expected_correct = list(
            self.TEST_STRING_REPEATED_MULTIPLE.replace('s', ''))
        expected_diff = {'f': ['s', 't']}

        self.assertEqual(set(expected_correct), set(correct))
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_replace_multiple_for_same(self):
        comparable = ['this', 'is', 'a', 'false',
                      'list', 'false', 'list', 'false']

        correct, diff = _parse_operations(self.TEST_LIST_REPLACE_REPEATED, TestClass.TEST_LIST_BASE,
                                          get_operations(self.TEST_LIST_REPLACE_REPEATED, TestClass.TEST_LIST_BASE))
        expected_correct = [
            element for element in self.TEST_LIST_REPLACE_REPEATED if element != 'false']
        expected_diff = {'false': ['test', 'string']}

        self.assertEqual(expected_correct, correct)
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_string_replace_multiple_for_same_list(self):
        comparable = 'fabcfdfdf'
        base = 'sabcpdsds'
        correct, diff = _parse_operations(comparable, base,
                                          get_operations(comparable, base))
        expected_correct = list('abcd')
        expected_diff = {'f': ['p', ['s', 3]]}

        self.assertEqual(set(expected_correct), set(correct))
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_replace_multiple_for_same_list(self):
        assert self.TEST_STRING_REPLACE_DIFFERENT_MULTIPLE_GROUP == 'fcriftftf'
        correct, diff = _parse_operations(self.TEST_STRING_REPLACE_DIFFERENT_MULTIPLE_GROUP, TestClass.TEST_STRING_BASE + 'sts',
                                          get_operations(self.TEST_STRING_REPLACE_DIFFERENT_MULTIPLE_GROUP, TestClass.TEST_STRING_BASE + 'sts'))
        expected_correct = list(
            TestClass.TEST_STRING_BASE.replace('s', '').replace('p', ''))
        expected_diff = {'f': ['p', ['s', 3]]}

        self.assertEqual(set(expected_correct), set(correct))
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_string_replace_multiple_for_same_list_multiple_first(self):
        comparable = 'fbfbf'
        base = 'ababm'
        correct, diff = _parse_operations(comparable, base,
                                          get_operations(comparable, base))
        expected_correct = list('b')
        expected_diff = {'f': [['a', 2], 'm']}

        self.assertEqual(set(expected_correct), set(correct))
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_list_replace_multiple_for_same_list_multiple_first(self):
        comparable = ['not', 'is', 'not', 'is', 'not']
        base = ['it', 'is', 'it', 'is', 'are']
        correct, diff = _parse_operations(comparable, base,
                                          get_operations(comparable, base))
        expected_correct = ['is']
        expected_diff = {'not': [['it', 2], 'are']}

        self.assertEqual(set(expected_correct), set(correct))
        self.assertEqual(expected_diff, diff)

    def test_parse_returns_expected_with_different_string_replace_multiple_list(self):
        comparable = 'fbfbf'
        base = 'abcbe'
        correct, diff = _parse_operations(comparable, base,
                                          get_operations(comparable, base))
        expected_correct = list('b')
        expected_diff = {'f': ['a', 'c', 'e']}

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

    def test_json_computed_correcly_string(self):
        operations = get_operations(TestClass.TEST_STRING_REPLACE,
                                    TestClass.TEST_STRING_BASE)
        result = three_way_diff_compute(TestClass.TEST_STRING_REPLACE,
                                        TestClass.TEST_STRING_REPLACE,
                                        TestClass.TEST_STRING_BASE)
        comparable_result, comparable_diff = _parse_operations(TestClass.TEST_STRING_REPLACE,
                                                                TestClass.TEST_STRING_BASE,
                                                                operations)

        assert result['correct']['comparable1'] == comparable_result
        assert result['correct']['comparable2'] == comparable_result
        assert result['diff']['comparable1'] == comparable_diff
        assert result['diff']['comparable2'] == comparable_diff
        
        accuracy = _compute_accuracy(operations, TestClass.TEST_STRING_BASE)
        assert result['accuracy']['comparable1'] == accuracy
        assert result['accuracy']['comparable2'] == accuracy

    def test_json_computed_correcly_list(self):
        operations = get_operations(TestClass.TEST_LIST_REPLACE,
                                    TestClass.TEST_LIST_BASE)
        result = three_way_diff_compute(TestClass.TEST_LIST_REPLACE,
                                              TestClass.TEST_LIST_REPLACE,
                                              TestClass.TEST_LIST_BASE)
        comparable_result, comparable_diff = _parse_operations(TestClass.TEST_LIST_REPLACE,
                                                               TestClass.TEST_LIST_BASE,
                                                               operations)

        assert result['correct']['comparable1'] == comparable_result
        assert result['correct']['comparable2'] == comparable_result
        assert result['diff']['comparable1'] == comparable_diff
        assert result['diff']['comparable2'] == comparable_diff

        accuracy = _compute_accuracy(operations, TestClass.TEST_LIST_BASE)
        assert result['accuracy']['comparable1'] == accuracy
        assert result['accuracy']['comparable2'] == accuracy

    def test_json_file_created_string(self):
        file_path = three_way_diff_JSON(
            'comparable1', 'comparable2', 'base', __file__)
        self.TEST_RESULTS_LOCATION = file_path

        assert path.exists(file_path)

    def test_json_file_created_list(self):
        comparable1 = ['this', 'is', 'the', 'first', 'comparable']
        comparable2 = ['this', 'is', 'the', 'second', 'comparable']
        base = ['this', 'is', 'the', 'base']
        file_path = three_way_diff_JSON(
            comparable1, comparable2, base, __file__)
        self.TEST_RESULTS_LOCATION = file_path

        assert path.exists(file_path)

    def test_html_file_created_string(self):
        file_path = three_way_diff_HTML(
            'comparable1', 'comparable2', 'base', __file__)
        self.TEST_RESULTS_LOCATION = file_path

        assert path.exists(file_path)

    def test_html_file_created_list(self):
        comparable1 = ['this', 'is', 'the', 'first', 'comparable']
        comparable2 = ['this', 'is', 'the', 'second', 'comparable']
        base = ['this', 'is', 'the', 'base']
        file_path = three_way_diff_HTML(
            comparable1, comparable2, base, __file__)
        self.TEST_RESULTS_LOCATION = file_path

        assert path.exists(file_path)
