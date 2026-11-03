"""
47. Permutations II
Difficulty: Medium
Topics: Array, Backtracking, Sorting

Problem:
Given a collection of numbers, nums, that might contain duplicates, return all
possible unique permutations in any order.

Example 1:
    Input: nums = [1,1,2]
    Output: [[1,1,2],[1,2,1],[2,1,1]]

Example 2:
    Input: nums = [1,2,3]
    Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Constraints:
    1 <= nums.length <= 8
    -10 <= nums[i] <= 10

Approach (sort + used[] backtracking):
    Sort so equal numbers are adjacent. Build the permutation position by
    position. At each position skip a value if it is already used, and skip
    nums[i] if it equals nums[i-1] while nums[i-1] is NOT used in the current
    path -- that means the equal predecessor was already tried at this depth,
    so choosing nums[i] would repeat the same branch. This forces equal values
    to be placed in left-to-right order, giving each unique permutation once.

Complexity:
    Time:  O(n * n!) worst case (all distinct), output size dominates.
    Space: O(n) recursion + used array (excluding output).

Alternative (counter-based):
    Count occurrences and at each step pick any value with remaining count > 0.
    No sorting or skip rule needed.
"""
from collections import Counter
from typing import List


def permute_unique(nums: List[int]) -> List[List[int]]:
    nums = sorted(nums)
    n = len(nums)
    used = [False] * n
    path: List[int] = []
    res: List[List[int]] = []

    def backtrack() -> None:
        if len(path) == n:
            res.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return res


def permute_unique_counter(nums: List[int]) -> List[List[int]]:
    cnt = Counter(nums)
    n = len(nums)
    path: List[int] = []
    res: List[List[int]] = []

    def backtrack() -> None:
        if len(path) == n:
            res.append(path[:])
            return
        for v in list(cnt):
            if cnt[v] > 0:
                cnt[v] -= 1
                path.append(v)
                backtrack()
                path.pop()
                cnt[v] += 1

    backtrack()
    return res


if __name__ == "__main__":
    from itertools import permutations
    from math import factorial

    for fn in (permute_unique, permute_unique_counter):
        assert sorted(fn([1, 1, 2])) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
        assert len(fn([1, 2, 3])) == 6
        assert fn([1]) == [[1]]
        assert fn([2, 2, 2]) == [[2, 2, 2]]
        assert sorted(fn([0, -1, 0])) == [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]
        assert len(fn([1, 1, 2, 2])) == 6
        assert len(fn(list(range(8)))) == factorial(8)
        for arr in ([1, 2, 2, 3], [3, 3, 0, 0, 1], [1, 1, 1, 2, 2]):
            assert sorted(fn(arr)) == sorted(map(list, set(permutations(arr))))
    print("All tests passed")
