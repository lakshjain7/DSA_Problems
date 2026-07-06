"""
16. 3Sum Closest
Difficulty: Medium
Topics: Array, Two Pointers, Sorting

Problem Statement:
Given an integer array `nums` of length n and an integer `target`, find three
integers in `nums` such that the sum is closest to `target`.

Return the sum of the three integers.

You may assume that each input would have exactly one solution.

Examples:
    Input: nums = [-1,2,1,-4], target = 1
    Output: 2
    Explanation: The sum that is closest to the target is 2 (-1 + 2 + 1 = 2).

    Input: nums = [0,0,0], target = 1
    Output: 0
    Explanation: The sum that is closest to the target is 0 (0 + 0 + 0 = 0).

Constraints:
    3 <= nums.length <= 500
    -1000 <= nums[i] <= 1000
    -10^4 <= target <= 10^4

Approach (Sort + Two Pointers):
Sort the array first. Then fix the first number `nums[i]` and use two pointers
(`lo` starting right after `i`, `hi` at the end) to search for the pair whose
sum with `nums[i]` is closest to `target`.

For each fixed `i`:
    - Compute current_sum = nums[i] + nums[lo] + nums[hi].
    - Track the closest sum seen so far (smallest absolute difference from
      target). Ties don't matter since the problem guarantees a unique
      solution/closest value in practice, but we keep the first-found closest
      on exact ties for determinism.
    - If current_sum == target, we can return immediately since nothing can
      be closer.
    - If current_sum < target, moving `lo` right increases the sum, which
      might bring us closer -> lo += 1.
    - If current_sum > target, moving `hi` left decreases the sum -> hi -= 1.

Sorting lets us use the two-pointer technique to explore all pairs for a
fixed `i` in O(n) instead of O(n^2), and monotonic pointer movement is valid
because the array is sorted: increasing `lo` strictly increases the sum,
decreasing `hi` strictly decreases the sum, so we never miss the optimal pair
for that fixed `i`.

Complexity:
    Time:  O(n^2)   - O(n log n) sort + O(n) for outer loop * O(n) two pointers
    Space: O(1)     - excluding the space used for sorting (O(log n) to O(n)
                       depending on the sort algorithm's implementation)

Alternative Approach:
Brute force check every triplet: O(n^3) time, O(1) space. Correct but far too
slow for n up to 500 (worst case ~1.25*10^8 combinations, borderline but the
two-pointer approach is strictly better and idiomatic for this problem
family, mirroring 3Sum).
"""

from typing import List


def three_sum_closest(nums: List[int], target: int) -> int:
    nums.sort()
    n = len(nums)
    closest = nums[0] + nums[1] + nums[2]

    for i in range(n - 2):
        # Skip duplicate anchors to save a little work (not required for
        # correctness here, but harmless and a common optimization).
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        lo, hi = i + 1, n - 1
        while lo < hi:
            current_sum = nums[i] + nums[lo] + nums[hi]

            if abs(current_sum - target) < abs(closest - target):
                closest = current_sum

            if current_sum == target:
                return current_sum
            elif current_sum < target:
                lo += 1
            else:
                hi -= 1

    return closest


def three_sum_closest_brute_force(nums: List[int], target: int) -> int:
    """Alternative O(n^3) brute-force approach, useful for cross-checking."""
    n = len(nums)
    closest = nums[0] + nums[1] + nums[2]
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                current_sum = nums[i] + nums[j] + nums[k]
                if abs(current_sum - target) < abs(closest - target):
                    closest = current_sum
    return closest


if __name__ == "__main__":
    # Example 1
    assert three_sum_closest([-1, 2, 1, -4], 1) == 2

    # Example 2
    assert three_sum_closest([0, 0, 0], 1) == 0

    # Exact match possible
    assert three_sum_closest([1, 1, 1, 1], 3) == 3

    # Negative numbers and target
    neg_result = three_sum_closest([-3, -2, -5, -6, -1], -10)
    assert neg_result == three_sum_closest_brute_force([-3, -2, -5, -6, -1], -10)

    # Larger array, sanity check against brute force
    import random
    random.seed(42)
    for _ in range(50):
        size = random.randint(3, 8)
        arr = [random.randint(-10, 10) for _ in range(size)]
        tgt = random.randint(-15, 15)
        fast = three_sum_closest(arr[:], tgt)
        slow = three_sum_closest_brute_force(arr[:], tgt)
        assert abs(fast - tgt) == abs(slow - tgt), (arr, tgt, fast, slow)

    # Minimum size input (exactly 3 elements)
    assert three_sum_closest([1, 2, 3], 10) == 6

    print("All test cases passed!")
