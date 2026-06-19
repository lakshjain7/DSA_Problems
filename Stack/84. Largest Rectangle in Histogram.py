"""
Problem 84: Largest Rectangle in Histogram
Difficulty: Hard
Topics: Stack, Arrays, Monotonic Stack

Given heights, return the area of the largest rectangle in the histogram.
Example: heights = [2,1,5,6,2,3] -> 10

Approach: Monotonic Increasing Stack — O(n) time, O(n) space
For each bar, track (height, start_index). When a shorter bar appears,
pop and compute area. Sentinel 0 flushes remaining stack.
"""

from typing import List


def largest_rectangle_area(heights: List[int]) -> int:
    max_area = 0
    stack: List[tuple] = []

    for i, h in enumerate(heights + [0]):
        start = i
        while stack and stack[-1][0] >= h:
            height, start = stack.pop()
            max_area = max(max_area, height * (i - start))
        stack.append((h, start))

    return max_area


def largest_rectangle_area_boundaries(heights: List[int]) -> int:
    n = len(heights)
    left = [-1] * n
    right = [n] * n

    stack: List[int] = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

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
    assert largest_rectangle_area([1]) == 1
    assert largest_rectangle_area([0]) == 0
    assert largest_rectangle_area([5, 5, 5, 5]) == 20
    assert largest_rectangle_area([1, 2, 3, 4, 5]) == 9
    assert largest_rectangle_area([5, 4, 3, 2, 1]) == 9
    assert largest_rectangle_area([0, 0, 0]) == 0
    assert largest_rectangle_area([6, 2, 5, 4, 5, 1, 6]) == 12
    test_cases = [[2, 1, 5, 6, 2, 3], [2, 4], [5, 5, 5, 5], [1, 2, 3, 4, 5], [6, 2, 5, 4, 5, 1, 6], [1], [0, 1, 0]]
    for tc in test_cases:
        assert largest_rectangle_area(tc) == largest_rectangle_area_boundaries(tc)
    print("All tests passed for 84. Largest Rectangle in Histogram")
