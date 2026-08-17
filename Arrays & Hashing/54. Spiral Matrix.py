"""
54. Spiral Matrix
Difficulty: Medium
Topics: Array, Matrix, Simulation

Problem Statement
-----------------
Given an m x n matrix, return all elements of the matrix in spiral order.

Example 1:
    Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
    Output: [1,2,3,6,9,8,7,4,5]

Example 2:
    Input:  matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    Output: [1,2,3,4,8,12,11,10,9,5,6,7]

Constraints:
    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 10
    -100 <= matrix[i][j] <= 100


Approach (Boundary Shrinking)
-----------------------------
Maintain four boundaries: top, bottom, left, right. Repeatedly walk the
outer ring in the order right -> down -> left -> up, and after finishing
each edge shrink the corresponding boundary inward. Stop as soon as the
boundaries cross.

Why it works:
- Each of the four directional sweeps consumes exactly one row or column
  and then retreats that boundary, so every cell is visited exactly once.
- The two guard checks (top <= bottom and left <= right) before the
  leftward and upward sweeps prevent double-counting the middle row/column
  when the matrix is not square (e.g. a single remaining row or column).

Complexity
----------
Time:  O(m * n) - every element is appended once.
Space: O(1) extra (ignoring the output list of size m * n).
"""

from typing import List


def spiralOrder(matrix: List[List[int]]) -> List[int]:
    if not matrix or not matrix[0]:
        return []

    result: List[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Traverse the top row, left -> right.
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        # Traverse the right column, top -> bottom.
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        # Traverse the bottom row, right -> left (if a row remains).
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        # Traverse the left column, bottom -> top (if a column remains).
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result


def spiralOrder_layers(matrix: List[List[int]]) -> List[int]:
    """
    Alternative approach: peel off the first row, then rotate the rest
    counter-clockwise and recurse/iterate. Concise but uses O(m*n) extra
    work for the rotations. Included to contrast with the boundary method.
    """
    result: List[int] = []
    m = [row[:] for row in matrix]  # copy so we do not mutate the input
    while m:
        result += m.pop(0)              # take the top row
        m = [list(row) for row in zip(*m)][::-1]  # rotate remainder CCW
    return result


if __name__ == "__main__":
    # Example 1
    assert spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]

    # Example 2
    assert spiralOrder([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == \
        [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]

    # Single element
    assert spiralOrder([[7]]) == [7]

    # Single row
    assert spiralOrder([[1, 2, 3, 4]]) == [1, 2, 3, 4]

    # Single column
    assert spiralOrder([[1], [2], [3], [4]]) == [1, 2, 3, 4]

    # Non-square, more rows than cols
    assert spiralOrder([[1, 2], [3, 4], [5, 6]]) == [1, 2, 4, 6, 5, 3]

    # 2x2
    assert spiralOrder([[1, 2], [3, 4]]) == [1, 2, 4, 3]

    # Cross-check the alternative implementation on the same cases.
    cases = [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
        [[7]],
        [[1, 2, 3, 4]],
        [[1], [2], [3], [4]],
        [[1, 2], [3, 4], [5, 6]],
        [[1, 2], [3, 4]],
    ]
    for c in cases:
        assert spiralOrder(c) == spiralOrder_layers(c)

    print("All tests passed for 54. Spiral Matrix")
