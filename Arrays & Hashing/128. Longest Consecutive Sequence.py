"""
Problem #128 — Longest Consecutive Sequence
Difficulty : Medium
Topics     : Array, Hash Set

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROBLEM STATEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Given an unsorted array of integers nums, return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Examples:
  Input: nums = [100,4,200,1,3,2]   →  Output: 4  (sequence: [1,2,3,4])
  Input: nums = [0,3,7,2,5,8,4,6,0,1]  →  Output: 9  (sequence: [0..8])
  Input: nums = []                   →  Output: 0

Constraints:
  0 <= nums.length <= 10^5
  -10^9 <= nums[i] <= 10^9

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
APPROACH — Hash Set with Sequence Start Detection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Naive sort-based approach is O(n log n). To achieve O(n):

1. Insert all numbers into a hash set (O(n) build, O(1) lookup).
2. Iterate over nums. For each number n, check if (n - 1) is NOT in the set.
   - If (n - 1) is absent, then n is the START of a new consecutive sequence.
   - Only at sequence starts do we count: extend the streak by checking
     n+1, n+2, ... until the next number is missing.
3. Track the maximum streak length seen.

Why this is O(n): each number is the start of a sequence at most once.
Non-start numbers are skipped in the outer loop (the (n-1) check). The inner
while-loop traverses each sequence only once total, so every element is touched
at most twice overall → O(n).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLEXITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Time  : O(n)  — each element visited at most twice
Space : O(n)  — hash set stores all elements
"""

from typing import List


def longest_consecutive(nums: List[int]) -> int:
    """Return length of longest consecutive sequence in O(n) time."""
    num_set = set(nums)
    best = 0

    for n in num_set:                   # iterate over set to avoid duplicate work
        if (n - 1) not in num_set:      # n is the start of a sequence
            current = n
            streak = 1
            while (current + 1) in num_set:
                current += 1
                streak += 1
            best = max(best, streak)

    return best


def longest_consecutive_union_find(nums: List[int]) -> int:
    """Union-Find alternative — O(n·α(n)) ≈ O(n)."""
    if not nums:
        return 0

    parent: dict[int, int] = {n: n for n in nums}
    size:   dict[int, int] = {n: 1 for n in nums}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    num_set = set(nums)
    for n in num_set:
        if n + 1 in num_set:
            union(n, n + 1)

    return max(size[find(n)] for n in num_set)


if __name__ == "__main__":
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    assert longest_consecutive([1]) == 1
    assert longest_consecutive([1, 2, 3, 4, 5]) == 5
    assert longest_consecutive([5, 4, 3, 2, 1]) == 5
    assert longest_consecutive([1, 3, 5, 7]) == 1
    assert longest_consecutive([1, 1, 1, 1]) == 1
    assert longest_consecutive([-3, -2, -1, 0, 1]) == 5
    assert longest_consecutive([0]) == 1

    for test in [[100, 4, 200, 1, 3, 2], [0, 3, 7, 2, 5, 8, 4, 6, 0, 1], [], [1, 3, 5, 7], [-3, -2, -1, 0, 1]]:
        assert longest_consecutive(test) == longest_consecutive_union_find(test)

    print("All assertions passed!")
