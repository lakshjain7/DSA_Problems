"""
77. Combinations
Difficulty: Medium
Topics: Backtracking

Problem:
Given two integers n and k, return all possible combinations of k numbers
chosen from the range [1, n]. You may return the answer in any order.

Example 1:
    Input: n = 4, k = 2
    Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
Example 2:
    Input: n = 1, k = 1
    Output: [[1]]

Constraints:
    1 <= n <= 20
    1 <= k <= n

Approach:
Backtracking with an increasing start index so each combination is built in
sorted order (no duplicates). Prune: if the remaining numbers (n - start + 1)
are fewer than the slots still needed (k - len(path)), stop early.

Complexity: Time O(k * C(n, k)), Space O(k) recursion (excluding output).
"""
from itertools import combinations as _it_comb
from typing import List


def combine(n: int, k: int) -> List[List[int]]:
    res: List[List[int]] = []
    path: List[int] = []

    def dfs(start: int) -> None:
        if len(path) == k:
            res.append(path[:])
            return
        need = k - len(path)
        for x in range(start, n - need + 2):
            path.append(x)
            dfs(x + 1)
            path.pop()

    dfs(1)
    return res


def combine_iterative(n: int, k: int) -> List[List[int]]:
    """Alternative: iterative lexicographic generation."""
    c = list(range(1, k + 1)) + [n + 1]
    res = []
    j = 0
    while j < k:
        res.append(c[:k])
        j = 0
        while j < k and c[j + 1] == c[j] + 1:
            c[j] = j + 1
            j += 1
        c[j] += 1
    return res


if __name__ == "__main__":
    for f in (combine, combine_iterative):
        assert sorted(f(4, 2)) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        assert f(1, 1) == [[1]]
        assert f(3, 3) == [[1, 2, 3]]
        assert sorted(f(3, 1)) == [[1], [2], [3]]
        for n in range(1, 9):
            for k in range(1, n + 1):
                assert sorted(f(n, k)) == [list(t) for t in _it_comb(range(1, n + 1), k)]
    print("All tests passed")
