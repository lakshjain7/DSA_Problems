"""
1658. Minimum Operations to Reduce X to Zero
Difficulty: Medium
Topics: Array, Hash Table, Binary Search, Sliding Window, Prefix Sum

Problem:
You are given an integer array nums and an integer x. In one operation, you can
either remove the leftmost or the rightmost element from the array nums and
subtract its value from x. Note that this modifies the array for future
operations.

Return the minimum number of operations to reduce x to exactly 0 if it is
possible, otherwise, return -1.

Example 1:
  Input: nums = [1,1,4,2,3], x = 5
  Output: 2
  Explanation: The optimal solution is to remove the last two elements.

Example 2:
  Input: nums = [5,6,7,8,9], x = 4
  Output: -1

Example 3:
  Input: nums = [3,2,20,1,1,3], x = 10
  Output: 5
  Explanation: Remove the last three elements and the first two (5 operations).

Constraints:
  - 1 <= nums.length <= 10^5
  - 1 <= nums[i] <= 10^4
  - 1 <= x <= 10^9

Approach (invert the problem -> longest subarray with a fixed sum):
  Removing a prefix and a suffix whose sum is x is the same as KEEPING a
  contiguous middle subarray whose sum is target = sum(nums) - x. Minimizing
  removals == maximizing the length of that middle window.
  Because all nums[i] are positive, the window sum is monotonic in its size,
  so a classic variable-size sliding window works: extend right, shrink left
  while the sum exceeds target, and record the length when sum == target.
  Edge cases: target < 0 -> impossible; target == 0 -> remove everything.

Complexity:
  Time:  O(n) — each index enters and leaves the window at most once.
  Space: O(1).

Alternative approach (prefix sums + hash map):
  Map each prefix sum to its index. For each suffix (scanning from the right),
  look up whether prefix sum (x - suffix_sum) exists; total ops = prefix_len +
  suffix_len. Also O(n) time but O(n) space; it would still work if values
  could be zero (not negative), while the sliding window relies on positivity.
"""
from typing import List


def min_operations(nums: List[int], x: int) -> int:
    target = sum(nums) - x
    if target < 0:
        return -1
    if target == 0:
        return len(nums)

    best = -1
    window = 0
    left = 0
    for right, val in enumerate(nums):
        window += val
        while window > target:
            window -= nums[left]
            left += 1
        if window == target:
            best = max(best, right - left + 1)
    return -1 if best == -1 else len(nums) - best


def min_operations_prefix_map(nums: List[int], x: int) -> int:
    """Alternative: prefix-sum hash map, combining a prefix with each suffix."""
    n = len(nums)
    first_idx = {0: 0}  # prefix sum -> number of elements taken from the left
    s = 0
    for i, v in enumerate(nums):
        s += v
        if s > x:
            break
        first_idx.setdefault(s, i + 1)

    best = first_idx.get(x, float("inf"))
    suffix = 0
    for j in range(n - 1, -1, -1):
        suffix += nums[j]
        if suffix > x:
            break
        k = n - j  # suffix length
        need = x - suffix
        if need in first_idx and first_idx[need] + k <= n:
            best = min(best, first_idx[need] + k)
    return -1 if best == float("inf") else int(best)


if __name__ == "__main__":
    for f in (min_operations, min_operations_prefix_map):
        assert f([1, 1, 4, 2, 3], 5) == 2
        assert f([5, 6, 7, 8, 9], 4) == -1
        assert f([3, 2, 20, 1, 1, 3], 10) == 5
        # Remove everything
        assert f([1, 1], 2) == 2
        # x larger than total
        assert f([1, 1], 3) == -1
        # Single element
        assert f([7], 7) == 1
        assert f([7], 3) == -1
        # Only from the left
        assert f([2, 3, 100, 100], 5) == 2
        # Mixed, prefer fewer ops
        assert f([1, 1, 1, 1, 5], 5) == 1
        assert f([8828, 9581, 49, 9818, 9974, 9869, 9991, 10000, 10000,
                  10000, 9999, 9993, 9904, 8819, 1231, 6309], 134365) == 16

    # Brute-force cross-check
    import random
    random.seed(1)

    def brute(nums, x):
        n = len(nums); best = -1
        for l in range(n + 1):
            for r in range(n + 1 - l):
                if sum(nums[:l]) + sum(nums[n - r:]) == x:
                    if best == -1 or l + r < best:
                        best = l + r
        return best

    for _ in range(400):
        arr = [random.randint(1, 6) for _ in range(random.randint(1, 8))]
        x = random.randint(1, 30)
        exp = brute(arr, x)
        assert min_operations(arr, x) == exp, (arr, x)
        assert min_operations_prefix_map(arr, x) == exp, (arr, x)
    print("All tests passed for 1658. Minimum Operations to Reduce X to Zero")
