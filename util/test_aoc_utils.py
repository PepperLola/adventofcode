import numpy as np
import pytest
import aoc_utils

def test_find_grid_basic():
    grid = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ], dtype=np.int64)

    pat = np.array([
        [5, 6],
        [8, 9]
    ], dtype=np.int64)

    result = aoc_utils.find_grid(grid, pat)
    assert result == (1, 1)

def test_find_grid_not_found():
    grid = np.array([
        [1, 2],
        [3, 4]
    ], dtype=np.int64)

    pat = np.array([
        [5]
    ], dtype=np.int64)

    result = aoc_utils.find_grid(grid, pat)
    assert result is None

def test_find_all_grid_basic():
    grid = np.array([
        [1, 2, 1],
        [2, 1, 2],
        [1, 2, 1]
    ], dtype=np.int64)

    pat = np.array([[1, 2]], dtype=np.int64)

    result = aoc_utils.find_all_grid(grid, pat, max_matches=10)
    expected = [(0,0), (1,1), (0,2)]
    assert result == expected

def test_find_all_grid_max_matches():
    grid = np.ones((10,10), dtype=np.int64)
    pat = np.ones((1,1), dtype=np.int64)

    # limiting max_matches
    result = aoc_utils.find_all_grid(grid, pat, max_matches=5)
    assert len(result) == 5

def test_letter_grid():
    lines = ["abc", "def", "ghi"]

    result = aoc_utils.letter_grid(lines)
    expected = [["a", "b", "c"],
                ["d", "e", "f"],
                ["g", "h", "i"]]
    assert len(result) == 3
    assert result == expected

def test_number_grid():
    lines = ["123", "456", "789"]

    result = aoc_utils.number_grid(lines)
    expected = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]]
    assert len(result) == 3
    assert result == expected
