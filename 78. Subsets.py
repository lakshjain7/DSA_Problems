"""
Problem 78: Subsets
Difficulty: Medium
Topics: Array, Backtracking, Bit Manipulation

Problem Statement:
    Given an integer array nums of unique elements, return all possible subsets (the power set).
    The solution set must not contain duplicate subsets. Return the solution in any order.

Examples:
    Input: nums = [1,2,3]
    Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

    Input: nums = [0]
    Output: [[],[0]]

Constraints:
    - 1 <= nums.length <= 10
    - -10 <= nums[i] <= 10
    - All the numbers of nums are unique.

Approach:
    Backtracking (DFS):
    At each recursive step, we decide whether to include or skip the current element.
    We iterate through starting indices to avoid generating duplicate orderings.
    For each position i in nums:
      - Add nums[i] to the current path
      - Recurse from i+1 (forward only, so we never re-pick)
      - Remove nums[i] (backtrack)
    We record the current path at every recursive call (not just leaf nodes),
    because every partial build is a valid subset.

    Why this works: each element is either in or out of the subset. The recursion
    tree has 2^n leaves, and we capture all intermediate states, giving us all 2^n subsets.

Complexity:
    Time:  O(n * 2^n) -- 2^n subsets, each takes O(n) to copy into the result
    Space: O(n) recursion depth + O(n * 2^n) for the output

Alternative Approach (Bit Manipulation):
    For n elements, iterate integers from 0 to 2^n - 1. The i-th bit of the integer
    represents whether the i-th element is included. Clean and iterative, same complexity.
"""

from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    """Return all subsets of nums using backtracking."""
    result: List[List[int]] = []

    def backtrack(start: int, path: List[int]) -> None:
        result.append(list(path))  # every path (including empty) is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()  # undo the choice (backtrack)

    backtrack(0, [])
    return result


def subsets_bit_manipulation(nums: List[int]) -> List[List[int]]:
    """Alternative: iterative approach using bit masks."""
    n = len(nums)
    result: List[List[int]] = []
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result


if __name__ == "__main__":
    # Helper to compare lists of lists regardless of order
    def normalize(lst_of_lists):
        return sorted(tuple(sorted(sub)) for sub in lst_of_lists)

    # Test 1: standard case
    result = subsets([1, 2, 3])
    expected = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    assert normalize(result) == normalize(expected), f"Test 1 failed: {result}"

    # Test 2: single element
    result = subsets([0])
    expected = [[], [0]]
    assert normalize(result) == normalize(expected), f"Test 2 failed: {result}"

    # Test 3: two elements
    result = subsets([1, 2])
    expected = [[], [1], [2], [1, 2]]
    assert normalize(result) == normalize(expected), f"Test 3 failed: {result}"

    # Test 4: negative numbers
    result = subsets([-1, 0, 1])
    assert len(result) == 8, f"Test 4 size failed: {len(result)}"
    assert [] in result, "Test 4: empty subset missing"
    assert [-1, 0, 1] in result, "Test 4: full set missing"

    # Test 5: verify count is always 2^n
    for n in range(1, 6):
        nums = list(range(n))
        assert len(subsets(nums)) == 2 ** n, f"Test 5 failed for n={n}"

    # Test 6: bit manipulation alternative matches backtracking
    for test in [[1, 2, 3], [0], [4, 5]]:
        assert normalize(subsets(test)) == normalize(subsets_bit_manipulation(test)), \
            f"Mismatch between approaches for {test}"

    print("All tests passed for 78. Subsets!")
