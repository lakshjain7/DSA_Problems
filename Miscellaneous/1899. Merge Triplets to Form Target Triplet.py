"""
1899. Merge Triplets to Form Target Triplet
Difficulty: Medium
Topics: Array, Greedy

Problem:
A triplet is an array of three integers. You are given a 2D integer array
triplets, where triplets[i] = [a_i, b_i, c_i] describes the i-th triplet. You
are also given an integer array target = [x, y, z] that describes the triplet
you want to obtain.

To obtain target, you may apply the following operation on triplets any number
of times (possibly zero):
  Choose two indices (0-indexed) i and j (i != j) and update triplets[j] to
  become [max(a_i, a_j), max(b_i, b_j), max(c_i, c_j)].

Return true if it is possible to obtain the target triplet [x, y, z] as an
element of triplets, or false otherwise.

Example 1:
    Input: triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]
    Output: true   (merge [2,5,3] and [1,7,5] -> [2,7,5])

Example 2:
    Input: triplets = [[3,4,5],[4,5,6]], target = [3,2,5]
    Output: false

Example 3:
    Input: triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target = [5,5,5]
    Output: true

Constraints:
    1 <= triplets.length <= 10^5
    triplets[i].length == target.length == 3
    1 <= a_i, b_i, c_i, x, y, z <= 1000

Approach (Greedy filter):
Merging takes element-wise max, so values only ever grow. Any triplet with some
coordinate strictly greater than the target's can never be part of the merge —
it would push that coordinate past the target forever. Discard those.
Every remaining triplet is "safe": merging all of them never exceeds target.
The max over the safe set equals target iff, for each coordinate k, some safe
triplet hits target[k] exactly. So track which coordinates are matched by safe
triplets; answer is true iff all three are matched.

Complexity:
    Time:  O(n)
    Space: O(1)

Alternative:
Explicitly fold all safe triplets with element-wise max and compare the result
to target — same complexity, slightly more direct.
"""
from typing import List


def merge_triplets(triplets: List[List[int]], target: List[int]) -> bool:
    found = set()
    for t in triplets:
        if t[0] > target[0] or t[1] > target[1] or t[2] > target[2]:
            continue
        for k in range(3):
            if t[k] == target[k]:
                found.add(k)
        if len(found) == 3:
            return True
    return len(found) == 3


def merge_triplets_fold(triplets: List[List[int]], target: List[int]) -> bool:
    cur = [0, 0, 0]
    for t in triplets:
        if all(t[k] <= target[k] for k in range(3)):
            cur = [max(cur[k], t[k]) for k in range(3)]
    return cur == target


if __name__ == "__main__":
    cases = [
        ([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5], True),
        ([[3, 4, 5], [4, 5, 6]], [3, 2, 5], False),
        ([[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], [5, 5, 5], True),
        ([[1, 1, 1]], [1, 1, 1], True),               # already present
        ([[1, 2, 3]], [1, 2, 4], False),              # single, short
        ([[1, 3, 1], [3, 1, 1]], [3, 3, 3], False),   # z never reached
        ([[5, 1, 1], [1, 5, 9], [1, 1, 5]], [5, 5, 5], False),  # middle one unsafe
        ([[5, 1, 1], [1, 5, 1], [1, 1, 5]], [5, 5, 5], True),
    ]
    for trips, target, expected in cases:
        assert merge_triplets(trips, target) == expected, (trips, target)
        assert merge_triplets_fold(trips, target) == expected, (trips, target)
    print("All tests passed for 1899. Merge Triplets to Form Target Triplet")
