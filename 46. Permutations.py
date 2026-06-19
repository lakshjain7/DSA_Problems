"""
Problem Number: 46
Title: Permutations
Difficulty: Medium
Topics: Array, Backtracking

Problem Statement:
    Given an array `nums` of distinct integers, return all the possible permutations.
    You can return the answer in any order.

Examples:
    Input:  nums = [1, 2, 3]
    Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

    Input:  nums = [0, 1]
    Output: [[0,1],[1,0]]

    Input:  nums = [1]
    Output: [[1]]

Constraints:
    - 1 <= nums.length <= 6
    - -10 <= nums[i] <= 10
    - All the integers of nums are unique.

Approach:
    Backtracking — at each step, choose an unused number to place at the current
    position. Recurse until all positions are filled, then record the permutation.
    Backtrack by un-marking the choice and trying the next option.

    We track which elements have been used with a boolean `used` array so we avoid
    O(n) `in` checks per call.

Complexity:
    Time:  O(n * n!) — there are n! permutations, each of length n to copy.
    Space: O(n)     — recursion depth n, plus the `current` list of length n.
                      Output space O(n * n!) is not counted in auxiliary space.
"""

from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    """Return all permutations of the distinct integer array `nums`."""
    result: List[List[int]] = []
    used = [False] * len(nums)
    current: List[int] = []

    def backtrack() -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i, num in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            current.append(num)
            backtrack()
            current.pop()
            used[i] = False

    backtrack()
    return result


# ---------------------------------------------------------------------------
# Alternative Approach: Swap-based in-place backtracking
# ---------------------------------------------------------------------------
def permute_swap(nums: List[int]) -> List[List[int]]:
    """
    Alternative: swap each element into the current position, recurse, then
    swap back.  Avoids the extra `used` array entirely.

    Time:  O(n * n!)
    Space: O(n)  (recursion depth only; operates in-place on `nums`)
    """
    result: List[List[int]] = []

    def backtrack(start: int) -> None:
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # undo swap

    backtrack(0)
    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    def sorted_perms(perms):
        return sorted(tuple(p) for p in perms)

    # Basic: 3 elements → 6 permutations
    expected_3 = sorted_perms([[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]])
    assert sorted_perms(permute([1, 2, 3])) == expected_3
    assert sorted_perms(permute_swap([1, 2, 3])) == expected_3

    # 2 elements
    expected_2 = sorted_perms([[0,1],[1,0]])
    assert sorted_perms(permute([0, 1])) == expected_2
    assert sorted_perms(permute_swap([0, 1])) == expected_2

    # Single element
    assert permute([1]) == [[1]]
    assert permute_swap([1]) == [[1]]

    # Negative numbers
    expected_neg = sorted_perms([[-1,1],[ 1,-1]])
    assert sorted_perms(permute([-1, 1])) == expected_neg

    # 4 elements → 24 permutations
    result_4 = permute([1, 2, 3, 4])
    assert len(result_4) == 24
    assert len(set(tuple(p) for p in result_4)) == 24  # all unique

    print("All tests passed!")
