'''
This module defines the functions to compute the three-way-diff between
three objects of type str.
The functions defined are:
- three_way_diff_JSON
'''

from json import dump
from typing import Dict, List, Set, Tuple, Union
from three_way_diff.levenshtein import get_operations


def _format_input(comparable: str, base: str) -> Tuple[List[str], List[str]]:
    '''This function makes the given objects lowercase.'''
    comparable_split = comparable.lower().split()
    base_split = base.lower().split()

    return comparable_split, base_split


def _parse_operations(comparable: List[str], base: List[str],
                      operations_list: List[Tuple[str, int, int]]) \
        -> Tuple[List[str], Dict[str, Union[str, List[str]]]]:
    '''
    This functions parses the operations required to go from the comparable
    list of stirngs to the base list of strings. The returned dicitonary has
    the wrong part in the comparable list of strings mapped to the part in the
    given base list of strings as well as the times that it happens if bigger
    or equal to 2.
    '''
    diff: Dict[str, Union[str, List[str]]] = {}
    # Using a dict to maintain order of insertion
    correct: Dict[str, bool] = {}
    separator = ' '
    operations_enumerated = list(enumerate(operations_list))
    index_operation = 0

    while index_operation < len(operations_enumerated):
        index_operation, (
            operation,
            index_comparable_start,
            index_base_start) = operations_enumerated[index_operation]
        index_base_end = index_base_start
        index_comparable_end = index_comparable_start
        previous_index_base = index_base_start
        previous_index_comparable = index_comparable_start
        previous_index_operation = index_operation

        if operation == 'nothing':
            key = comparable[index_base_start]
            value = correct.get(key, False)

            if not value:
                correct[key] = True

            index_operation += 1
        else:
            while operation != 'nothing' \
                and (index_base_start == index_base_end
                     or (previous_index_base + 1 == index_base_end
                         and previous_index_comparable + 1
                         == index_comparable_end)):
                index_operation += 1

                if index_operation < len(operations_list):
                    previous_index_base = index_base_end
                    previous_index_comparable = index_comparable_end
                    operation, index_comparable_end, \
                        index_base_end = operations_list[index_operation]
                else:
                    break

            index_base_end = operations_list[index_operation - 1][2]
            index_comparable_end = operations_list[index_operation - 1][1]

            if operation == 'insert' \
                    and previous_index_operation + 1 == index_operation:
                key = ''
            else:
                key = separator.join(
                    comparable[
                        index_comparable_start:index_comparable_end + 1])

            value = separator.join(base[index_base_start:index_base_end + 1])
            current_value = diff.get(key)

            if current_value:
                if current_value == value:
                    diff[key] = [current_value, 2]
                elif isinstance(current_value, list) \
                        and isinstance(current_value[1], int):
                    if current_value[0] == value:
                        diff[key][1] += 1
                    else:
                        diff[key] = [current_value, value]
                elif isinstance(current_value, list):
                    index_found = _find_element(current_value, value)

                    if index_found >= 0:
                        value_found = current_value[index_found]

                        if isinstance(value_found, list):
                            current_value[index_found][1] += 1
                        else:
                            current_value.remove(value)
                            value_found = [value_found, 2]
                            current_value.append(value_found)
                    else:
                        diff[key].append(value)
                else:
                    diff[key] = [current_value, value]
            else:
                diff[key] = value

            index_comparable_start = index_comparable_end

    return list(correct.keys()), diff


def _compute_accuracy(operations_list: List[Tuple[str, int, int]],
                      base: List[str]) -> float:
    '''
    This function computes the accuracy of words given a list
    of operations to get from a string to the base string.
    '''
    missed_indices: Set[int] = set()

    for operation, _index_comparable, index_base in operations_list:
        if operation != 'nothing' \
                and index_base not in missed_indices:
            missed_indices.add(index_base)

    return round(1 - len(missed_indices) / len(base), 2)


def _find_element(list_values: List[str], value: str) -> int:
    '''
    This function returns the index where the given value
    is within the list or -1.
    '''

    for element_index, element in enumerate(list_values):
        if isinstance(element, list):
            if value in element:
                return element_index
        elif element == value:
            return element_index
    return -1


def _three_way_diff_compute(comparable1: str,
                            comparable2: str,
                            base: str)\
    -> Dict[str,
            Union[Dict[str, Union[str, List[Union[str, int]]]],
                  Dict[str, float]]]:
    '''
    This function creates a dictionary holding the results for
    the given comparable1 and comparable2 strings when compared with
    the base given string.
    '''
    comparable1_split, base_split = _format_input(comparable1, base)
    comparable2_split, base_split = _format_input(comparable2, base)

    operations_list_comparable1 = get_operations(comparable1_split, base_split)
    comparable1_correct, comparable1_diff = _parse_operations(
        comparable1_split, base_split, operations_list_comparable1)

    operations_list_comparable2 = get_operations(comparable2_split, base_split)
    comparable2_correct, comparable2_diff = _parse_operations(
        comparable2_split, base_split, operations_list_comparable2)

    results: Dict[str,
                  Union[Dict[str, Union[str, List[Union[str, int]]]],
                        Dict[str, float]]] = {
                            'correct': {
                                'comparable1': comparable1_correct,
                                'comparable2': comparable2_correct,
                            },
                            'diff': {
                                'comparable1': comparable1_diff,
                                'comparable2': comparable2_diff
                            },
                            'accuracy': {
                                'comparable1': _compute_accuracy(
                                    operations_list_comparable1,
                                    base_split),
                                'comparable2': _compute_accuracy(
                                    operations_list_comparable2,
                                    base_split),
                            }}

    return results


def three_way_diff_JSON(comparable1: str,
                        comparable2: str,
                        base: str) -> None:
    '''
    This function creates a JSON file comparing the given comparable1,
    comparable2 and base string.
    '''
    results_json = _three_way_diff_compute(comparable1, comparable2, base)

    with open('results.json', 'w') as json_file:
        dump(results_json, json_file)
