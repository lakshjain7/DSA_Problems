"""
1235. Maximum Profit in Job Scheduling
Difficulty: Hard
Topics: Array, Binary Search, Dynamic Programming, Sorting

Problem Statement:
We have n jobs, where every job is scheduled to be done from startTime[i] to
endTime[i], obtaining a profit of profit[i].

You're given the startTime, endTime and profit arrays. Return the maximum profit
you can take such that there are no two jobs in the subset with overlapping time
range.

If you choose a job that ends at time X you will be able to start another job
that starts at time X.

Example 1:
    Input:  startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
    Output: 120
    Explanation: The subset chosen is the first and fourth job.
    Time range [1-3]+[3-6], we get profit of 120 = 50 + 70.

Example 2:
    Input:  startTime = [1,2,3,4,6], endTime = [3,5,10,6,9],
            profit = [20,20,100,70,60]
    Output: 150
    Explanation: The subset chosen is the first, fourth and fifth job.
    Profit obtained 150 = 20 + 70 + 60.

Example 3:
    Input:  startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
    Output: 6

Constraints:
    - 1 <= startTime.length == endTime.length == profit.length <= 5 * 10^4
    - 1 <= startTime[i] < endTime[i] <= 10^9
    - 1 <= profit[i] <= 10^4

--------------------------------------------------------------------------------
Approach (Sort by end time + DP with binary search):
This is the weighted interval scheduling problem. The classic solution sorts jobs
by end time and defines:

    dp[i] = maximum profit achievable using only the first i jobs (in end-sorted
            order).

For the i-th job (1-indexed) with (start, end, p), we have two choices:
    - Skip it:  dp[i-1]
    - Take it:  p + dp[j], where j is the number of jobs whose end time is
                <= this job's start time. Because jobs are sorted by end time,
                that count is found by binary-searching the array of end times
                for the rightmost end <= start.

    dp[i] = max(dp[i-1], p + dp[j])

The answer is dp[n].

Why sort by end time:
Sorting by end time makes "the latest non-conflicting job" a contiguous prefix of
the sorted order, so a single binary search over end times locates the best
compatible predecessor. dp is monotonic non-decreasing in i, so dp[j] is the best
profit among all jobs ending at or before the current job's start.

Complexity:
    Time:  O(n log n) - sorting plus a binary search per job.
    Space: O(n) - the dp array and the end-time array.

--------------------------------------------------------------------------------
Alternative Approach (Sort by start time + heap):
Sort jobs by start time and use a min-heap keyed by end time. Track the best
profit realized among all jobs that have already ended; when processing a job,
pop everything from the heap that ends at or before its start to update that
running best, then push (end, running_best + profit). The maximum profit ever
pushed is the answer. Also O(n log n).
"""

from typing import List
from bisect import bisect_right
import heapq


class Solution:
    def jobScheduling(
        self, startTime: List[int], endTime: List[int], profit: List[int]
    ) -> int:
        jobs = sorted(zip(endTime, startTime, profit))  # sort by end time
        ends = [j[0] for j in jobs]
        n = len(jobs)

        # dp[i] = best profit using first i jobs (end-sorted). dp[0] = 0.
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            end, start, p = jobs[i - 1]
            # Rightmost job index whose end <= start (among jobs[0..i-2]).
            j = bisect_right(ends, start, 0, i - 1)
            dp[i] = max(dp[i - 1], dp[j] + p)

        return dp[n]

    def jobScheduling_heap(
        self, startTime: List[int], endTime: List[int], profit: List[int]
    ) -> int:
        jobs = sorted(zip(startTime, endTime, profit))  # sort by start time
        heap: List[tuple] = []  # (end_time, profit_accumulated_up_to_end)
        best = 0  # best profit among jobs already finished
        answer = 0

        for start, end, p in jobs:
            while heap and heap[0][0] <= start:
                _, prof = heapq.heappop(heap)
                best = max(best, prof)
            heapq.heappush(heap, (end, best + p))
            answer = max(answer, best + p)

        return answer


if __name__ == "__main__":
    sol = Solution()

    for method in (sol.jobScheduling, sol.jobScheduling_heap):
        # Example 1
        assert method([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]) == 120
        # Example 2
        assert (
            method([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]) == 150
        )
        # Example 3
        assert method([1, 1, 1], [2, 3, 4], [5, 6, 4]) == 6
        # Single job
        assert method([5], [9], [7]) == 7
        # Two overlapping jobs -> pick the more profitable one
        assert method([1, 2], [10, 3], [5, 100]) == 100
        # Two non-overlapping jobs (touching endpoints) -> take both
        assert method([1, 3], [3, 5], [40, 60]) == 100
        # Chain where taking all is optimal
        assert method([1, 2, 3, 4], [2, 3, 4, 5], [10, 10, 10, 10]) == 40

    print("All tests passed for 1235. Maximum Profit in Job Scheduling")
