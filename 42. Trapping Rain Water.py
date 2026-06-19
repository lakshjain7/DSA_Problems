"""
42. Trapping Rain Water
Difficulty: Hard
Topics: Array, Two Pointers, Stack, Dynamic Programming

=== PROBLEM ===
Given n non-negative integers representing an elevation map where the width
of each bar is 1, compute how much water it can trap after raining.

Example 1:
    Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6

Example 2:
    Input:  height = [4,2,0,3,2,5]
    Output: 9

Constraints:
    n == height.length
    1 <= n <= 2 * 10^4
    0 <= height[i] <= 10^5

=== APPROACH: Two Pointers (Optimal) ===

Key Insight:
    Water trapped at index i = min(max_left[i], max_right[i]) - height[i]

    Instead of precomputing both max arrays (O(n) space), use two pointers:
    - left pointer starts at 0, right pointer starts at n-1
    - Track max_left (tallest bar seen from left so far)
         and max_right (tallest bar seen from right so far)
    - At each step, process the side with the SMALLER max:
        * If max_left <= max_right:
            water at left = max_left - height[left]   (max_right is guaranteed ≥ max_left)
            left++
        * Else:
            water at right = max_right - height[right]
            right--

    Why the smaller-height-side is safe:
        The water at a position is bounded by min(max_left, max_right).
        When height[left] <= height[right], the right wall is at least as
        tall as the left wall RIGHT NOW, so the limiting factor for the
        current left position is max_left (not max_right).
        We can safely compute water[left] = max_left - height[left].
        Key: compare CURRENT heights, not running maxes — this ensures
        we never leave a position unvisited before both pointers meet.

Algorithm:
    left, right = 0, n-1
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

Complexity:
    Time:  O(n) — single pass
    Space: O(1) — no extra arrays

=== ALTERNATIVE: Monotonic Stack ===
    Process bars left to right. Maintain a stack of indices with
    decreasing heights. When current bar is taller than stack top,
    we found a valley; compute trapped water between the popped bar
    and the new bar. Also O(n) time, O(n) space.
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


# ─── Monotonic Stack alternative (for reference) ─────────────────────────────
def trap_stack(height: List[int]) -> int:
    stack = []   # indices, heights non-increasing
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


# ─── Tests ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9
    assert trap([]) == 0
    assert trap([3, 0, 2, 0, 4]) == 7
    assert trap([1, 0, 1]) == 1

    # Veri