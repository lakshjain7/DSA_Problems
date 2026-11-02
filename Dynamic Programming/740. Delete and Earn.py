"""
740. Delete and Earn
Difficulty: Medium
Topics: Array, Hash Table, Dynamic Programming

Problem:
You are given an integer array nums. You want to maximize the number of points
you get by performing the following operation any number of times:
  Pick any nums[i] and delete it to earn nums[i] points. Afterwards, you must
  delete every element equal to nums[i] - 1 and every element equal to nums[i] + 1.
Return the maximum number of points you can earn by applying the above operation
some number of times.

Example 1:
  Input: nums = [3,4,2]   Output: 6
  Explanation: Delete 4 (earn 4), which removes 3. Then delete 2 (earn 2).
Example 2:
  Input: nums = [2,2,3,3,3,4]   Output: 9
  Explanation: Delete 3s (earn 9), which removes the 2s and 4.

Constraints:
  1 <= nums.length <= 2 * 10^4
  1 <= nums[i] <= 10^4

Approach:
Taking a value v means taking ALL copies of v (they are free once one is taken,
and leaving them never helps), earning v * count[v]. Taking v forbids v-1 and
v+1, which is exactly the House Robber constraint over the sorted distinct
values: adjacent values (differing by 1) cannot both be taken; values that
differ by >= 2 are independent. So aggregate points per value and run
House Robber, resetting the "adjacency" when there is a gap in values.

Complexity:
  Time:  O(n + k log k) where k = distinct values (O(n + M) with bucket array)
  Space: O(k)
"""
from collections import Counter
from typing import List


def deleteAndEarn(nums: List[int]) -> int:
    cnt = Counter(nums)
    keys = sorted(cnt)
    take, skip = 0, 0  # best total ending with previous value taken / skipped
    prev = None
    for v in keys:
        gain = v * cnt[v]
        if prev is not None and v == prev + 1:
            take, skip = skip + gain, max(take, skip)
        else:
            take, skip = max(take, skip) + gain, max(take, skip)
        prev = v
    return max(take, skip)


# Alternative: bucket array + classic House Robber on points[0..max]
def deleteAndEarnBuckets(nums: List[int]) -> int:
    points = [0] * (max(nums) + 1)
    for x in nums:
        points[x] += x
    a = b = 0  # a = dp[i-2], b = dp[i-1]
    for p in points:
        a, b = b, max(b, a + p)
    return b


if __name__ == "__main__":
    import random
    for f in (deleteAndEarn, deleteAndEarnBuckets):
        assert f([3, 4, 2]) == 6
        assert f([2, 2, 3, 3, 3, 4]) == 9
        assert f([1]) == 1
        assert f([1, 1, 1, 1]) == 4
        assert f([1, 3, 5]) == 9          # gaps: take all
        assert f([1, 2]) == 2
        assert f([10000, 10000, 9999]) == 20000
    # brute-force cross-check
    def brute(nums):
        best = 0
        vals = sorted(set(nums))
        n = len(vals)
        for mask in range(1 << n):
            chosen = [vals[i] for i in range(n) if mask >> i & 1]
            if any(b - a == 1 for a, b in zip(chosen, chosen[1:])):
                continue
            best = max(best, sum(v * nums.count(v) for v in chosen))
        return best
    for _ in range(300):
        arr = [random.randint(1, 8) for _ in range(random.randint(1, 10))]
        exp = brute(arr)
        assert deleteAndEarn(arr) == exp and deleteAndEarnBuckets(arr) == exp, arr
    print("All tests passed.")
