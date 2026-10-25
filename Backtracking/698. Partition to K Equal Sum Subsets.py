"""
698. Partition to K Equal Sum Subsets
Difficulty: Medium
Topics: Array, Dynamic Programming, Backtracking, Bit Manipulation, Bitmask

Given an integer array nums and an integer k, return true if it is possible to
divide this array into k non-empty subsets whose sums are all equal.

Example 1:
    Input: nums = [4,3,2,3,5,2,1], k = 4
    Output: true  ([5], [1,4], [2,3], [2,3])
Example 2:
    Input: nums = [1,2,3,4], k = 3
    Output: false

Constraints:
    1 <= k <= nums.length <= 16
    1 <= nums[i] <= 10^4
    The frequency of each element is in the range [1, 4].

Approach (bitmask DP):
    Target = sum / k (must divide evenly, and max(nums) <= target). Let
    mask be the set of used numbers; dp[mask] = sum of used numbers modulo
    target, or -1 if the mask is unreachable. Adding number i to a reachable
    mask is allowed if (dp[mask] + nums[i]) <= target. Answer is dp[full] == 0
    (i.e. reachable). Sorting is not needed for correctness.

Complexity: Time O(2^n * n), Space O(2^n).
"""
from typing import List


def can_partition_k_subsets(nums: List[int], k: int) -> bool:
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    if max(nums) > target:
        return False
    n = len(nums)
    full = (1 << n) - 1
    dp = [-1] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] < 0:
            continue
        for i in range(n):
            if mask & (1 << i):
                continue
            if dp[mask] + nums[i] <= target:
                nm = mask | (1 << i)
                if dp[nm] < 0:
                    dp[nm] = (dp[mask] + nums[i]) % target
    return dp[full] == 0


def can_partition_backtrack(nums: List[int], k: int) -> bool:
    """Alternative: backtracking filling k buckets, largest numbers first."""
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    nums = sorted(nums, reverse=True)
    if nums[0] > target:
        return False
    buckets = [0] * k

    def dfs(i: int) -> bool:
        if i == len(nums):
            return True
        seen = set()
        for b in range(k):
            if buckets[b] + nums[i] > target or buckets[b] in seen:
                continue
            seen.add(buckets[b])
            buckets[b] += nums[i]
            if dfs(i + 1):
                return True
            buckets[b] -= nums[i]
        return False

    return dfs(0)


if __name__ == "__main__":
    cases = [([4, 3, 2, 3, 5, 2, 1], 4, True), ([1, 2, 3, 4], 3, False),
             ([1], 1, True), ([2, 2, 2, 2, 3, 4, 5], 4, False),
             ([1, 1, 1, 1], 4, True), ([10, 10, 10, 7, 7, 7, 7, 7, 7, 6, 6, 6], 3, True),
             ([5, 5], 2, True), ([1, 2], 2, False)]
    for arr, k, exp in cases:
        assert can_partition_k_subsets(arr, k) == exp, (arr, k)
        assert can_partition_backtrack(arr, k) == exp, (arr, k)
    print("All tests passed.")
