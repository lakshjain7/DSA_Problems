"""
1552. Magnetic Force Between Two Balls
Difficulty: Medium
Topics: Array, Binary Search, Sorting

Problem:
In the universe Earth C-137, Rick discovered a special form of magnetic force
between two balls if they are put in his new invented basket. Rick has n empty
baskets, the ith basket is at position[i]. Morty has m balls and needs to
distribute the balls into the baskets such that the minimum magnetic force
between any two balls is maximum.

Rick stated that magnetic force between two different balls at positions x and
y is |x - y|.

Given the integer array position and the integer m. Return the required force.

Example 1:
    Input: position = [1,2,3,4,7], m = 3
    Output: 3
    Explanation: Balls at 1, 4 and 7 give forces [3, 3, 6]; min is 3.
                 No placement achieves a minimum greater than 3.

Example 2:
    Input: position = [5,4,3,2,1,1000000000], m = 2
    Output: 999999999
    Explanation: Use baskets 1 and 1000000000.

Constraints:
    n == position.length
    2 <= n <= 10^5
    1 <= position[i] <= 10^9
    All integers in position are distinct.
    2 <= m <= position.length

Approach (Binary Search on the Answer + Greedy Check):
    Feasibility is monotonic: if we can place m balls with every gap >= d, we
    can also do it for any d' < d. So binary search the largest feasible d.
    Check(d): sort positions, put the first ball in the leftmost basket, then
    greedily put the next ball in the first basket at least d away from the
    previous ball. Greedy-leftmost is optimal because placing a ball as early
    as possible never reduces the room left for subsequent balls (exchange
    argument). Feasible iff we place >= m balls.
    Search range: lo = 1, hi = (max - min) // (m - 1) (the gaps sum to at most
    max - min, so the smallest of m-1 gaps cannot exceed the average).

Complexity:
    Time:  O(n log n + n log(R)) where R = (max - min)/(m - 1).
    Space: O(n) for the sorted copy (O(1) extra if sorting in place).
"""
from typing import List


def max_distance(position: List[int], m: int) -> int:
    pos = sorted(position)

    def can_place(d: int) -> bool:
        count, last = 1, pos[0]
        for p in pos[1:]:
            if p - last >= d:
                count += 1
                last = p
                if count >= m:
                    return True
        return count >= m

    lo, hi = 1, (pos[-1] - pos[0]) // (m - 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2      # upper mid -> search for last True
        if can_place(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def max_distance_candidate_gaps(position: List[int], m: int) -> int:
    """Alternative: the answer is always a difference of two positions, so
    binary search over the sorted set of candidate pairwise distances is
    possible but O(n^2) to enumerate. Here we keep it practical for small n by
    testing candidate distances in descending order -- useful as a reference
    implementation (not for the full constraints)."""
    pos = sorted(position)
    cands = sorted({b - a for i, a in enumerate(pos) for b in pos[i + 1:]}, reverse=True)
    for d in cands:
        count, last = 1, pos[0]
        for p in pos[1:]:
            if p - last >= d:
                count += 1
                last = p
        if count >= m:
            return d
    return 0


if __name__ == "__main__":
    import random

    assert max_distance([1, 2, 3, 4, 7], 3) == 3
    assert max_distance([5, 4, 3, 2, 1, 1000000000], 2) == 999999999
    assert max_distance([1, 2], 2) == 1                 # minimal input
    assert max_distance([1, 2, 3, 4, 5], 5) == 1        # every basket used
    assert max_distance([1, 100], 2) == 99
    assert max_distance([79, 74, 57, 22], 4) == 5       # unsorted input
    assert max_distance(list(range(1, 100001)), 2) == 99999

    random.seed(1)
    for _ in range(300):
        n = random.randint(2, 12)
        arr = random.sample(range(1, 60), n)
        k = random.randint(2, n)
        assert max_distance(arr, k) == max_distance_candidate_gaps(arr, k), (arr, k)

    print("All tests passed for 1552. Magnetic Force Between Two Balls")
