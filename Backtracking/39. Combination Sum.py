"""
Problem 39: Combination Sum
Difficulty: Medium
Topics: Array, Backtracking

Problem Statement:
Given an array of distinct integers 'candidates' and a target integer 'target',
return a list of all unique combinations of candidates where the chosen numbers sum to target.
You may return the combinations in any order.
The same number may be chosen from candidates an unlimited number of times.
Two combinations are unique if the frequency of at least one of the chosen numbers is different.
The test cases are generated such that the number of unique combinations that sum up to target
is less than 150 combinations for the given input.

Examples:
  Input: candidates = [2,3,6,7], target = 7
  Output: [[2,2,3],[7]]

  Input: candidates = [2,3,5], target = 8
  Output: [[2,2,2,2],[2,3,3],[3,5]]

  Input: candidates = [2], target = 1
  Output: []

Constraints:
  1 <= candidates.length <= 30
  2 <= candidates[i] <= 40
  All elements of candidates are distinct.
  1 <= target <= 40

Approach:
  Backtracking with pruning.
  Sort candidates first (enables early termination when candidate > remaining).
  At each step, try including each candidate starting from index i (to avoid duplicates).
  Recursively subtract the chosen candidate from target.
  Base cases:
    - remaining == 0: add current combination to results
    - remaining < 0 or no candidates left: prune (backtrack)
  Because we allow repeats, we pass the same index i (not i+1) when recurring.

Complexity:
  Time:  O(N^(T/M)) where N = len(candidates), T = target, M = min(candidates)
         (number of nodes in the recursion tree)
  Space: O(T/M) for the recursion stack depth

Alternative Approach:
  Dynamic Programming (bottom-up):
    dp[amount] = list of all combinations that sum to amount.
    For each amount from 1 to target, for each candidate c <= amount,
    extend dp[amount - c] with c.
  Produces the same result but iteratively. Uses more memory (stores all combinations).
"""

from typing import List


def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    """Backtracking solution."""
    candidates.sort()
    result = []

    def backtrack(start: int, current: List[int], remaining: int) -> None:
        if remaining == 0:
            result.append(list(current))
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remaining:
                break  # sorted, so all further candidates also too large
            current.append(c)
            backtrack(i, current, remaining - c)  # i, not i+1: allow reuse
            current.pop()

    backtrack(0, [], target)
    return result


def combinationSum_dp(candidates: List[int], target: int) -> List[List[int]]:
    """Alternative: DP approach building up combinations iteratively."""
    dp: List[List[List[int]]] = [[] for _ in range(target + 1)]
    dp[0] = [[]]  # one way to make 0: empty combination

    for amount in range(1, target + 1):
        for c in candidates:
            if c <= amount:
                for combo in dp[amount - c]:
                    # Only add if combo is already sorted & c >= last element (avoid dups)
                    if not combo or c >= combo[-1]:
                        dp[amount].append(combo + [c])

    return dp[target]


if __name__ == "__main__":
    def sorted_result(lst):
        return sorted(sorted(x) for x in lst)

    # Test 1
    r = combinationSum([2, 3, 6, 7], 7)
    assert sorted_result(r) == sorted_result([[2, 2, 3], [7]])

    # Test 2
    r = combinationSum([2, 3, 5], 8)
    assert sorted_result(r) == sorted_result([[2, 2, 2, 2], [2, 3, 3], [3, 5]])

    # Test 3: no combination
    r = combinationSum([2], 1)
    assert r == []

    # Test 4: single element exact match
    r = combinationSum([7], 7)
    assert sorted_result(r) == [[7]]

    # Test 5: multiple repeats
    r = combinationSum([2], 6)
    assert sorted_result(r) == [[2, 2, 2]]

    # Test DP alternative
    r = combinationSum_dp([2, 3, 6, 7], 7)
    assert sorted_result(r) == sorted_result([[2, 2, 3], [7]])

    r = combinationSum_dp([2, 3, 5], 8)
    assert sorted_result(r) == sorted_result([[2, 2, 2, 2], [2, 3, 3], [3, 5]])

    print("All tests passed!")
