"""
73. Set Matrix Zeroes
Difficulty: Medium
Topics: Array, Hash Table, Matrix

Problem Statement
-----------------
Given an m x n integer matrix `matrix`, if an element is 0, set its entire row
and column to 0's.

You must do it in place.

Examples
--------
Example 1:
    Input:  matrix = [[1,1,1],[1,0,1],[1,1,1]]
    Output: [[1,0,1],[0,0,0],[1,0,1]]

Example 2:
    Input:  matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
    Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]

Constraints
-----------
    m == matrix.length
    n == matrix[0].length
    1 <= m, n <= 200
    -2^31 <= matrix[i][j] <= 2^31 - 1

Follow up:
    - A straightforward solution using O(mn) space is probably a bad idea.
    - A simple improvement uses O(m + n) space, but still not the best.
    - Could you devise a constant-space solution?

Approach (O(1) extra space)
---------------------------
The trick is to reuse the matrix's own first row and first column as marker
storage, so no extra arrays are needed.

  1. First, record separately whether the first row and first column each
     originally contain a zero (two booleans), because we are about to overwrite
     them as markers.
  2. Scan the inner submatrix (rows 1..m-1, cols 1..n-1). Whenever
     matrix[i][j] == 0, mark matrix[i][0] = 0 and matrix[0][j] = 0.
  3. Scan the inner submatrix again. Zero out matrix[i][j] if its row marker
     matrix[i][0] == 0 or its column marker matrix[0][j] == 0.
  4. Finally, using the two saved booleans, zero the first row and/or first
     column if they originally held a zero.

Why it works: the first row/column act as a per-column / per-row "should be
zeroed" flag. Processing the interior before the borders prevents the markers
from being clobbered prematurely; the two saved booleans handle the borders
themselves, which cannot use themselves as their own markers.

Complexity
----------
Time:  O(m * n) - a constant number of full passes over the matrix.
Space: O(1)     - only two boolean flags beyond the input.
"""

from typing import List


def set_zeroes(matrix: List[List[int]]) -> None:
    """Modify `matrix` in place, zeroing the row and column of every zero."""
    if not matrix or not matrix[0]:
        return

    m, n = len(matrix), len(matrix[0])
    first_row_has_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_has_zero = any(matrix[i][0] == 0 for i in range(m))

    # Use borders as markers for the interior.
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # Apply markers to the interior.
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # Handle the first row and first column.
    if first_row_has_zero:
        for j in range(n):
            matrix[0][j] = 0
    if first_col_has_zero:
        for i in range(m):
            matrix[i][0] = 0


# ---------------------------------------------------------------------------
# Alternative approach: O(m + n) space using explicit marker sets. Simpler to
# reason about; often the expected "improvement" answer before the O(1) trick.
# ---------------------------------------------------------------------------
def set_zeroes_sets(matrix: List[List[int]]) -> None:
    if not matrix or not matrix[0]:
        return
    m, n = len(matrix), len(matrix[0])
    zero_rows, zero_cols = set(), set()
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                zero_rows.add(i)
                zero_cols.add(j)
    for i in range(m):
        for j in range(n):
            if i in zero_rows or j in zero_cols:
                matrix[i][j] = 0


if __name__ == "__main__":
    import copy

    cases = [
        ([[1, 1, 1], [1, 0, 1], [1, 1, 1]],
         [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
        ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],
         [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]),
        ([[1]], [[1]]),
        ([[0]], [[0]]),
        ([[1, 2, 3]], [[1, 2, 3]]),               # single row, no zero
        ([[1, 0, 3]], [[0, 0, 0]]),               # single row with zero
        ([[1], [2], [0]], [[0], [0], [0]]),        # single col with zero
        ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),      # no zeros at all
        ([[5, 0], [0, 5]], [[0, 0], [0, 0]]),      # zeros on both borders
    ]

    for fn in (set_zeroes, set_zeroes_sets):
        for grid, expected in cases:
            work = copy.deepcopy(grid)
            fn(work)
            assert work == expected, (fn.__name__, grid, work, expected)

    print("All tests passed.")
