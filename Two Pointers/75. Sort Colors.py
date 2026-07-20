"""
75. Sort Colors
Difficulty: Medium
Topics: Array, Two Pointers, Sorting

Problem Statement
-----------------
Given an array `nums` with n objects colored red, white, or blue, sort them
in-place so that objects of the same color are adjacent, with the colors in
the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and
blue, respectively.

You must solve this problem without using the library's sort function.

Examples
--------
Example 1:
    Input:  nums = [2, 0, 2, 1, 1, 0]
    Output: [0, 0, 1, 1, 2, 2]

Example 2:
    Input:  nums = [2, 0, 1]
    Output: [0, 1, 2]

Constraints
-----------
    n == nums.length
    1 <= n <= 300
    nums[i] is either 0, 1, or 2.

Follow up: Could you come up with a one-pass algorithm using only constant
extra space?

Approach (Dutch National Flag algorithm)
----------------------------------------
This is the classic Dutch National Flag problem posed by Edsger Dijkstra.
We maintain three regions in the array using three pointers:

    - [0, low)      -> all 0s (red)
    - [low, mid)    -> all 1s (white)
    - (high, n-1]   -> all 2s (blue)
    - [mid, high]   -> unclassified elements still to be scanned

We scan with `mid`:
    - If nums[mid] == 0: swap it into the 0s region (swap with `low`),
      then advance both low and mid. We advance mid because the element
      swapped from `low` was already scanned (it was a 1, since low <= mid).
    - If nums[mid] == 1: it is already in the right region; just advance mid.
    - If nums[mid] == 2: swap it into the 2s region (swap with `high`),
      then decrement high. We do NOT advance mid, because the element swapped
      in from `high` is unclassified and must be examined next.

The loop runs while mid <= high. Each element is examined a constant number
of times, giving a single pass.

Why it works: the invariants on the four regions are preserved by every
branch, and the unclassified region shrinks by at least one on every
iteration, so the algorithm terminates with a fully partitioned array.

Complexity
----------
Time:  O(n) - single pass, each step advances mid or decreases high.
Space: O(1) - sorting done in place with three pointers.
"""

from typing import List


def sort_colors(nums: List[int]) -> None:
    """Sort an array of 0s, 1s, and 2s in place (Dutch National Flag)."""
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1


def sort_colors_counting(nums: List[int]) -> None:
    """
    Alternative: counting sort (two-pass).

    Count the occurrences of 0, 1, and 2, then overwrite the array. Simpler
    to reason about but makes two passes over the data instead of one.

    Time: O(n), Space: O(1) (fixed-size count array of length 3).
    """
    counts = [0, 0, 0]
    for v in nums:
        counts[v] += 1

    i = 0
    for color in range(3):
        for _ in range(counts[color]):
            nums[i] = color
            i += 1


if __name__ == "__main__":
    # Example 1
    a = [2, 0, 2, 1, 1, 0]
    sort_colors(a)
    assert a == [0, 0, 1, 1, 2, 2], a

    # Example 2
    a = [2, 0, 1]
    sort_colors(a)
    assert a == [0, 1, 2], a

    # Single element
    a = [0]
    sort_colors(a)
    assert a == [0], a

    a = [1]
    sort_colors(a)
    assert a == [1], a

    a = [2]
    sort_colors(a)
    assert a == [2], a

    # Already sorted
    a = [0, 0, 1, 1, 2, 2]
    sort_colors(a)
    assert a == [0, 0, 1, 1, 2, 2], a

    # Reverse sorted
    a = [2, 2, 1, 1, 0, 0]
    sort_colors(a)
    assert a == [0, 0, 1, 1, 2, 2], a

    # All the same
    a = [1, 1, 1, 1]
    sort_colors(a)
    assert a == [1, 1, 1, 1], a

    # No 1s
    a = [2, 0, 2, 0]
    sort_colors(a)
    assert a == [0, 0, 2, 2], a

    # Cross-check the counting-sort variant against the two-pointer version
    import random

    for _ in range(1000):
        n = random.randint(1, 300)
        original = [random.randint(0, 2) for _ in range(n)]
        x, y = original[:], original[:]
        sort_colors(x)
        sort_colors_counting(y)
        assert x == y == sorted(original), (original, x, y)

    print("All tests passed for 75. Sort Colors")
