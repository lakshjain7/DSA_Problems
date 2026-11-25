"""
1626. Best Team With No Conflicts
Difficulty: Medium
Topics: Array, Dynamic Programming, Sorting

Problem:
You are the manager of a basketball team. For the upcoming tournament, you want
to choose the team with the highest overall score. The score of the team is the
sum of scores of all the players in the team.

However, the basketball team is not allowed to have conflicts. A conflict exists
if a younger player has a strictly higher score than an older player. A conflict
does not occur between players of the same age.

Given two lists, `scores` and `ages`, where each scores[i] and ages[i] represents
the score and age of the i-th player, respectively, return the highest overall
score of all possible basketball teams.

Example 1:
    Input: scores = [1,3,5,10,15], ages = [1,2,3,4,5]
    Output: 34
    Explanation: You can choose all the players.

Example 2:
    Input: scores = [4,5,6,5], ages = [2,1,2,1]
    Output: 16
    Explanation: Choose the last 3 players (scores 5,6,5). Same-age players never conflict.

Example 3:
    Input: scores = [1,2,3,5], ages = [8,9,10,1]
    Output: 6
    Explanation: Choose the first 3 players.

Constraints:
    1 <= scores.length, ages.length <= 1000
    scores.length == ages.length
    1 <= scores[i] <= 10^6
    1 <= ages[i] <= 1000

Approach (Sort + LIS-style DP):
    Sort players by (age, score). After sorting, a team is conflict-free iff the
    scores along the sorted order are non-decreasing: within the same age, ties are
    broken by score so they're non-decreasing anyway; across ages, an older player
    must not have a lower score. So the problem becomes "maximum-sum non-decreasing
    subsequence" of the sorted scores.
    dp[i] = score[i] + max(dp[j] for j < i if score[j] <= score[i]), answer = max(dp).

Complexity:
    Time:  O(n^2)
    Space: O(n)

Alternative (Sort by score + Fenwick tree over ages, O(n log A)):
    Sort by (score, age). Now scores are non-decreasing, and we need ages to be
    non-decreasing too. Process players in that order; for each, query the max dp
    over ages <= age with a Binary Indexed Tree (prefix-max), then update at age.
"""

from typing import List


class Solution:
    def bestTeamScore(self, scores: List[int], ages: List[int]) -> int:
        players = sorted(zip(ages, scores))
        n = len(players)
        dp = [0] * n
        for i in range(n):
            si = players[i][1]
            best = 0
            for j in range(i):
                if players[j][1] <= si and dp[j] > best:
                    best = dp[j]
            dp[i] = best + si
        return max(dp)

    def bestTeamScoreBIT(self, scores: List[int], ages: List[int]) -> int:
        max_age = max(ages)
        tree = [0] * (max_age + 1)

        def query(i: int) -> int:
            res = 0
            while i > 0:
                res = max(res, tree[i])
                i -= i & -i
            return res

        def update(i: int, val: int) -> None:
            while i <= max_age:
                tree[i] = max(tree[i], val)
                i += i & -i

        ans = 0
        for score, age in sorted(zip(scores, ages)):
            cur = query(age) + score
            update(age, cur)
            ans = max(ans, cur)
        return ans


if __name__ == "__main__":
    sol = Solution()
    cases = [
        (([1, 3, 5, 10, 15], [1, 2, 3, 4, 5]), 34),
        (([4, 5, 6, 5], [2, 1, 2, 1]), 16),
        (([1, 2, 3, 5], [8, 9, 10, 1]), 6),
        (([7], [3]), 7),
        (([5, 5, 5], [1, 1, 1]), 15),
        (([10, 1], [1, 2]), 10),
        (([1, 10], [1, 2]), 11),
    ]
    for (sc, ag), exp in cases:
        assert sol.bestTeamScore(sc, ag) == exp, (sc, ag)
        assert sol.bestTeamScoreBIT(sc, ag) == exp, (sc, ag)

    import random
    from itertools import combinations

    def brute(sc, ag):
        n, best = len(sc), 0
        for r in range(1, n + 1):
            for comb in combinations(range(n), r):
                ok = all(not ((ag[a] < ag[b] and sc[a] > sc[b]) or (ag[b] < ag[a] and sc[b] > sc[a]))
                         for a, b in combinations(comb, 2))
                if ok:
                    best = max(best, sum(sc[k] for k in comb))
        return best

    for _ in range(200):
        n = random.randint(1, 7)
        sc = [random.randint(1, 10) for _ in range(n)]
        ag = [random.randint(1, 5) for _ in range(n)]
        b = brute(sc, ag)
        assert sol.bestTeamScore(sc, ag) == b
        assert sol.bestTeamScoreBIT(sc, ag) == b
    print("All tests passed!")
