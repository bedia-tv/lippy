"""
This module defines the functions to compute the Levenshtein distance between
two objects of type str or List[str].
The functions defined are:
- get_operations
- get_levenshtein_distance_matrix
"""

from typing import List, Tuple, Union
from numpy import argmin, ndarray, zeros


def _lower_input(comparable: Union[str, List[str]],
                 base: Union[str, List[str]]) \
        -> Tuple[Union[str, List[str]], Union[str, List[str]]]:
    """This function makes the given objects lowercase."""

    if isinstance(comparable, str):
        comparable = comparable.lower()
        base = base.lower()
    else:
        comparable = [word.lower() for word in comparable]
        base = [word.lower() for word in base]

    return comparable, base


def get_operations(comparable: Union[str, List[str]],
                   base: Union[str, List[str]]) -> List[Tuple[str, int, int]]:
    """
    This function gets the required operations to get from the given
    comparable string to the given base string. The operations are in format
    (operation_type, index_comparable, index_base).
    """

    comparable, base = _lower_input(comparable, base)
    dist_matrix = get_levenshtein_distance_matrix(comparable, base)
    rows, cols = dist_matrix.shape
    rows -= 1
    cols -= 1
    operations: List[Tuple[str, int, int]] = []

    while rows != -1 and cols != -1:
        index = argmin([dist_matrix[rows - 1, cols - 1],
                        dist_matrix[rows, cols - 1],
                        dist_matrix[rows - 1, cols]])

        if index == 0:
            if dist_matrix[rows, cols] > dist_matrix[rows - 1, cols - 1]:
                operations.insert(0, ('replace', rows - 1, cols - 1))
            elif rows != 0 and cols != 0:
                operations.insert(0, ('nothing', rows - 1, cols - 1))

            rows -= 1
            cols -= 1
        elif index == 1:
            operations.insert(0, ('insert', rows - 1, cols - 1))
            cols -= 1
        elif index == 2:
            operations.insert(0, ('delete', rows - 1, rows - 1))
            rows -= 1

    return operations


def get_levenshtein_distance_matrix(comparable: Union[str, List[str]],
                                    base: Union[str, List[str]]) -> ndarray:
    """
    This function creates the Levenhstein distance matrix for the given
    comparable object and the given base object.
    """

    comparable, base = _lower_input(comparable, base)
    comparable_len = len(comparable)
    base_len = len(base)
    distance_matrix: ndarray = zeros(
        (comparable_len + 1, base_len + 1), dtype=int)

    for i in range(comparable_len + 1):
        distance_matrix[i, 0] = i

    for j in range(base_len + 1):
        distance_matrix[0, j] = j

    for i in range(comparable_len):
        for j in range(base_len):
            if comparable[i] == base[j]:
                cost = 0
            else:
                cost = 1

            distance_matrix[i + 1, j + 1] = min(distance_matrix[i, j + 1] + 1,
                                                distance_matrix[i + 1, j] + 1,
                                                distance_matrix[i, j] + cost)

    return distance_matrix
