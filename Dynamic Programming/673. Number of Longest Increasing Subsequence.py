"""
Problem 673: Number of Longest Increasing Subsequence
Difficulty: Medium
Topics: Array, Dynamic Programming, Binary Indexed Tree, Segment Tree

Given an integer array nums, return the number of longest strictly increasing
subsequences.

Examples:
    nums = [1,3,5,4,7] -> 2   (LIS length 4: [1,3,4,7] and [1,3,5,7])
    nums = [2,2,2,2,2] -> 5   (LIS length 1, five of them)

Constraints:
- 1 <= nums.length <= 2000
- -10^6 <= nums[i] <= 10^6

Approach:
    For each i keep length[i] = LIS length ending at i and count[i] = number of
    such subsequences. For every j < i with nums[j] < nums[i]:
      - if length[j]+1 > length[i]: length[i] = length[j]+1, count[i] = count[j]
      - elif equal: count[i] += count[j]
    Answer is the sum of count[i] over i with length[i] == max length.
    Correct because every LIS ending at i extends a best-length LIS ending at
    some smaller j.

Complexity:
    Time O(n^2), Space O(n).

Alternative: O(n log n) using, per length, a list of (value, cumulative count)
    with binary search (patience-sorting style).
"""
from bisect import bisect_left, bisect_right
from typing import List


def findNumberOfLIS(nums: List[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0
    length = [1] * n
    count = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
    best = max(length)
    return sum(c for l, c in zip(length, count) if l == best)


def findNumberOfLIS_nlogn(nums: List[int]) -> int:
    # tails[k]: ends of LIS of length k+1 (decreasing order kept per level)
    # levels[k]: list of (end value, cumulative count), values decreasing
    levels: List[List[tuple]] = []
    for x in nums:
        # find first level whose last value >= x (x extends level lo-1)
        lo, hi = 0, len(levels)
        while lo < hi:
            mid = (lo + hi) // 2
            if levels[mid][-1][0] >= x:
                hi = mid
            else:
                lo = mid + 1
        cnt = 1
        if lo > 0:
            prev = levels[lo - 1]
            # entries have decreasing values; cumulative counts increase.
            # need sum of counts for values < x -> suffix of the list
            neg = [-v for v, _ in prev]          # increasing
            idx = bisect_right(neg, -x)          # first entry with value < x
            total = prev[-1][1]
            before = prev[idx - 1][1] if idx > 0 else 0
            cnt = total - before
        if lo == len(levels):
            levels.append([(x, cnt)])
        else:
            levels[lo].append((x, levels[lo][-1][1] + cnt))
    return levels[-1][-1][1] if levels else 0


if __name__ == "__main__":
    cases = [
        ([1, 3, 5, 4, 7], 2),
        ([2, 2, 2, 2, 2], 5),
        ([1], 1),
        ([1, 2, 3, 4, 5], 1),
        ([5, 4, 3, 2, 1], 5),
        ([1, 2, 4, 3, 5, 4, 7, 2], 3),
        ([-1, 0, -1, 1], 1),
    ]
    for nums, exp in cases:
        assert findNumberOfLIS(nums) == exp, (nums, findNumberOfLIS(nums), exp)
        assert findNumberOfLIS_nlogn(nums) == exp, (nums, findNumberOfLIS_nlogn(nums), exp)
    import random
    for _ in range(300):
        a = [random.randint(-5, 5) for _ in range(random.randint(1, 12))]
        assert findNumberOfLIS(a) == findNumberOfLIS_nlogn(a), a
    print("All tests passed.")
