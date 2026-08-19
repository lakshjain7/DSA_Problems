"""
48. Rotate Image
Difficulty: Medium
Topics: Array, Math, Matrix

Problem Statement
-----------------
You are given an n x n 2D matrix representing an image. Rotate the image by
90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input
2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.

Examples
--------
Example 1:
    Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
    Output: [[7,4,1],[8,5,2],[9,6,3]]

Example 2:
    Input:  matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
    Output: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]

Constraints
-----------
    n == matrix.length == matrix[i].length
    1 <= n <= 20
    -1000 <= matrix[i][j] <= 1000

Approach
--------
A clockwise 90-degree rotation can be decomposed into two in-place operations:

    1. Transpose the matrix (swap matrix[i][j] with matrix[j][i]). This turns
       rows into columns.
    2. Reverse each row.

Why it works: After transposing, the element originally at (i, j) moves to
(j, i). Reversing each row then maps column index j -> n-1-j. Composing the two
maps sends (i, j) -> (j, n-1-i), which is exactly the position an element takes
under a clockwise 90-degree rotation. Because both steps operate on the matrix
itself using only swaps, no extra 2D buffer is required.

Complexity
----------
Time:  O(n^2) - every cell is touched a constant number of times.
Space: O(1)   - rotation is done in place; only scalar temporaries are used.
"""

from typing import List
from copy import deepcopy


def rotate(matrix: List[List[int]]) -> None:
    """Rotate the n x n matrix 90 degrees clockwise, in place."""
    n = len(matrix)

    # Step 1: transpose in place (only iterate the upper triangle).
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: reverse each row.
    for row in matrix:
        row.reverse()


def rotate_layers(matrix: List[List[int]]) -> None:
    """
    Alternative: rotate the matrix ring by ring (four-way cyclic swap).

    For each concentric layer, rotate four elements at a time using a single
    temporary. This performs the rotation directly without a transpose step.
    """
    n = len(matrix)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            offset = i - first
            top = matrix[first][i]                                     # save top
            matrix[first][i] = matrix[last - offset][first]            # left -> top
            matrix[last - offset][first] = matrix[last][last - offset]  # bottom -> left
            matrix[last][last - offset] = matrix[i][last]              # right -> bottom
            matrix[i][last] = top                                      # top -> right


if __name__ == "__main__":
    def expected_rotation(mat: List[List[int]]) -> List[List[int]]:
        n = len(mat)
        return [[mat[n - 1 - j][i] for j in range(n)] for i in range(n)]

    test_cases = [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],
        [[1]],
        [[1, 2], [3, 4]],
        [[-1000, 1000], [0, 500]],
    ]

    # Verify known outputs explicitly.
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate(m1)
    assert m1 == [[7, 4, 1], [8, 5, 2], [9, 6, 3]], m1

    m2 = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    rotate(m2)
    assert m2 == [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]], m2

    # Cross-check both approaches against a reference rotation.
    for tc in test_cases:
        ref = expected_rotation(tc)

        a = deepcopy(tc)
        rotate(a)
        assert a == ref, (tc, a, ref)

        b = deepcopy(tc)
        rotate_layers(b)
        assert b == ref, (tc, b, ref)

    # Four rotations return to the original matrix.
    original = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    spun = deepcopy(original)
    for _ in range(4):
        rotate(spun)
    assert spun == original, spun

    print("All tests passed for 48. Rotate Image")
