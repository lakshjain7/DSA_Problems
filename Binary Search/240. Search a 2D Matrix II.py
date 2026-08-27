"""
240. Search a 2D Matrix II
Difficulty: Medium
Topics: Array, Binary Search, Divide and Conquer, Matrix

Problem Statement
-----------------
Write an efficient algorithm that searches for a target value in an m x n
integer matrix `matrix`. This matrix has the following properties:

    - Integers in each row are sorted in ascending order from left to right.
    - Integers in each column are sorted in ascending order from top to bottom.

Return True if `target` is found in the matrix, otherwise return False.

Example 1:
    Input: matrix = [[1,4,7,11,15],
                     [2,5,8,12,19],
                     [3,6,9,16,22],
                     [10,13,14,17,24],
                     [18,21,23,26,30]], target = 5
    Output: True

Example 2:
    Input: matrix = [[1,4,7,11,15],
                     [2,5,8,12,19],
                     [3,6,9,16,22],
                     [10,13,14,17,24],
                     [18,21,23,26,30]], target = 20
    Output: False

Constraints:
    m == matrix.length
    n == matrix[i].length
    1 <= n, m <= 300
    -10^9 <= matrix[i][j] <= 10^9
    All the integers in each row are sorted in ascending order.
    All the integers in each column are sorted in ascending order.
    -10^9 <= target <= 10^9

Approach (Staircase Search)
---------------------------
Start from the top-right corner of the matrix (row = 0, col = n - 1).
At every position the value there is the largest in its row and the smallest
in its column, which lets us eliminate a whole row or column each step:

    - If matrix[row][col] == target -> found it.
    - If matrix[row][col] > target  -> the whole column is too big; move left.
    - If matrix[row][col] < target  -> the whole row is too small; move down.

Each move discards one row or one column, so we make at most m + n moves.
This "staircase" walk is why the corner start works: only the top-right
(or symmetrically bottom-left) corner is simultaneously a row-max and a
column-min, giving an unambiguous direction to prune.

Complexity
----------
Time:  O(m + n) - at most one step per row plus one per column.
Space: O(1)     - only two index variables.

Alternative Approach (Binary Search per row)
--------------------------------------------
Run a standard binary search on each of the m rows: O(m log n). The staircase
method is asymptotically better and simpler, but the per-row binary search is
included below as a cross-check for testing.
"""

from typing import List
import bisect


def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    row, col = 0, cols - 1  # start at top-right corner

    while row < rows and col >= 0:
        val = matrix[row][col]
        if val == target:
            return True
        elif val > target:
            col -= 1  # eliminate this column
        else:
            row += 1  # eliminate this row

    return False


def searchMatrixBinary(matrix: List[List[int]], target: int) -> bool:
    """Alternative: binary search each row independently. O(m log n)."""
    if not matrix or not matrix[0]:
        return False

    for r in matrix:
        idx = bisect.bisect_left(r, target)
        if idx < len(r) and r[idx] == target:
            return True
    return False


if __name__ == "__main__":
    m1 = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]

    for fn in (searchMatrix, searchMatrixBinary):
        # Example cases
        assert fn(m1, 5) is True
        assert fn(m1, 20) is False

        # Corner / boundary values
        assert fn(m1, 1) is True    # top-left
        assert fn(m1, 30) is True   # bottom-right
        assert fn(m1, 18) is True   # bottom-left
        assert fn(m1, 15) is True   # top-right
        assert fn(m1, 0) is False   # smaller than all
        assert fn(m1, 31) is False  # larger than all

        # Single element
        assert fn([[7]], 7) is True
        assert fn([[7]], 3) is False

        # Single row / single column
        assert fn([[1, 3, 5, 7, 9]], 7) is True
        assert fn([[1, 3, 5, 7, 9]], 8) is False
        assert fn([[1], [3], [5], [7]], 5) is True
        assert fn([[1], [3], [5], [7]], 4) is False

        # Empty-ish inputs
        assert fn([], 1) is False
        assert fn([[]], 1) is False

        # Negative numbers
        assert fn([[-5, -4], [-3, -2]], -4) is True
        assert fn([[-5, -4], [-3, -2]], -1) is False

    print("All tests passed for 240. Search a 2D Matrix II")
