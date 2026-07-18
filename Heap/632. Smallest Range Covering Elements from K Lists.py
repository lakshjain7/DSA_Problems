"""
632. Smallest Range Covering Elements from K Lists
Difficulty: Hard
Topics: Array, Hash Table, Greedy, Sorting, Heap (Priority Queue), Sliding Window

------------------------------------------------------------------------
PROBLEM STATEMENT
------------------------------------------------------------------------
You have k lists of sorted integers in non-decreasing order. Find the
smallest range that includes at least one number from each of the k lists.

We define the range [a, b] is smaller than range [c, d] if b - a < d - c
or (b - a == d - c and a < c).

------------------------------------------------------------------------
EXAMPLES
------------------------------------------------------------------------
Example 1:
Input:  nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]
Output: [20,24]
Explanation:
    List 1: [4, 10, 15, 24, 26], 24 is in range [20, 24].
    List 2: [0, 9, 12, 20],      20 is in range [20, 24].
    List 3: [5, 18, 22, 30],     22 is in range [20, 24].

Example 2:
Input:  nums = [[1,2,3],[1,2,3],[1,2,3]]
Output: [1,1]

------------------------------------------------------------------------
CONSTRAINTS
------------------------------------------------------------------------
- nums.length == k
- 1 <= k <= 3500
- 1 <= nums[i].length <= 50
- -10^5 <= nums[i][j] <= 10^5
- nums[i] is sorted in non-decreasing order.

------------------------------------------------------------------------
APPROACH (Min-heap over one pointer per list)
------------------------------------------------------------------------
Any valid range must contain at least one element from every list. Think
of choosing one "current" element from each list; the tightest range that
covers those k picks is [min(picks), max(picks)]. We want to minimize
max - min over all ways of picking.

Greedy insight: maintain a candidate window that always holds exactly one
element from each list -- the current frontier. The window's width is
(current max) - (current min). To try to shrink it, we must advance the
list that currently contributes the minimum (any other move can only keep
or grow the min while the max stays >= current max). Advancing the min is
the only move that can reduce the width.

Implementation with a min-heap:
    - Push the first element of every list: (value, list_index, elem_index).
    - Track `cur_max` = the maximum value currently in the heap.
    - Repeatedly:
        * Pop the smallest (value == cur_min). The window
          [cur_min, cur_max] covers one element from each list, so update
          the best range if it is smaller.
        * If the popped element was the last of its list, stop -- we can
          no longer cover that list, so no further window is possible.
        * Otherwise push the next element from that same list and update
          cur_max.

Why it works: the heap always contains exactly one element per list, so
[cur_min, cur_max] is always a valid covering window. By always advancing
the minimum we enumerate every window that could possibly be optimal, and
we stop the moment any list is exhausted (its minimum can never be
covered again with a smaller value).

------------------------------------------------------------------------
COMPLEXITY
------------------------------------------------------------------------
Let n = total number of elements across all k lists.
Time:  O(n log k) -- each element is pushed/popped once, heap size <= k.
Space: O(k) for the heap.
"""

from typing import List
import heapq


def smallestRange(nums: List[List[int]]) -> List[int]:
    # Initialize heap with the first element of each list.
    heap = []
    cur_max = float("-inf")
    for i, lst in enumerate(nums):
        heap.append((lst[0], i, 0))
        cur_max = max(cur_max, lst[0])
    heapq.heapify(heap)

    best_lo, best_hi = float("-inf"), float("inf")

    while heap:
        cur_min, list_idx, elem_idx = heapq.heappop(heap)

        # Update the best range. Prefer a strictly smaller width; ties are
        # already resolved because we advance the minimum, encountering the
        # smaller starting point first for equal widths.
        if cur_max - cur_min < best_hi - best_lo:
            best_lo, best_hi = cur_min, cur_max

        # If the list contributing the minimum is exhausted, we cannot
        # cover it anymore -> no future window is valid.
        if elem_idx + 1 == len(nums[list_idx]):
            break

        next_val = nums[list_idx][elem_idx + 1]
        cur_max = max(cur_max, next_val)
        heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return [best_lo, best_hi]


# ----------------------------------------------------------------------
# ALTERNATIVE APPROACH: merge + sliding window over a "need all k" count
# ----------------------------------------------------------------------
# Flatten every value into (value, list_id), sort, then slide a window
# that must contain at least one element from each list. Shrink from the
# left whenever all k lists are represented, recording the tightest window.
# Same O(n log n) time, O(n) space, but conceptually a frequency-window
# problem instead of a heap frontier.
def smallestRange_slidingWindow(nums: List[List[int]]) -> List[int]:
    merged = []
    for i, lst in enumerate(nums):
        for v in lst:
            merged.append((v, i))
    merged.sort()

    k = len(nums)
    count = {}
    have = 0
    left = 0
    best_lo, best_hi = float("-inf"), float("inf")

    for right in range(len(merged)):
        val_r, id_r = merged[right]
        count[id_r] = count.get(id_r, 0) + 1
        if count[id_r] == 1:
            have += 1

        while have == k:
            val_l, id_l = merged[left]
            if val_r - val_l < best_hi - best_lo:
                best_lo, best_hi = val_l, val_r
            count[id_l] -= 1
            if count[id_l] == 0:
                have -= 1
            left += 1

    return [best_lo, best_hi]


if __name__ == "__main__":
    # Example 1
    assert smallestRange([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]) == [20, 24]
    assert smallestRange_slidingWindow([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]) == [20, 24]

    # Example 2: all identical lists -> zero-width range
    assert smallestRange([[1, 2, 3], [1, 2, 3], [1, 2, 3]]) == [1, 1]
    assert smallestRange_slidingWindow([[1, 2, 3], [1, 2, 3], [1, 2, 3]]) == [1, 1]

    # Single list -> range is [first, first] (smallest width, smallest start)
    assert smallestRange([[1, 2, 3]]) == [1, 1]
    assert smallestRange_slidingWindow([[1, 2, 3]]) == [1, 1]

    # Two lists, one element each
    assert smallestRange([[1], [5]]) == [1, 5]
    assert smallestRange_slidingWindow([[1], [5]]) == [1, 5]

    # Negative numbers: [-5,-3] (width 2, smallest start) covers -5,-4,-3.
    assert smallestRange([[-5, -1], [-4, -2], [-3, 0]]) == [-5, -3]
    assert smallestRange_slidingWindow([[-5, -1], [-4, -2], [-3, 0]]) == [-5, -3]

    # Lists of differing lengths; verify both methods agree
    data = [[1, 5, 8], [4, 12], [7, 8, 10]]
    assert smallestRange(data) == smallestRange_slidingWindow(data)

    # Width-tie resolution: prefer the smaller starting value.
    # [[0,10],[5,15]] -> windows [0,5] (width 5) and [10,15] (width 5);
    # answer must be [0,5].
    assert smallestRange([[0, 10], [5, 15]]) == [0, 5]
    assert smallestRange_slidingWindow([[0, 10], [5, 15]]) == [0, 5]

    print("632. Smallest Range Covering Elements from K Lists: all tests passed!")
