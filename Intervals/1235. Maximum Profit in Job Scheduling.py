"""
1235. Maximum Profit in Job Scheduling
Difficulty: Hard
Topics: Array, Binary Search, Dynamic Programming, Sorting

Problem Statement:
------------------
We have `n` jobs, where every job is scheduled to be done from
`startTime[i]` to `endTime[i]`, obtaining a profit of `profit[i]`.

You're given the `startTime`, `endTime` and `profit` arrays, return the
maximum profit you can take such that there are no two jobs in the
subset with overlapping time range. If you choose a job that ends at
time `X`, you can choose another job that starts at time `X`.

Examples:
---------
Example 1:
    Input: startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
    Output: 120
    Explanation: The subset chosen is the first and fourth job.
    Time range [1-3]+[3-6], we get a profit of 120 = 50 + 70.

Example 2:
    Input: startTime = [1,2,3,4,6], endTime = [3,5,10,6,9],
           profit = [20,20,100,70,60]
    Output: 150
    Explanation: The subset chosen is the first, fourth and fifth job.
    Profit obtained 150 = 20 + 70 + 60.

Example 3:
    Input: startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
    Output: 6

Constraints:
-------------
- 1 <= startTime.length == endTime.length == profit.length <= 5 * 10^4
- 1 <= startTime[i] < endTime[i] <= 10^9
- 1 <= profit[i] <= 10^4

Approach:
---------
Approach 1 - Sort by end time + DP with binary search (implemented as the
primary solution):
    This is the classic "weighted interval scheduling" problem.

    1. Pair up (start, end, profit) for each job and sort the jobs by
       their end time.
    2. Let `dp[i]` = the maximum profit achievable using only the first
       `i` jobs (in end-time sorted order). `dp[0] = 0`.
    3. For the i-th job (1-indexed, sorted by end time), we have two
       choices:
         a) Skip it: profit = dp[i-1].
         b) Take it: profit = profit[i] + dp[j], where `j` is the number
            of jobs (in the sorted order) whose end time is <= this job's
            start time (i.e., the latest job that doesn't conflict).
       Because the jobs are sorted by end time, the ends of the first
       `j` jobs form a sorted array, so we can binary search
       (bisect_right) for the start time of the current job to find `j`
       in O(log n).
    4. `dp[i] = max(dp[i-1], profit[i] + dp[j])`.
    5. The answer is `dp[n]`.

    Why it works: sorting by end time lets us process jobs in an order
    where "all jobs compatible with job i that could be taken before it"
    are exactly a prefix of the dp array, discoverable via binary search
    on end times, which is what makes the O(n log n) approach correct and
    efficient (this is a textbook application of DP + binary search for
    weighted interval scheduling).

Approach 2 (alternative) - Top-down memoized recursion:
    Sort jobs by start time. Define `solve(i)` = max profit obtainable
    considering jobs from index `i` onward.
    - Option A: skip job i -> solve(i + 1).
    - Option B: take job i -> profit[i] + solve(next), where `next` is
      the index of the first job (in start-time sorted order) whose start
      time is >= end time of job i (found via binary search).
    `solve(i) = max(option A, option B)`, memoized on `i`. Same overall
    O(n log n) complexity, just phrased as top-down recursion instead of
    bottom-up DP.

Complexity Analysis:
---------------------
Approach 1 (bottom-up DP + binary search):
    Time:  O(n log n) - O(n log n) to sort, and O(log n) binary search
           for each of the n jobs.
    Space: O(n) - dp array and the sorted jobs list.

Approach 2 (top-down memoized recursion):
    Time:  O(n log n) - same reasoning as above.
    Space: O(n) - memoization cache plus recursion stack (O(n) worst
           case).
"""

from bisect import bisect_right
from functools import lru_cache
from typing import List


def job_scheduling(
    startTime: List[int], endTime: List[int], profit: List[int]
) -> int:
    """Bottom-up DP with binary search, sorted by end time."""
    jobs = sorted(zip(startTime, endTime, profit), key=lambda job: job[1])
    n = len(jobs)
    ends = [job[1] for job in jobs]

    dp = [0] * (n + 1)  # dp[i] = best profit using first i sorted jobs
    for i in range(1, n + 1):
        start, end, prof = jobs[i - 1]
        # Find count of jobs (in ends[0:i-1]) whose end <= start.
        j = bisect_right(ends, start, 0, i - 1)
        dp[i] = max(dp[i - 1], prof + dp[j])

    return dp[n]


def job_scheduling_top_down(
    startTime: List[int], endTime: List[int], profit: List[int]
) -> int:
    """Alternative: top-down memoized recursion, sorted by start time."""
    jobs = sorted(zip(startTime, endTime, profit), key=lambda job: job[0])
    starts = [job[0] for job in jobs]
    n = len(jobs)

    @lru_cache(maxsize=None)
    def solve(i: int) -> int:
        if i == n:
            return 0
        # Skip job i.
        best = solve(i + 1)
        # Take job i: find next index whose start >= jobs[i].end.
        _, end, prof = jobs[i]
        nxt = bisect_right(starts, end - 1)
        # bisect_right(starts, end - 1) gives first index with start > end-1,
        # i.e. start >= end, since starts are integers.
        best = max(best, prof + solve(nxt))
        return best

    result = solve(0)
    solve.cache_clear()
    return result


if __name__ == "__main__":
    # Example 1
    assert job_scheduling([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]) == 120
    assert (
        job_scheduling_top_down([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]) == 120
    )

    # Example 2
    assert (
        job_scheduling([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60])
        == 150
    )
    assert (
        job_scheduling_top_down(
            [1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]
        )
        == 150
    )

    # Example 3
    assert job_scheduling([1, 1, 1], [2, 3, 4], [5, 6, 4]) == 6
    assert job_scheduling_top_down([1, 1, 1], [2, 3, 4], [5, 6, 4]) == 6

    # Single job
    assert job_scheduling([1], [2], [100]) == 100

    # All jobs overlap completely -> take only the best one
    assert job_scheduling([1, 1, 1, 1], [5, 5, 5, 5], [10, 20, 5, 15]) == 20

    # All jobs are back-to-back (touching endpoints allowed) -> take all
    assert job_scheduling([1, 3, 5, 7], [3, 5, 7, 9], [10, 10, 10, 10]) == 40

    # Two jobs, non-overlapping -> take both
    assert job_scheduling([1, 10], [2, 20], [5, 5]) == 10

    print("All tests passed!")
