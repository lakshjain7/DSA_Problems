"""
18. 4Sum
Difficulty: Medium
Topics: Array, Two Pointers, Sorting

Problem Statement:
Given an array `nums` of n integers, return an array of all the unique
quadruplets [nums[a], nums[b], nums[c], nums[d]] such that:
    - 0 <= a, b, c, d < n
    - a, b, c, and d are distinct.
    - nums[a] + nums[b] + nums[c] + nums[d] == target
You may return the answer in any order.

Example 1:
    Input:  nums = [1, 0, -1, 0, -2, 2], target = 0
    Output: [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]

Example 2:
    Input:  nums = [2, 2, 2, 2, 2], target = 8
    Output: [[2, 2, 2, 2]]

Constraints:
    1 <= nums.length <= 200
    -10^9 <= nums[i] <= 10^9
    -10^9 <= target <= 10^9

------------------------------------------------------------------------
Approach: Sort + two nested loops + two-pointer
------------------------------------------------------------------------
This is a generalization of 3Sum. Sort the array first so that we can
both skip duplicates cheaply and use the two-pointer technique on the
inner-most search.

Fix the first two indices `i` and `j` with two nested loops. For each
fixed pair, the remaining problem is a 2Sum-on-a-sorted-array: use two
pointers `left` and `right` moving inward looking for
    nums[left] + nums[right] == target - nums[i] - nums[j].

Duplicate handling is the key to producing only *unique* quadruplets:
    - Skip a repeated value for `i` (when nums[i] == nums[i-1]).
    - Skip a repeated value for `j` (when nums[j] == nums[j-1]).
    - After recording a match, advance `left`/`right` past duplicates.

Why it works: sorting groups equal numbers together, so skipping equal
neighbors guarantees each distinct combination of values is considered
exactly once. The two-pointer sweep is complete for a sorted array
because increasing the sum requires moving `left` right and decreasing
it requires moving `right` left.

Complexity:
    Time:  O(n^3) - two nested loops (O(n^2)) each running an O(n)
           two-pointer scan.
    Space: O(1) extra (ignoring the output and the sort's stack), or
           O(n) if the sort is not in place.
"""

from typing import List


def four_sum(nums: List[int], target: int) -> List[List[int]]:
    """Return all unique quadruplets summing to target (two-pointer)."""
    nums.sort()
    n = len(nums)
    res: List[List[int]] = []

    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        # Pruning: smallest / largest achievable sums with i fixed.
        if nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
            break
        if nums[i] + nums[n - 1] + nums[n - 2] + nums[n - 3] < target:
            continue

        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            if nums[i] + nums[j] + nums[j + 1] + nums[j + 2] > target:
                break
            if nums[i] + nums[j] + nums[n - 1] + nums[n - 2] < target:
                continue

            left, right = j + 1, n - 1
            need = target - nums[i] - nums[j]
            while left < right:
                s = nums[left] + nums[right]
                if s == need:
                    res.append([nums[i], nums[j], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif s < need:
                    left += 1
                else:
                    right -= 1

    return res


# ------------------------------------------------------------------------
# Alternative approach: generalized k-Sum via recursion
# ------------------------------------------------------------------------
# k_sum reduces any k-Sum to the base case 2-Sum (two pointers). This is
# cleaner and extends to 5Sum, 6Sum, ... with the same code. Same
# O(n^{k-1}) time.
def four_sum_ksum(nums: List[int], target: int) -> List[List[int]]:
    nums.sort()

    def k_sum(start: int, k: int, tgt: int) -> List[List[int]]:
        n = len(nums)
        res: List[List[int]] = []
        if start >= n:
            return res
        # Feasibility pruning.
        if tgt < nums[start] * k or tgt > nums[-1] * k:
            return res
        if k == 2:
            lo, hi = start, n - 1
            while lo < hi:
                s = nums[lo] + nums[hi]
                if s == tgt:
                    res.append([nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
                    while lo < hi and nums[hi] == nums[hi + 1]:
                        hi -= 1
                elif s < tgt:
                    lo += 1
                else:
                    hi -= 1
            return res
        for i in range(start, n):
            if i > start and nums[i] == nums[i - 1]:
                continue
            for tail in k_sum(i + 1, k - 1, tgt - nums[i]):
                res.append([nums[i]] + tail)
        return res

    return k_sum(0, 4, target)


def _normalize(quads: List[List[int]]) -> set:
    """Order-independent comparison helper."""
    return {tuple(sorted(q)) for q in quads}


if __name__ == "__main__":
    # Example 1
    assert _normalize(four_sum([1, 0, -1, 0, -2, 2], 0)) == _normalize(
        [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
    )
    # Example 2 - all identical
    assert _normalize(four_sum([2, 2, 2, 2, 2], 8)) == _normalize([[2, 2, 2, 2]])
    # No solution
    assert four_sum([1, 2, 3, 4], 100) == []
    # Minimum length (cannot form a quadruplet)
    assert four_sum([1], 1) == []
    assert four_sum([0, 0, 0], 0) == []
    # Exactly one quadruplet
    assert _normalize(four_sum([0, 0, 0, 0], 0)) == _normalize([[0, 0, 0, 0]])
    # Negative target
    assert _normalize(four_sum([-3, -2, -1, 0, 0, 1, 2, 3], 0)) == _normalize([
        [-3, -2, 2, 3], [-3, -1, 1, 3], [-3, 0, 0, 3], [-3, 0, 1, 2],
        [-2, -1, 0, 3], [-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1],
    ])
    # Large values (no overflow concerns in Python)
    assert _normalize(four_sum([1000000000] * 4, 4000000000)) == _normalize(
        [[1000000000, 1000000000, 1000000000, 1000000000]]
    )

    # Cross-check the two implementations on random inputs.
    import random
    for _ in range(300):
        arr = [random.randint(-5, 5) for _ in range(random.randint(0, 8))]
        t = random.randint(-10, 10)
        assert _normalize(four_sum(list(arr), t)) == _normalize(
            four_sum_ksum(list(arr), t)
        )

    print("All tests passed for 18. 4Sum")
