"""
40. Combination Sum II
Difficulty: Medium
Topics: Array, Backtracking

Problem:
Given a collection of candidate numbers (candidates) and a target number
(target), find all unique combinations in candidates where the candidate
numbers sum to target. Each number in candidates may only be used once in
the combination. The solution set must not contain duplicate combinations.

Examples:
    candidates = [10,1,2,7,6,1,5], target = 8
        -> [[1,1,6],[1,2,5],[1,7],[2,6]]
    candidates = [2,5,2,1,2], target = 5 -> [[1,2,2],[5]]

Constraints:
    1 <= candidates.length <= 100
    1 <= candidates[i] <= 50
    1 <= target <= 30

Approach (sort + backtracking with same-level duplicate skipping):
    Sort so equal values are adjacent. At each recursion level, iterate over
    choices starting at `start`; skip candidates[i] if it equals
    candidates[i-1] and i > start (that value was already tried at this
    level, so it would produce a duplicate combination). Recurse with i+1
    since each element is used once. Prune when the value exceeds the
    remaining target (sorted => all later values do too).

Complexity:
    Time: O(2^n) worst case   Space: O(n) recursion depth
"""
from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        res: List[List[int]] = []
        path: List[int] = []

        def dfs(start: int, remain: int) -> None:
            if remain == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                if candidates[i] > remain:
                    break
                path.append(candidates[i])
                dfs(i + 1, remain - candidates[i])
                path.pop()

        dfs(0, target)
        return res

    # Alternative: count-based backtracking over distinct values.
    def combinationSum2Counter(self, candidates: List[int], target: int) -> List[List[int]]:
        from collections import Counter
        items = sorted(Counter(candidates).items())
        res: List[List[int]] = []
        path: List[int] = []

        def dfs(idx: int, remain: int) -> None:
            if remain == 0:
                res.append(path[:])
                return
            if idx == len(items) or items[idx][0] > remain:
                return
            val, cnt = items[idx]
            dfs(idx + 1, remain)  # use zero copies
            used = 0
            while used < cnt and remain - val * (used + 1) >= 0:
                used += 1
                path.append(val)
                dfs(idx + 1, remain - val * used)
            for _ in range(used):
                path.pop()

        dfs(0, target)
        return res


if __name__ == "__main__":
    s = Solution()
    norm = lambda r: sorted(sorted(x) for x in r)
    for f in (s.combinationSum2, s.combinationSum2Counter):
        assert norm(f([10, 1, 2, 7, 6, 1, 5], 8)) == [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
        assert norm(f([2, 5, 2, 1, 2], 5)) == [[1, 2, 2], [5]]
        assert f([1], 2) == []
        assert f([1], 1) == [[1]]
        assert norm(f([1, 1, 1, 1], 2)) == [[1, 1]]
        assert f([3, 4], 2) == []
    print("All tests passed")
