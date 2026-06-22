"""
Problem 74: Search a 2D Matrix
Difficulty: Medium
Topics: Array, Binary Search, Matrix

Problem Statement:
You are given an m x n integer matrix 'matrix' with the following two properties:
  - Each row is sorted in non-decreasing order.
  - The first integer of each row is greater than the last integer of the previous row.
Given an integer 'target', return True if target is in matrix or False otherwise.
You must write a solution in O(log(m * n)) time complexity.

Examples:
  Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
  Output: True

  Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
  Output: False

Constraints:
  m == matrix.length
  n == matrix[i].length
  1 <= m, n <= 100
  -10^4 <= matrix[i][j] <= 10^4
  -10^4 <= target <= 10^4

Approach:
  Treat the 2D matrix as a 1D sorted array of length m*n.
  Use binary search over indices [0, m*n - 1].
  For a mid index i, the corresponding row is i // n and column is i % n.
  This gives O(log(m*n)) = O(log m + log n) time.

Complexity:
  Time:  O(log(m * n))
  Space: O(1)

Alternative Approach:
  Two-pass binary search:
    1. Binary search for the correct row (find the row where first <= target <= last).
    2. Binary search within that row.
  Same time complexity but two separate passes. Slightly more code.
"""

from typing import List


def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    """Single binary search treating the matrix as a flat sorted array."""
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return False


def searchMatrix_two_pass(matrix: List[List[int]], target: int) -> bool:
    """Alternative: binary search for row, then binary search within row."""
    m, n = len(matrix), len(matrix[0])

    # Find the row
    top, bot = 0, m - 1
    row = -1
    while top <= bot:
        mid = (top + bot) // 2
        if matrix[mid][0] <= target <= matrix[mid][-1]:
            row = mid
            break
        elif target < matrix[mid][0]:
            bot = mid - 1
        else:
            top = mid + 1

    if row == -1:
        return False

    # Binary search within the row
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if matrix[row][mid] == target:
            return True
        elif matrix[row][mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return False


if __name__ == "__main__":
    # Basic cases
    assert searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3) is True
    assert searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13) is False

    # Target at boundaries
    assert searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 1) is True
    assert searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 60) is True
    assert searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 0) is False
    assert searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 61) is False

    # Single cell
    assert searchMatrix([[1]], 1) is True
    assert searchMatrix([[1]], 2) is False

    # Single row
    assert searchMatrix([[1, 3, 5]], 3) is True
    assert searchMatrix([[1, 3, 5]], 4) is False

    # Single column
    assert searchMatrix([[1], [3], [5]], 3) is True
    assert searchMatrix([[1], [3], [5]], 4) is False

    # Test alternative approach
    assert searchMatrix_two_pass([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3) is True
    assert searchMatrix_two_pass([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13) is False

    print("All tests passed!")
