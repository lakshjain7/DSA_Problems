"""
Problem: 11. Container With Most Water
Difficulty: Medium
Topics: Array, Two Pointers, Greedy

Problem Statement:
    You are given an integer array height of length n. There are n vertical lines
    drawn such that the two endpoints of the i-th line are (i, 0) and (i, height[i]).
    Find two lines that together with the x-axis form a container, such that the
    container contains the most water.
    Return the maximum amount of water a container can store.
    Notice that you may not slant the container.

Examples:
    Input: height = [1,8,6,2,5,4,8,3,7]
    Output: 49

    Input: height = [1,1]
    Output: 1

Constraints:
    - n == height.length
    - 2 <= n <= 10^5
    - 0 <= height[i] <= 10^4

Approach:
    Two Pointers (Greedy): Start with widest container (left=0, right=n-1).
    Always move the pointer at the shorter side inward.

Complexity:
    Time:  O(n) — single pass
    Space: O(1)
"""

from typing import List


def maxArea(height: List[int]) -> int:
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        width = right - left
        current_water = min(height[left], height[right]) * width
        max_water = max(max_water, current_water)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water


def maxArea_brute(height: List[int]) -> int:
    n = len(height)
    max_water = 0
    for i in range(n):
        for j in range(i + 1, n):
            max_water = max(max_water, min(height[i], height[j]) * (j - i))
    return max_water


if __name__ == "__main__":
    assert maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert maxArea([1, 1]) == 1
    assert maxArea([5, 5, 5, 5]) == 15
    assert maxArea([1, 2, 3, 4, 5]) == 6
    assert maxArea([5, 4, 3, 2, 1]) == 6
    assert maxArea([1, 100, 1]) == 2
    test = [3, 9, 3, 4, 7, 2, 12, 6]
    assert maxArea(test) == maxArea_brute(test)
    assert maxArea([0, 0]) == 0
    assert maxArea([0, 10]) == 0
    print("All tests passed for 11. Container With Most Water!")
