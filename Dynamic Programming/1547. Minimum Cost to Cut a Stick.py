"""
1547. Minimum Cost to Cut a Stick
Difficulty: Hard
Topics: Array, Dynamic Programming, Sorting (Interval DP)

Problem:
Given a wooden stick of length n units. The stick is labelled from 0 to n.
Given an integer array cuts where cuts[i] denotes a position you should
perform a cut at.

You should perform the cuts in order; you can change the order of the cuts as
you wish. The cost of one cut is the length of the stick to be cut; the total
cost is the sum of costs of all cuts. When you cut a stick, it will be split
into two smaller sticks (the sum of their lengths is the length of the stick
before the cut).

Return the minimum total cost of the cuts.

Example 1:
    Input: n = 7, cuts = [1,3,4,5]
    Output: 16
    Explanation: Cutting in order [3,5,1,4] costs 7 + 4 + 3 + 2 = 16.
    (The given order [1,3,4,5] costs 7 + 6 + 4 + 3 = 20.)

Example 2:
    Input: n = 9, cuts = [5,6,1,4,2]
    Output: 22

Constraints:
    2 <= n <= 10^6
    1 <= cuts.length <= min(n - 1, 100)
    1 <= cuts[i] <= n - 1
    All the integers in cuts are distinct.

Approach (Interval DP):
Sort cuts and add the stick ends: pts = [0] + sorted(cuts) + [n].
Let dp[i][j] = min cost to make every cut strictly between pts[i] and pts[j]
on the segment [pts[i], pts[j]]. Think of the FIRST cut made on that segment,
at pts[k] (i < k < j): it costs the segment length pts[j] - pts[i], and then
the two halves are independent subproblems:
    dp[i][j] = (pts[j] - pts[i]) + min_{i<k<j} (dp[i][k] + dp[k][j])
Base case: dp[i][i+1] = 0 (no cut points inside). Fill by increasing gap j - i.
Answer: dp[0][m+1] where m = len(cuts).
This is the same structure as Burst Balloons / Matrix Chain Multiplication:
choosing the first (or last) action on an interval splits it cleanly.

Complexity (m = len(cuts)):
    Time:  O(m^3)  — O(m^2) intervals, O(m) split points each
    Space: O(m^2)
Note n itself (up to 10^6) never matters — only the m+2 cut positions do.

Alternative (top-down memoization):
Recursive solve(i, j) with lru_cache over the same state; identical
complexity, often easier to derive first.
"""
from functools import lru_cache
from typing import List


def min_cost(n: int, cuts: List[int]) -> int:
    pts = [0] + sorted(cuts) + [n]
    size = len(pts)
    dp = [[0] * size for _ in range(size)]
    for gap in range(2, size):
        for i in range(size - gap):
            j = i + gap
            best = min(dp[i][k] + dp[k][j] for k in range(i + 1, j))
            dp[i][j] = best + pts[j] - pts[i]
    return dp[0][size - 1]


def min_cost_memo(n: int, cuts: List[int]) -> int:
    pts = [0] + sorted(cuts) + [n]

    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> int:
        if j - i < 2:
            return 0
        return pts[j] - pts[i] + min(solve(i, k) + solve(k, j) for k in range(i + 1, j))

    return solve(0, len(pts) - 1)


def _brute(n: int, cuts: List[int]) -> int:
    from itertools import permutations
    best = float("inf")
    for order in permutations(cuts):
        segs = [(0, n)]
        cost = 0
        for c in order:
            for idx, (l, r) in enumerate(segs):
                if l < c < r:
                    cost += r - l
                    segs[idx:idx + 1] = [(l, c), (c, r)]
                    break
        best = min(best, cost)
    return best


if __name__ == "__main__":
    cases = [
        (7, [1, 3, 4, 5], 16),
        (9, [5, 6, 1, 4, 2], 22),
        (2, [1], 2),               # single cut costs full length
        (10, [5], 10),
        (4, [1, 2, 3], 8),         # cut middle first: 4 + 2 + 2
        (1_000_000, [1, 999_999], 1_999_999),  # huge n, few cuts
    ]
    for n, cuts, expected in cases:
        assert min_cost(n, cuts) == expected, (n, cuts)
        assert min_cost_memo(n, cuts) == expected, (n, cuts)

    import random
    random.seed(1547)
    for _ in range(200):
        n = random.randint(2, 15)
        k = random.randint(1, min(n - 1, 6))
        cuts = random.sample(range(1, n), k)
        assert min_cost(n, cuts) == min_cost_memo(n, cuts) == _brute(n, cuts), (n, cuts)
    print("All tests passed for 1547. Minimum Cost to Cut a Stick")
