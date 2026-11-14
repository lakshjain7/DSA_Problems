"""
1335. Minimum Difficulty of a Job Schedule
Difficulty: Hard
Topics: Array, Dynamic Programming, Monotonic Stack

Problem:
You want to schedule a list of jobs in d days. Jobs are dependent (i.e. to work
on the i-th job, you have to finish all the jobs j where 0 <= j < i).

You have to finish at least one task every day. The difficulty of a job schedule
is the sum of difficulties of each day of the d days. The difficulty of a day is
the maximum difficulty of a job done on that day.

You are given an integer array `jobDifficulty` and an integer d. The difficulty
of the i-th job is jobDifficulty[i].

Return the minimum difficulty of a job schedule. If you cannot find a schedule
for the jobs return -1.

Example 1:
    Input: jobDifficulty = [6,5,4,3,2,1], d = 2
    Output: 7
    Explanation: Day 1 does the first 5 jobs (difficulty 6), day 2 does the last
    job (difficulty 1). Total = 7.

Example 2:
    Input: jobDifficulty = [9,9,9], d = 4
    Output: -1
    Explanation: Fewer jobs than days - at least one job per day is impossible.

Example 3:
    Input: jobDifficulty = [1,1,1], d = 3
    Output: 3

Constraints:
    1 <= jobDifficulty.length <= 300
    0 <= jobDifficulty[i] <= 1000
    1 <= d <= 10

Approach (DP over prefixes, partition into d contiguous segments):
    Let dp[k][i] = minimum difficulty to finish the first i jobs in exactly k days.
    The k-th day covers jobs j..i-1 for some j in [k-1, i-1], so
        dp[k][i] = min over j of ( dp[k-1][j] + max(jobs[j..i-1]) ).
    Iterate j downward from i-1 while maintaining a running max, so each
    transition is O(1). Base: dp[0][0] = 0. Answer: dp[d][n].

    Why it works: any valid schedule is a split of the job array into d non-empty
    contiguous blocks; the last block's cost depends only on its own range, so
    the optimal schedule = optimal (d-1)-day schedule of the prefix + last block.

Complexity:
    Time:  O(d * n^2)  (<= 10 * 300^2 = 9e5 operations)
    Space: O(n) using two rolling rows.

Alternative (monotonic stack, O(d * n)):
    For a fixed day k, process i left to right with a stack of candidate segment
    maxima. When jobs[i] dominates the max of the segment at stack top, that
    segment's best "previous dp" can be merged into the current one, because its
    last-day cost now becomes jobs[i]. Implemented in `minDifficulty_stack`.
"""
from itertools import combinations
from typing import List

INF = float("inf")


def minDifficulty(jobDifficulty: List[int], d: int) -> int:
    n = len(jobDifficulty)
    if n < d:
        return -1
    prev = [INF] * (n + 1)
    prev[0] = 0
    for k in range(1, d + 1):
        cur = [INF] * (n + 1)
        for i in range(k, n - (d - k) + 1):
            mx = 0
            best = INF
            for j in range(i - 1, k - 2, -1):  # day k covers jobs[j..i-1]
                mx = max(mx, jobDifficulty[j])
                if prev[j] + mx < best:
                    best = prev[j] + mx
            cur[i] = best
        prev = cur
    return int(prev[n])


def minDifficulty_stack(jobDifficulty: List[int], d: int) -> int:
    """O(d * n) DP using a monotonic decreasing stack per day."""
    n = len(jobDifficulty)
    if n < d:
        return -1
    # prev[i]: min cost of first i+1 jobs (0..i) in k-1 days
    prev = [INF] * n
    mx = 0
    for i in range(n):
        mx = max(mx, jobDifficulty[i])
        prev[i] = mx  # one day
    for _ in range(2, d + 1):
        cur = [INF] * n
        stack: List[int] = []  # indices of jobs, decreasing difficulty
        for i in range(1, n):
            # option: job i alone starts a fresh segment after prefix 0..i-1
            cur[i] = prev[i - 1] + jobDifficulty[i]
            while stack and jobDifficulty[stack[-1]] <= jobDifficulty[i]:
                j = stack.pop()
                # segment that had max jobs[j] now has max jobs[i]
                cur[i] = min(cur[i], cur[j] - jobDifficulty[j] + jobDifficulty[i])
            if stack:
                # the last day can extend back past i and keep the larger max
                cur[i] = min(cur[i], cur[stack[-1]])
            stack.append(i)
        prev = cur
    return int(prev[n - 1])


def _brute(jobs: List[int], d: int) -> int:
    n = len(jobs)
    if n < d:
        return -1
    best = INF
    for cuts in combinations(range(1, n), d - 1):
        b = (0,) + cuts + (n,)
        best = min(best, sum(max(jobs[b[t]:b[t + 1]]) for t in range(d)))
    return int(best)


if __name__ == "__main__":
    import random

    for fn in (minDifficulty, minDifficulty_stack):
        assert fn([6, 5, 4, 3, 2, 1], 2) == 7
        assert fn([9, 9, 9], 4) == -1
        assert fn([1, 1, 1], 3) == 3
        assert fn([7, 1, 7, 1, 7, 1], 3) == 15
        assert fn([11, 111, 22, 222, 33, 333, 44, 444], 6) == 843
        assert fn([0], 1) == 0                       # single job
        assert fn([5, 0, 0, 0], 1) == 5              # one day takes the max
        assert fn([3, 2, 1], 3) == 6                 # each job its own day

    random.seed(7)
    for _ in range(500):
        n = random.randint(1, 9)
        jobs = [random.randint(0, 20) for _ in range(n)]
        d = random.randint(1, 6)
        exp = _brute(jobs, d)
        assert minDifficulty(jobs, d) == exp, (jobs, d)
        assert minDifficulty_stack(jobs, d) == exp, (jobs, d)
    print("All tests passed!")
