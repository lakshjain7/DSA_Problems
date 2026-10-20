"""
1482. Minimum Number of Days to Make m Bouquets
Difficulty: Medium
Topics: Array, Binary Search

Problem:
You are given an integer array bloomDay, an integer m and an integer k.
You want to make m bouquets. To make a bouquet, you need to use k adjacent
flowers from the garden. The garden consists of n flowers, the i-th flower
will bloom on bloomDay[i] and then can be used in exactly one bouquet.
Return the minimum number of days you need to wait to be able to make m
bouquets from the garden. If it is impossible, return -1.

Examples:
    bloomDay = [1,10,3,10,2], m = 3, k = 1  -> 3
    bloomDay = [1,10,3,10,2], m = 3, k = 2  -> -1
    bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3 -> 12

Constraints:
    bloomDay.length == n, 1 <= n <= 10^5
    1 <= bloomDay[i] <= 10^9
    1 <= m <= 10^6, 1 <= k <= n

Approach (binary search on the answer):
    If we can make m bouquets after day d, we can also do so after day d+1
    (monotonic). So binary search d in [min(bloomDay), max(bloomDay)].
    feasible(d): scan the garden, count consecutive flowers with
    bloomDay <= d; every k of them form a bouquet and the run resets.
    If m*k > n it is impossible -> -1.

Complexity:
    Time: O(n log(max - min))   Space: O(1)
"""
from typing import List


class Solution:
    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        if m * k > len(bloomDay):
            return -1

        def feasible(day: int) -> bool:
            bouquets = run = 0
            for b in bloomDay:
                if b <= day:
                    run += 1
                    if run == k:
                        bouquets += 1
                        run = 0
                        if bouquets >= m:
                            return True
                else:
                    run = 0
            return bouquets >= m

        lo, hi = min(bloomDay), max(bloomDay)
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo

    # Alternative: sort the distinct bloom days and binary search over them
    # (same complexity, but searches only over days that matter).
    def minDaysSorted(self, bloomDay: List[int], m: int, k: int) -> int:
        if m * k > len(bloomDay):
            return -1
        days = sorted(set(bloomDay))

        def ok(d: int) -> bool:
            cnt = run = 0
            for b in bloomDay:
                run = run + 1 if b <= d else 0
                if run == k:
                    cnt += 1
                    run = 0
            return cnt >= m

        lo, hi = 0, len(days) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(days[mid]):
                hi = mid
            else:
                lo = mid + 1
        return days[lo]


if __name__ == "__main__":
    s = Solution()
    for f in (s.minDays, s.minDaysSorted):
        assert f([1, 10, 3, 10, 2], 3, 1) == 3
        assert f([1, 10, 3, 10, 2], 3, 2) == -1
        assert f([7, 7, 7, 7, 12, 7, 7], 2, 3) == 12
        assert f([5], 1, 1) == 5
        assert f([1, 1, 1, 1], 2, 2) == 1
        assert f([1000000000, 1000000000], 1, 1) == 1000000000
        assert f([1, 2, 3, 4], 1, 4) == 4
    print("All tests passed")
