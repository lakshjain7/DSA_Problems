"""
1964. Find the Longest Valid Obstacle Course at Each Position
Difficulty: Hard
Topics: Array, Binary Search, Binary Indexed Tree, Longest Increasing Subsequence

Problem:
You want to build some obstacle courses. You are given a 0-indexed integer
array `obstacles` of length n, where obstacles[i] describes the height of the
ith obstacle.

For every index i between 0 and n - 1 (inclusive), find the length of the
longest obstacle course in `obstacles` such that:
    - You choose any number of obstacles between 0 and i inclusive.
    - You must include the ith obstacle in the course.
    - You must put the chosen obstacles in the same order as they appear.
    - Every obstacle (except the first) is taller than or the same height as
      the obstacle immediately before it.

Return an array `ans` of length n, where ans[i] is the length of the longest
obstacle course for index i as described above.

Example 1:
    Input: obstacles = [1,2,3,2]
    Output: [1,2,3,3]
    Explanation: i=3 -> [1,2,_,2] has length 3.

Example 2:
    Input: obstacles = [2,2,1]
    Output: [1,2,1]

Example 3:
    Input: obstacles = [3,1,5,6,4,2]
    Output: [1,1,2,3,2,2]

Constraints:
    n == obstacles.length
    1 <= n <= 10^5
    1 <= obstacles[i] <= 10^7

Approach (patience sorting / LIS with binary search):
    This is "longest non-decreasing subsequence ending at i" for every i.
    Maintain tails[k] = the smallest possible last height of a valid course of
    length k+1 seen so far. `tails` is always non-decreasing.
    For obstacle h, the longest course it can extend is the longest one whose
    tail is <= h. Because duplicates are allowed, we use bisect_right(tails, h):
    the index p is the count of tails <= h, so the course ending at h has
    length p+1. Then set tails[p] = h (append if p == len(tails)) -- h is a
    smaller-or-equal tail for length p+1 than whatever was there, keeping
    tails minimal, which is what makes the greedy optimal.

Complexity:
    Time:  O(n log n) -- one binary search per element.
    Space: O(n)       -- tails array and output.

Alternative (Fenwick tree over compressed heights):
    Coordinate-compress heights; for each h query the prefix max of best
    lengths over heights <= h, answer = that + 1, then point-update at h.
    Also O(n log n), more general (works for weighted variants).
"""
from bisect import bisect_right
from typing import List


class Solution:
    def longestObstacleCourseAtEachPosition(self, obstacles: List[int]) -> List[int]:
        tails: List[int] = []
        ans: List[int] = []
        for h in obstacles:
            p = bisect_right(tails, h)
            if p == len(tails):
                tails.append(h)
            else:
                tails[p] = h
            ans.append(p + 1)
        return ans

    def longestObstacleCourseFenwick(self, obstacles: List[int]) -> List[int]:
        rank = {v: i + 1 for i, v in enumerate(sorted(set(obstacles)))}
        m = len(rank)
        tree = [0] * (m + 1)

        def query(i: int) -> int:
            best = 0
            while i > 0:
                best = max(best, tree[i])
                i -= i & -i
            return best

        def update(i: int, val: int) -> None:
            while i <= m:
                if tree[i] < val:
                    tree[i] = val
                i += i & -i

        ans: List[int] = []
        for h in obstacles:
            r = rank[h]
            cur = query(r) + 1
            update(r, cur)
            ans.append(cur)
        return ans


def _brute(obstacles: List[int]) -> List[int]:
    n = len(obstacles)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if obstacles[j] <= obstacles[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return dp


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([1, 2, 3, 2], [1, 2, 3, 3]),
        ([2, 2, 1], [1, 2, 1]),
        ([3, 1, 5, 6, 4, 2], [1, 1, 2, 3, 2, 2]),
        ([5], [1]),
        ([7, 7, 7, 7], [1, 2, 3, 4]),          # all equal -> non-decreasing
        ([5, 4, 3, 2, 1], [1, 1, 1, 1, 1]),    # strictly decreasing
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    ]
    for obs, exp in cases:
        assert s.longestObstacleCourseAtEachPosition(obs) == exp, obs
        assert s.longestObstacleCourseFenwick(obs) == exp, obs

    random.seed(1964)
    for _ in range(300):
        arr = [random.randint(1, 6) for _ in range(random.randint(1, 25))]
        exp = _brute(arr)
        assert s.longestObstacleCourseAtEachPosition(arr) == exp, arr
        assert s.longestObstacleCourseFenwick(arr) == exp, arr

    big = list(range(1, 100001))
    assert s.longestObstacleCourseAtEachPosition(big)[-1] == 100000
    print("All tests passed!")
