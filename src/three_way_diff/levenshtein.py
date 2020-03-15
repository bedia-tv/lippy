'''
This module defines the functions to compute the Levenshtein distance between
two objects of type List[str].
The functions defined are:
- get_operations
- get_levenshtein_distance_matrix
'''

from typing import List, Tuple
from numpy import argmin, ndarray, zeros


def get_levenshtein_distance_matrix(comparable: List[str],
                                    base: List[str]) -> ndarray:
    '''
    This function creates the Levenhstein distance matrix for the given
    comparable list of strings and the given base list of strings.
    '''
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


def get_operations(comparable: List[str], base: List[str]) \
        -> List[Tuple[str, int, int]]:
    '''
    This function gets the required operations to get from the given
    comparable list of strings to the given base list of strings.
    The operations are in format (operation_type, index_comparable,
    index_base).
    '''
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
