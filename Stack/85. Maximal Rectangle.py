"""
Problem: 85. Maximal Rectangle
Difficulty: Hard
Topics: Stack, Dynamic Programming, Array, Matrix

Problem Statement:
Given a rows x cols binary matrix filled with '0's and '1's, find the largest
rectangle containing only '1's and return its area.

Examples:
    Input: matrix = [["1","0","1","0","0"],
                     ["1","0","1","1","1"],
                     ["1","1","1","1","1"],
                     ["1","0","0","1","0"]]
    Output: 6

    Input: matrix = [["0"]]
    Output: 0

    Input: matrix = [["1"]]
    Output: 1

Constraints:
    - rows == matrix.length
    - cols == matrix[i].length
    - 1 <= rows, cols <= 200
    - matrix[i][j] is '0' or '1'

Approach (Stack — Histogram Reduction):
    Reduce 2D problem to repeated 1D "Largest Rectangle in Histogram" (LeetCode 84).

    For each row i, build a heights[] array where heights[j] = number of
    consecutive '1's ending at row i in column j (reset to 0 if matrix[i][j]=='0').
    Then run a monotonic-stack histogram algorithm on heights to find the max area
    achievable with that row as the base.

    Histogram algorithm: maintain a stack of (start_index, height) pairs in
    increasing height order. When a bar shorter than the stack top is encountered,
    pop and compute area = height * (current_index - start_index).

    Time: O(m * n) — O(n) histogram work per row
    Space: O(n) — heights array + stack

Alternative (DP — Left/Right/Height arrays):
    For each cell, track:
        height[j]  = consecutive '1's ending at current row in column j
        left[j]    = leftmost column index where height[j] can extend
        right[j]   = rightmost column index (exclusive) where height[j] can extend
    Area at (i, j) = height[j] * (right[j] - left[j])

    Time: O(m * n), Space: O(n)
"""

from typing import List


def maximalRectangle(matrix: List[List[str]]) -> int:
    """Stack approach: reduce to Largest Rectangle in Histogram per row."""
    if not matrix or not matrix[0]:
        return 0

    cols = len(matrix[0])
    heights = [0] * cols
    max_area = 0

    for row in matrix:
        # Update running histogram heights
        for j in range(cols):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0

        max_area = max(max_area, _largest_rect_in_histogram(heights))

    return max_area


def _largest_rect_in_histogram(heights: List[int]) -> int:
    """Monotonic stack — O(n) largest rectangle in histogram."""
    # Append sentinel 0 so all remaining bars get processed at the end
    bars = heights + [0]
    stack: List[tuple] = []   # (start_idx, height)
    max_area = 0

    for i, h in enumerate(bars):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx          # extend left to where this popped bar began
        stack.append((start, h))

    return max_area


def maximalRectangle_dp(matrix: List[List[str]]) -> int:
    """DP approach with left/right/height boundary arrays."""
    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols
    lefts  = [0] * cols          # left boundary (inclusive)
    rights = [cols] * cols       # right boundary (exclusive)
    max_area = 0

    for i in range(rows):
        # Update heights
        for j in range(cols):
            heights[j] = heights[j] + 1 if matrix[i][j] == '1' else 0

        # Update left boundaries (sweep left -> right)
        cur_left = 0
        for j in range(cols):
            if matrix[i][j] == '1':
                lefts[j] = max(lefts[j], cur_left)  # tighten from stored + current row
            else:
                lefts[j] = 0
                cur_left = j + 1

        # Update right boundaries (sweep right -> left)
        cur_right = cols
        for j in range(cols - 1, -1, -1):
            if matrix[i][j] == '1':
                rights[j] = min(rights[j], cur_right)
            else:
                rights[j] = cols
                cur_right = j

        # Compute max area
        for j in range(cols):
            max_area = max(max_area, heights[j] * (rights[j] - lefts[j]))

    return max_area


if __name__ == "__main__":
    # Test 1: standard case, answer = 6
    m1 = [["1","0","1","0","0"],
          ["1","0","1","1","1"],
          ["1","1","1","1","1"],
          ["1","0","0","1","0"]]
    assert maximalRectangle(m1) == 6, "Test 1 stack"
    assert maximalRectangle_dp(m1) == 6, "Test 1 DP"

    # Test 2: single '0'
    assert maximalRectangle([["0"]]) == 0, "Test 2 stack"
    assert maximalRectangle_dp([["0"]]) == 0, "Test 2 DP"

    # Test 3: single '1'
    assert maximalRectangle([["1"]]) == 1, "Test 3 stack"
    assert maximalRectangle_dp([["1"]]) == 1, "Test 3 DP"

    # Test 4: all ones 2x2 -> 4
    m4 = [["1","1"],["1","1"]]
    assert maximalRectangle(m4) == 4, "Test 4 stack"
    assert maximalRectangle_dp(m4) == 4, "Test 4 DP"

    # Test 5: single row all ones -> width
    m5 = [["1","1","1","1"]]
    assert maximalRectangle(m5) == 4, "Test 5 stack"
    assert maximalRectangle_dp(m5) == 4, "Test 5 DP"

    # Test 6: L-shaped — max rect is the bottom row
    m6 = [["1","0"],
          ["1","0"],
          ["1","1"]]
    assert maximalRectangle(m6) == 3, "Test 6 stack"
    assert maximalRectangle_dp(m6) == 3, "Test 6 DP"

    # Test 7: entire 3x3 of ones -> 9
    m7 = [["1","1","1"],["1","1","1"],["1","1","1"]]
    assert maximalRectangle(m7) == 9, "Test 7 stack"
    assert maximalRectangle_dp(m7) == 9, "Test 7 DP"

    print("All tests passed!")
