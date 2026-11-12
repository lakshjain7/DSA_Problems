"""
983. Minimum Cost For Tickets
Difficulty: Medium
Topics: Array, Dynamic Programming

Problem:
You have planned some train traveling one year in advance. The days of the year
in which you will travel are given as an integer array `days`. Each day is an
integer from 1 to 365.

Train tickets are sold in three different ways:
  - a 1-day pass is sold for costs[0] dollars,
  - a 7-day pass is sold for costs[1] dollars, and
  - a 30-day pass is sold for costs[2] dollars.

The passes allow that many days of consecutive travel. For example, if we get a
7-day pass on day 2, then we can travel for 7 days: 2, 3, 4, 5, 6, 7, and 8.

Return the minimum number of dollars you need to travel every day in the given
list of days.

Example 1:
    Input: days = [1,4,6,7,8,20], costs = [2,7,15]
    Output: 11
    Explanation: 1-day pass on day 1 ($2), 7-day pass on day 3 covering
    days 3..9 ($7), 1-day pass on day 20 ($2). Total $11.

Example 2:
    Input: days = [1,2,3,4,5,6,7,8,9,10,30,31], costs = [2,7,15]
    Output: 17
    Explanation: 30-day pass on day 1 ($15), 1-day pass on day 31 ($2).

Constraints:
    1 <= days.length <= 365
    1 <= days[i] <= 365
    days is in strictly increasing order.
    costs.length == 3
    1 <= costs[i] <= 1000

Approach (DP over travel-day indices + two pointers):
    Let dp[i] = minimum cost to cover days[i:] (all travel days from index i on).
    At travel day days[i] we must buy some pass that starts today (buying earlier
    is never better than buying on the first uncovered travel day). For each pass
    of length L in (1, 7, 30) with cost c, it covers days[i] .. days[i] + L - 1;
    let j be the first index with days[j] >= days[i] + L. Then
        dp[i] = min over passes of  c + dp[j].
    dp[n] = 0. We iterate i from n-1 down to 0. Because days is sorted, j for
    each pass can be found with a pointer that only moves left as i decreases,
    giving O(n) overall (or bisect for O(n log n), still trivial).

    Why it works: the optimal schedule's first purchase covering days[i] can be
    shifted to start exactly on days[i] without uncovering any travel day, so
    trying the three options at each uncovered travel day is exhaustive.

Complexity:
    Time:  O(n) with monotone pointers (n = len(days) <= 365).
    Space: O(n) for the dp array.

Alternative (DP over calendar days 1..365):
    dp[d] = min cost to cover all travel days <= d.
    If d is not a travel day, dp[d] = dp[d-1]; otherwise
    dp[d] = min(dp[d-1] + c0, dp[max(0,d-7)] + c1, dp[max(0,d-30)] + c2).
    Time O(365), Space O(365) — independent of n, simple to write.
"""
from typing import List


class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        n = len(days)
        durations = (1, 7, 30)
        dp = [0] * (n + 1)
        # ptr[k] = first index NOT covered by a pass of durations[k] bought at days[i].
        # As i decreases, days[i] decreases, so each pointer only moves left.
        ptr = [n, n, n]
        for i in range(n - 1, -1, -1):
            best = float("inf")
            for k, length in enumerate(durations):
                while ptr[k] - 1 > i and days[ptr[k] - 1] >= days[i] + length:
                    ptr[k] -= 1
                best = min(best, costs[k] + dp[ptr[k]])
            dp[i] = best
        return dp[0]

    def mincostTicketsCalendar(self, days: List[int], costs: List[int]) -> int:
        travel = set(days)
        last = days[-1]
        dp = [0] * (last + 1)
        for d in range(1, last + 1):
            if d not in travel:
                dp[d] = dp[d - 1]
                continue
            dp[d] = min(
                dp[d - 1] + costs[0],
                dp[max(0, d - 7)] + costs[1],
                dp[max(0, d - 30)] + costs[2],
            )
        return dp[last]


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([1, 4, 6, 7, 8, 20], [2, 7, 15], 11),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15], 17),
        ([1], [2, 7, 15], 2),                 # single day
        ([1], [10, 1, 5], 1),                 # longer pass cheaper than 1-day
        ([1, 365], [2, 7, 15], 4),            # far apart days
        (list(range(1, 31)), [2, 7, 15], 15), # full month -> 30-day pass
        ([1, 2, 3, 4, 5, 6, 7], [3, 7, 100], 7),
    ]
    for days, costs, expected in cases:
        assert s.mincostTickets(days, costs) == expected, (days, costs)
        assert s.mincostTicketsCalendar(days, costs) == expected, (days, costs)

    # randomized cross-check between the two approaches
    rng = random.Random(983)
    for _ in range(300):
        k = rng.randint(1, 60)
        days = sorted(rng.sample(range(1, 366), k))
        costs = [rng.randint(1, 50) for _ in range(3)]
        assert s.mincostTickets(days, costs) == s.mincostTicketsCalendar(days, costs)

    print("All tests passed for 983. Minimum Cost For Tickets")
