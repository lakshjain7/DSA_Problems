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
    Explanation: Lines at index 1 (h=8) and index 8 (h=7) form container of width 7,
                 min(8,7)*7 = 49.

    Input: height = [1,1]
    Output: 1

Constraints:
    - n == height.length
    - 2 <= n <= 10^5
    - 0 <= height[i] <= 10^4

Approach:
    Two Pointers (Greedy):
    Start with the widest possible container (left=0, right=n-1).
    At each step, the area = min(height[left], height[right]) * (right - left).
    Moving the pointer with the GREATER height inward cannot improve results because:
      - width decreases by 1 regardless
      - the height is already bounded by the shorter side
    So we always move the pointer at the SHORTER side inward, hoping to find a taller line.
    This guarantees we never skip an optimal pair.

Complexity:
    Time:  O(n) — single pass, two pointers move inward
    Space: O(1) — only two pointer variables

Alternative Approach:
    Brute force — try all pairs, O(n^2) time. Not acceptable for large inputs.
"""

from typing import List


def maxArea(height: List[int]) -> int:
    """
    Two-pointer approach to find maximum water container area.

    Args:
        height: List of non-negative integers representing line heights.

    Returns:
        Maximum water that can be contained.
    """
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        # Current area: width * min height
        width = right - left
        current_water = min(height[left], height[right]) * width
        max_water = max(max_water, current_water)

        # Move the shorter side inward (greedy: taller side can only help)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water


def maxArea_brute(height: List[int]) -> int:
    """
    Alternative: Brute force O(n^2) — for verification only.
    """
    n = len(height)
    max_water = 0
    for i in range(n):
        for j in range(i + 1, n):
            max_water = max(max_water, min(height[i], height[j]) * (j - i))
    return max_water


if __name__ == "__main__":
    # Basic examples
    assert maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert maxArea([1, 1]) == 1

    # All same height
    assert maxArea([5, 5, 5, 5]) == 15  # min(5,5)*3 = 15

    # Increasing heights — best is last two? No: widest pair matters
    assert maxArea([1, 2, 3, 4, 5]) == 6
    # pairs: (0,4)=min(1,5)*4=4, (1,4)=min(2,5)*3=6, (2,4)=min(3,5)*2=6, (3,4)=min(4,5)*1=4
    # max = 6 ✓

    # Decreasing heights
    assert maxArea([5, 4, 3, 2, 1]) == 6  # symmetric to above

    # Single tall spike in middle
    assert maxArea([1, 100, 1]) == 2  # min(1,1)*2=2

    # Verify two-pointer matches brute force on random-ish case
    test = [3, 9, 3, 4, 7, 2, 12, 6]
    assert maxArea(test) == maxArea_brute(test)

    # Minimum input
    assert maxArea([0, 0]) == 0
    assert maxArea([0, 10]) == 0

    print("All tests passed for 11. Container With Most Water!")
