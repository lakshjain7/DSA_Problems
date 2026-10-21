"""
523. Continuous Subarray Sum
Difficulty: Medium
Topics: Array, Hash Table, Math, Prefix Sum

Problem:
Given an integer array nums and an integer k, return true if nums has a good
subarray, or false otherwise. A good subarray is a subarray where:
  - its length is at least two, and
  - the sum of the elements of the subarray is a multiple of k.
Note that a multiple of k is an integer x * k where x is an integer; 0 is
always a multiple of k.

Examples:
  Input: nums = [23,2,4,6,7], k = 6  -> True   ([2,4] sums to 6)
  Input: nums = [23,2,6,4,7], k = 6  -> True   ([23,2,6,4,7] sums to 42)
  Input: nums = [23,2,6,4,7], k = 13 -> False

Constraints:
  1 <= nums.length <= 10^5
  0 <= nums[i] <= 10^9
  0 <= sum(nums[i]) <= 2^31 - 1
  1 <= k <= 2^31 - 1

Approach (prefix sum remainders + hash map):
  Let P[i] be the sum of the first i elements. A subarray (j, i] has a sum that
  is a multiple of k iff P[i] % k == P[j] % k. Store the earliest index at
  which each remainder appears (seeding remainder 0 at index -1, i.e. the
  empty prefix). When the current remainder was seen at index j and
  i - j >= 2, the subarray has length >= 2 and we are done. We never overwrite
  an earlier index, which keeps the gap as large as possible.

Complexity:
  Time:  O(n)
  Space: O(min(n, k))
"""
from typing import List


def check_subarray_sum(nums: List[int], k: int) -> bool:
    first_seen = {0: -1}
    rem = 0
    for i, x in enumerate(nums):
        rem = (rem + x) % k
        if rem in first_seen:
            if i - first_seen[rem] >= 2:
                return True
        else:
            first_seen[rem] = i
    return False


def check_subarray_sum_brute(nums: List[int], k: int) -> bool:
    """Alternative: O(n^2) brute force using running sums (for cross-checking)."""
    n = len(nums)
    for i in range(n):
        s = nums[i]
        for j in range(i + 1, n):
            s += nums[j]
            if s % k == 0:
                return True
    return False


if __name__ == "__main__":
    import random

    assert check_subarray_sum([23, 2, 4, 6, 7], 6) is True
    assert check_subarray_sum([23, 2, 6, 4, 7], 6) is True
    assert check_subarray_sum([23, 2, 6, 4, 7], 13) is False
    assert check_subarray_sum([5], 5) is False            # length 1 not allowed
    assert check_subarray_sum([0, 0], 1) is True          # zeros
    assert check_subarray_sum([0], 1) is False
    assert check_subarray_sum([1, 0], 2) is False
    assert check_subarray_sum([1, 2, 3], 5) is True
    assert check_subarray_sum([1, 2, 12], 6) is False
    random.seed(1)
    for _ in range(2000):
        n = random.randint(1, 8)
        arr = [random.randint(0, 10) for _ in range(n)]
        kk = random.randint(1, 9)
        assert check_subarray_sum(arr, kk) == check_subarray_sum_brute(arr, kk), (arr, kk)
    print("All tests passed.")
