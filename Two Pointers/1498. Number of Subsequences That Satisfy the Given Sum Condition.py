"""
1498. Number of Subsequences That Satisfy the Given Sum Condition
Difficulty: Medium
Topics: Array, Two Pointers, Binary Search, Sorting

Problem:
You are given an array of integers nums and an integer target.

Return the number of non-empty subsequences of nums such that the sum of the
minimum and maximum element on it is less or equal to target. Since the answer
may be too large, return it modulo 10^9 + 7.

Example 1:
    Input: nums = [3,5,6,7], target = 9
    Output: 4
    Explanation: [3], [3,5], [3,5,6], [3,6] satisfy the condition.

Example 2:
    Input: nums = [3,3,6,8], target = 10
    Output: 6
    Explanation: [3], [3], [3,3], [3,6], [3,6], [3,3,6]

Example 3:
    Input: nums = [2,3,3,4,6,7], target = 12
    Output: 61
    Explanation: 63 non-empty subsequences in total; only [6,7] and [7] fail.

Constraints:
    1 <= nums.length <= 10^5
    1 <= nums[i] <= 10^6
    1 <= target <= 10^6

Approach (Sort + Two Pointers):
    A subsequence's validity only depends on its min and max, so order does not
    matter -> sort nums. Put l at the smallest candidate minimum and r at the
    largest element.
      - If nums[l] + nums[r] > target, nums[r] cannot be the max with nums[l]
        (or with any larger min), so r -= 1.
      - Otherwise nums[l] is the min and every element in (l, r] may be either
        included or excluded freely (they are all <= nums[r]), giving
        2^(r - l) valid subsequences whose minimum is nums[l]. Then l += 1.
    Each subsequence is counted exactly once, keyed by its minimum index.
    Powers of 2 are precomputed modulo 1e9+7.

Complexity:
    Time:  O(n log n) for sorting; the two-pointer sweep is O(n).
    Space: O(n) for the powers-of-two table (O(1) extra beyond sort otherwise).
"""
from bisect import bisect_right
from typing import List

MOD = 10**9 + 7


def num_subseq(nums: List[int], target: int) -> int:
    nums = sorted(nums)
    n = len(nums)
    pow2 = [1] * n
    for i in range(1, n):
        pow2[i] = pow2[i - 1] * 2 % MOD

    l, r, ans = 0, n - 1, 0
    while l <= r:
        if nums[l] + nums[r] > target:
            r -= 1
        else:
            ans = (ans + pow2[r - l]) % MOD
            l += 1
    return ans


def num_subseq_binary_search(nums: List[int], target: int) -> int:
    """Alternative: for each minimum index i, binary-search the furthest j with
    nums[i] + nums[j] <= target. O(n log n)."""
    nums = sorted(nums)
    ans = 0
    for i, x in enumerate(nums):
        if 2 * x > target:
            break
        j = bisect_right(nums, target - x) - 1
        ans = (ans + pow(2, j - i, MOD)) % MOD
    return ans


def _brute(nums: List[int], target: int) -> int:
    n, cnt = len(nums), 0
    for mask in range(1, 1 << n):
        sub = [nums[i] for i in range(n) if mask >> i & 1]
        if min(sub) + max(sub) <= target:
            cnt += 1
    return cnt % MOD


if __name__ == "__main__":
    import random

    for f in (num_subseq, num_subseq_binary_search):
        assert f([3, 5, 6, 7], 9) == 4
        assert f([3, 3, 6, 8], 10) == 6
        assert f([2, 3, 3, 4, 6, 7], 12) == 61
        assert f([5], 10) == 1          # single element, 5+5 <= 10
        assert f([6], 10) == 0          # single element too big
        assert f([1, 1, 1], 2) == 7     # all subsequences valid
        assert f([10, 20], 5) == 0      # nothing valid
        # large input -> modulo exercised
        assert f([1] * 100000, 2) == (pow(2, 100000, MOD) - 1) % MOD

    random.seed(0)
    for _ in range(300):
        arr = [random.randint(1, 15) for _ in range(random.randint(1, 10))]
        t = random.randint(1, 30)
        b = _brute(arr, t)
        assert num_subseq(arr, t) == b
        assert num_subseq_binary_search(arr, t) == b

    print("All tests passed for 1498. Number of Subsequences That Satisfy the Given Sum Condition")
