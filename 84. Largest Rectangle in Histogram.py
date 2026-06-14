"""
Problem 84: Largest Rectangle in Histogram
Difficulty: Hard
Topics: Stack, Arrays, Monotonic Stack

Problem Statement:
Given an array of integers heights representing the histogram's bar height where
the width of each bar is 1, return the area of the largest rectangle in the histogram.

Examples:
    Input: heights = [2,1,5,6,2,3]
    Output: 10
    Explanation: The largest rectangle spans bars at indices 2 and 3 (heights 5,6),
                 giving area = 5 * 2 = 10.

    Input: heights = [2,4]
    Output: 4

Constraints:
    - 1 <= heights.length <= 10^5
    - 0 <= heights[i] <= 10^4

Approach (Monotonic Stack, O(n)):
    For each bar, the rectangle it can anchor is bounded by:
    - The nearest shorter bar to its LEFT  (left boundary)
    - The nearest shorter bar to its RIGHT (right boundary)

    Use an increasing monotonic stack of (height, start_index).
    Iterate through heights, appending a sentinel 0 at the end to flush the stack.

    When we encounter a bar shorter than the stack top:
    - Pop the stack top — its right boundary is the current index.
    - Its left boundary extends back to where the popped element "started"
      (tracked by the `start` variable, since the popped element could have
       been reached from positions left of its actual index after prior pops).
    - Compute area = height * (current_index - start).

    This gives the maximal rectangle each height can form as a base.

Complexity:
    Time:  O(n) — each bar is pushed and popped at most once
    Space: O(n) — stack can hold up to n elements
"""

from typing import List


def largest_rectangle_area(heights: List[int]) -> int:
    """Monotonic increasing stack approach."""
    max_area = 0
    # Stack stores (height, start_index)
    stack: List[tuple] = []

    for i, h in enumerate(heights + [0]):  # sentinel 0 flushes remaining stack
        start = i
        while stack and stack[-1][0] >= h:
            height, start = stack.pop()
            max_area = max(max_area, height * (i - start))
        stack.append((h, start))

    return max_area


# Alternative Approach (Left/Right boundary arrays, O(n)):
# Precompute for each bar:
#   left[i]  = index of nearest bar to the left that is strictly shorter
#   right[i] = index of nearest bar to the right that is strictly shorter
# width[i] = right[i] - left[i] - 1
# area[i]  = heights[i] * width[i]
# Answer = max(area)
# Same O(n) time and space but requires two separate passes.

def largest_rectangle_area_boundaries(heights: List[int]) -> int:
    """Left/right boundary precomputation approach."""
    n = len(heights)
    left = [-1] * n   # index of nearest shorter bar to the left
    right = [n] * n   # index of nearest shorter bar to the right

    # Fill left boundaries
    stack: List[int] = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    # Fill right boundaries
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    return max(heights[i] * (right[i] - left[i] - 1) for i in range(n))


if __name__ == "__main__":
    assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle_area([2, 4]) == 4

    # Edge cases
    assert largest_rectangle_area([1]) == 1
    assert largest_rectangle_area([0]) == 0
    assert largest_rectangle_area([5, 5, 5, 5]) == 20   # full-width rectangle
    assert largest_rectangle_area([1, 2, 3, 4, 5]) == 9  # staircase: 3*3
    assert largest_rectangle_area([5, 4, 3, 2, 1]) == 9  # reverse staircase
    assert largest_rectangle_area([0, 0, 0]) == 0
    assert largest_rectangle_area([6, 2, 5, 4, 5, 1, 6]) == 12  # classic tricky case

    # Both approaches should agree
    test_cases = [
        [2, 1, 5, 6, 2, 3],
        [2, 4],
        [5, 5, 5, 5],
        [1, 2, 3, 4, 5],
        [6, 2, 5, 4, 5, 1, 6],
        [1],
        [0, 1, 0],
    ]
    for tc in test_cases:
        r1 = largest_rectangle_area(tc)
        r2 = largest_rectangle_area_boundaries(tc)
        assert r1 == r2, f"Mismatch on {tc}: {r1} vs {r2}"

    print("All tests passed for 84. Largest Rectangle in Histogram")
