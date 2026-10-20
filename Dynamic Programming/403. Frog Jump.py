"""
403. Frog Jump
Difficulty: Hard
Topics: Array, Dynamic Programming, Hash Table

Problem:
A frog is crossing a river. The river is divided into some number of units,
and at each unit, there may or may not exist a stone. The frog can jump on a
stone, but it must not jump into the water. Given a list of stones positions
(in units) in sorted ascending order, determine if the frog can cross the
river by landing on the last stone. Initially, the frog is on the first stone
and assumes the first jump must be 1 unit. If the frog's last jump was k
units, its next jump must be either k - 1, k, or k + 1 units. The frog can
only jump in the forward direction.

Examples:
    stones = [0,1,3,5,6,8,12,17] -> True
    stones = [0,1,2,3,4,8,9,11]  -> False

Constraints:
    2 <= stones.length <= 2000
    0 <= stones[i] <= 2^31 - 1
    stones[0] == 0, stones strictly increasing

Approach (DP with set of reachable jump sizes per stone):
    dp[pos] = set of jump sizes k with which the frog can land on stone pos.
    dp[0] = {0}. For each stone in order and each k in dp[pos], try next
    jumps k-1, k, k+1 (must be > 0); if pos + step is a stone, add step to
    its set. Answer: the last stone has a non-empty set.

Complexity:
    Time: O(n^2)   Space: O(n^2)
"""
from functools import lru_cache
from typing import List
import sys


class Solution:
    def canCross(self, stones: List[int]) -> bool:
        if stones[1] != 1:
            return False
        dp = {s: set() for s in stones}
        dp[0].add(0)
        for pos in stones:
            for k in dp[pos]:
                for step in (k - 1, k, k + 1):
                    if step > 0 and pos + step in dp:
                        dp[pos + step].add(step)
        return bool(dp[stones[-1]])

    # Alternative: top-down memoized DFS on (index, last jump).
    def canCrossMemo(self, stones: List[int]) -> bool:
        sys.setrecursionlimit(10000)
        idx = {s: i for i, s in enumerate(stones)}
        last = stones[-1]

        @lru_cache(maxsize=None)
        def dfs(pos: int, k: int) -> bool:
            if pos == last:
                return True
            for step in (k + 1, k, k - 1):
                if step > 0 and pos + step in idx and dfs(pos + step, step):
                    return True
            return False

        return stones[1] == 1 and dfs(1, 1) if len(stones) > 1 else True


if __name__ == "__main__":
    s = Solution()
    for f in (s.canCross, s.canCrossMemo):
        assert f([0, 1, 3, 5, 6, 8, 12, 17]) is True
        assert f([0, 1, 2, 3, 4, 8, 9, 11]) is False
        assert f([0, 1]) is True
        assert f([0, 2]) is False
        assert f([0, 1, 3]) is True
        assert f([0, 1, 2, 3, 4, 5, 6]) is True
        assert f([0, 1, 3, 6, 10, 15, 21]) is True
        assert f([0, 1, 3, 6, 10, 15, 16, 21]) is True
    print("All tests passed")
