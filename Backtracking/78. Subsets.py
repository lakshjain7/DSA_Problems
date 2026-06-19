"""
Problem 78: Subsets
Difficulty: Medium
Topics: Array, Backtracking, Bit Manipulation

Given an integer array nums of unique elements, return all possible subsets.

Approach: Backtracking — record path at every node, not just leaves.
Alternative: Bit manipulation — iterate 0..2^n-1, use bits as inclusion mask.

Complexity: O(n * 2^n) time, O(n) recursion + O(n * 2^n) output.
"""

from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    result: List[List[int]] = []
    def backtrack(start: int, path: List[int]) -> None:
        result.append(list(path))
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result


def subsets_bit_manipulation(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    result: List[List[int]] = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result


if __name__ == "__main__":
    def normalize(lst): return sorted(tuple(sorted(s)) for s in lst)
    assert normalize(subsets([1, 2, 3])) == normalize([[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]])
    assert normalize(subsets([0])) == normalize([[], [0]])
    for test in [[1,2,3],[0],[4,5]]:
        assert normalize(subsets(test)) == normalize(subsets_bit_manipulation(test))
    for n in range(1, 6):
        assert len(subsets(list(range(n)))) == 2**n
    print("All tests passed for 78. Subsets!")
