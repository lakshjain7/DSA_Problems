"""
42. Trapping Rain Water
Difficulty: Hard
Topics: Array, Two Pointers, Stack, Dynamic Programming

Problem Statement:
Given n non-negative integers representing an elevation map where the width
of each bar is 1, compute how much water it can trap after raining.

Example 1:
    Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6

Example 2:
    Input:  height = [4,2,0,3,2,5]
    Output: 9

Approach: Two Pointers (Optimal) — O(n) time, O(1) space
Water at index i = min(max_left[i], max_right[i]) - height[i]
Process the side with the smaller max, since that's the limiting factor.

Alternative: Monotonic Stack — O(n) time, O(n) space
"""

from typing import List


def trap(height: List[int]) -> int:
    if not height:
        return 0

    left, right = 0, len(height) - 1
    max_left = max_right = 0
    water = 0

    while left < right:
        if height[left] <= height[right]:
            max_left = max(max_left, height[left])
            water += max_left - height[left]
            left += 1
        else:
            max_right = max(max_right, height[right])
            water += max_right - height[right]
            right -= 1

    return water


def trap_stack(height: List[int]) -> int:
    stack = []
    water = 0

    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            if not stack:
                break
            width = i - stack[-1] - 1
            bounded_height = min(h, height[stack[-1]]) - height[bottom]
            water += width * bounded_height

        stack.append(i)

    return water


if __name__ == "__main__":
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9
    assert trap([]) == 0
    assert trap([3, 0, 2, 0, 4]) == 7
    assert trap([1, 0, 1]) == 1
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == trap_stack([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    print("All tests passed!")
