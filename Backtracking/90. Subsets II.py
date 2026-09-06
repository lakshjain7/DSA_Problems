"""
90. Subsets II
Difficulty: Medium
Topics: Array, Backtracking, Bit Manipulation

Problem Statement
-----------------
Given an integer array `nums` that may contain duplicates, return all possible
subsets (the power set).

The solution set must NOT contain duplicate subsets. Return the solution in any order.

Examples
--------
Example 1:
    Input:  nums = [1, 2, 2]
    Output: [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]

Example 2:
    Input:  nums = [0]
    Output: [[], [0]]

Constraints
-----------
    1 <= nums.length <= 10
    -10 <= nums[i] <= 10

Approach
--------
The power set of a set with n distinct elements has 2^n subsets. Duplicates in
`nums` make some of those subsets identical, so we must avoid generating the
same subset twice.

Key idea: sort `nums` first so equal values sit next to each other. Then run a
standard subset-building backtrack. At each recursion level we iterate over the
candidate starting indices; to prevent duplicate subsets we skip any value that
equals the previous value *at the same tree depth*. Concretely, inside the loop
we skip index i (i > start) whenever nums[i] == nums[i - 1]. This guarantees
that among a run of equal numbers we only ever "start" a branch on the first
occurrence, while deeper occurrences can still be picked by extending that same
branch. That produces every distinct multiset-subset exactly once.

Why it works: sorting groups duplicates. The condition `i > start` means we only
skip a duplicate when it is NOT the first element chosen at this level. The first
occurrence spawns the branch that includes k copies for every k; forbidding
later occurrences from *starting* a sibling branch removes the redundant
identical subsets.

Complexity
----------
Time:  O(n * 2^n) - there are up to 2^n subsets and copying each costs O(n).
Space: O(n) auxiliary for the recursion stack and current path (excluding the
       output). Sorting adds O(log n) stack / O(n) depending on implementation.

Alternative Approach (Iterative)
--------------------------------
Build subsets incrementally. Start with [[]]. For each number, append it to
existing subsets. When the current number equals the previous one, only extend
the subsets that were newly created in the previous step (tracked with a start
index) to avoid duplicates. This is an O(n * 2^n) iterative equivalent that
avoids recursion.
"""

from typing import List


def subsetsWithDup(nums: List[int]) -> List[List[int]]:
    """Backtracking solution. Returns all unique subsets."""
    nums.sort()
    res: List[List[int]] = []
    path: List[int] = []

    def backtrack(start: int) -> None:
        res.append(path[:])
        for i in range(start, len(nums)):
            # Skip duplicates at the same tree depth.
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return res


def subsetsWithDup_iterative(nums: List[int]) -> List[List[int]]:
    """Iterative alternative that grows the subset list level by level."""
    nums.sort()
    res: List[List[int]] = [[]]
    start = 0  # index in res where subsets from the previous number begin
    for i, num in enumerate(nums):
        # If current equals previous, only extend the subsets added last round.
        begin = start if i > 0 and num == nums[i - 1] else 0
        start = len(res)
        for j in range(begin, start):
            res.append(res[j] + [num])
    return res


def _canonical(subsets: List[List[int]]) -> set:
    """Normalize a list of subsets into a comparable set of tuples."""
    return {tuple(sorted(s)) for s in subsets}


if __name__ == "__main__":
    # Example 1
    r1 = subsetsWithDup([1, 2, 2])
    expected1 = _canonical([[], [1], [1, 2], [1, 2, 2], [2], [2, 2]])
    assert _canonical(r1) == expected1, r1
    assert len(r1) == 6  # no duplicate subsets

    # Example 2
    r2 = subsetsWithDup([0])
    assert _canonical(r2) == _canonical([[], [0]]), r2

    # All identical elements -> subsets are [], [2], [2,2], [2,2,2]
    r3 = subsetsWithDup([2, 2, 2])
    assert _canonical(r3) == _canonical([[], [2], [2, 2], [2, 2, 2]]), r3
    assert len(r3) == 4

    # All distinct -> full power set of size 2^n
    r4 = subsetsWithDup([1, 2, 3])
    assert len(r4) == 8
    assert _canonical(r4) == _canonical(
        [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    )

    # Negative numbers and duplicates
    r5 = subsetsWithDup([-1, -1, 0])
    assert _canonical(r5) == _canonical([[], [-1], [-1, -1], [-1, -1, 0], [-1, 0], [0]]), r5

    # Iterative alternative must match backtracking on random-ish inputs
    for test in ([1, 2, 2], [0], [2, 2, 2], [1, 2, 3], [-1, -1, 0], [4, 4, 4, 1, 4]):
        assert _canonical(subsetsWithDup(list(test))) == _canonical(
            subsetsWithDup_iterative(list(test))
        ), test

    # No subset appears twice
    r6 = subsetsWithDup([4, 4, 4, 1, 4])
    assert len(r6) == len(_canonical(r6))

    print("All tests passed for 90. Subsets II")
