"""
This module defines the functions to compute the three-way-diff between
three objects of type str or List[str].
The functions defined are:
- three_way_diff_JSON
- three_way_diff_HTML
"""

from json import dump, dumps
from os import getcwd, path
from typing import Any, Dict, List, Tuple, Union
from json2html import *
from levenshtein import get_operations


def _parse_operations(comparable: Union[str, List[str]],
                      base: Union[str, List[str]],
                      operations_list: List[Tuple[str, int, int]]) \
        -> Tuple[List[str], Dict[Any, Union[str, List[Union[str, int]]]]]:
    """
    This functions parses the operations required to go from the comparable
    object to the base object. The returned dicitonary has the wrong part in
    the comparable object mapped to the part in the given base object as well
    as the times that it happens if bigger or equal to 2.
    """
    diff: Dict[str, Union[str, List[Union[str, int]]]] = {}
    correct: Dict[str, bool] = {}

    separator = ' ' if isinstance(base, list) else ''

    for index_operation, (operation, index_comparable_start,
                          index_base_start) in enumerate(operations_list):
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
                      base: Union[str, List[str]]) -> float:
    """
    This function computes the accuracy of words given a list
    of operations to get from a string to the base string.
    """
    missed_indices: Dict[int, bool] = {}

    for operation, _index_comparable, index_base in operations_list:
        if operation != 'nothing' \
                and not missed_indices.get(index_base, False):
            missed_indices[index_base] = True

    return round(1 - len(missed_indices.keys()) / len(base), 2)


def _find_element(list_values: List[str], value) -> int:
    """
    This function returns the index where the given value
    is within the list or -1.
    """

    for element_index, element in enumerate(list_values):

        if isinstance(element, list):
            if value in element:
                return element_index
        elif element == value:
            return element_index
    return -1


def three_way_diff_compute(comparable1: Union[str, List[str]],
                           comparable2: Union[str, List[str]],
                           base: Union[str, List[str]])\
    -> Dict[str,
            Union[Dict[str, Union[str, List[Union[str, int]]]],
                  Dict[str, float]]]:
    """
    This function creates a JSON object holding the results for
    the given comparable1 and comparable2 objects when compared with
    the base given object. The JSON object containing the results will
    have the differences between the strings and the accuracy of each string.
    """

    operations_list_comparable1 = get_operations(comparable1, base)
    comparable1_correct, comparable1_diff = _parse_operations(
        comparable1, base, operations_list_comparable1)

    operations_list_comparable2 = get_operations(comparable2, base)
    comparable2_correct, comparable2_diff = _parse_operations(
        comparable2, base, operations_list_comparable2)

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
                                    base),
                                'comparable2': _compute_accuracy(
                                    operations_list_comparable2,
                                    base),
                            }}

    return results


def three_way_diff_JSON(comparable1: Union[str, List[str]],
                        comparable2: Union[str, List[str]],
                        base: Union[str, List[str]], file_object: str) -> str:
    """
    This function creates a JSON file comparing the given comparable1,
    comparable2 and base objects. The file is then saved in the
    location of the given file_object (_file_) in the returned path.
    """
    results_json = three_way_diff_compute(comparable1, comparable2, base)
    root = path.join(getcwd(), path.dirname(file_object))
    file_location = f'{root}/results.json'

    with open(file_location, 'w') as file:
        dump(results_json, file)

    return file_location


def three_way_diff_HTML(comparable1: Union[str, List[str]],
                        comparable2: Union[str, List[str]],
                        base: Union[str, List[str]], file_object: str) -> str:
    """
    This function creates an HTML file comparing the given comparable1,
    comparable2 and base objects. The file is then saved in the
    location of the given file_object (_file_) in the returned path.
    """
    results_json = dumps(three_way_diff_compute(
        comparable1, comparable2, base))
    root = path.join(getcwd(), path.dirname(file_object))
    file_location = f'{root}/results.html'

    with open(file_location, 'w') as file:
        file.write(json2html.convert(json=results_json))

    return file_location
