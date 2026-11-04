"""
881. Boats to Save People
Difficulty: Medium
Topics: Array, Two Pointers, Greedy, Sorting

Problem:
You are given an array people where people[i] is the weight of the i-th person,
and an infinite number of boats where each boat can carry a maximum weight of
limit. Each boat carries at most two people at the same time, provided the sum
of their weights is at most limit. Return the minimum number of boats needed
to carry every given person.

Examples:
    people = [1,2], limit = 3        -> 1   (1 + 2)
    people = [3,2,2,1], limit = 3    -> 3   (1+2), (2), (3)
    people = [3,5,3,4], limit = 5    -> 4   (3), (3), (4), (5)

Constraints:
    1 <= people.length <= 5 * 10^4
    1 <= people[i] <= limit <= 3 * 10^4

Approach (sort + two pointers, greedy):
    Sort weights. The heaviest person must board some boat. Pairing them with
    the lightest remaining person is the best possible partner: if the lightest
    cannot fit with the heaviest, nobody can, so the heaviest rides alone.
    Otherwise pairing them wastes nothing (exchange argument). Move pointers
    inward accordingly, one boat per iteration.

Complexity:
    Time:  O(n log n) for the sort, O(n) for the scan.
    Space: O(1) extra (ignoring sort internals).
"""
from typing import List


def numRescueBoats(people: List[int], limit: int) -> int:
    people = sorted(people)
    lo, hi, boats = 0, len(people) - 1, 0
    while lo <= hi:
        if people[lo] + people[hi] <= limit:
            lo += 1
        hi -= 1
        boats += 1
    return boats


def numRescueBoatsCounting(people: List[int], limit: int) -> int:
    """Alternative: counting sort, O(n + limit) time, since weights <= limit."""
    cnt = [0] * (limit + 1)
    for w in people:
        cnt[w] += 1
    lo, hi, boats, remaining = 1, limit, 0, len(people)
    while remaining > 0:
        while lo <= limit and cnt[lo] == 0:
            lo += 1
        while hi >= 1 and cnt[hi] == 0:
            hi -= 1
        # Take one heaviest person
        cnt[hi] -= 1
        remaining -= 1
        # Try to pair with lightest
        while lo <= limit and cnt[lo] == 0:
            lo += 1
        if remaining > 0 and lo <= limit and lo + hi <= limit:
            cnt[lo] -= 1
            remaining -= 1
        boats += 1
    return boats


if __name__ == "__main__":
    for f in (numRescueBoats, numRescueBoatsCounting):
        assert f([1, 2], 3) == 1
        assert f([3, 2, 2, 1], 3) == 3
        assert f([3, 5, 3, 4], 5) == 4
        assert f([5], 5) == 1
        assert f([1, 1, 1, 1], 2) == 2
        assert f([2, 2, 2], 3) == 3
        assert f([1, 2, 3, 4, 5], 6) == 3
    import random
    for _ in range(300):
        limit = random.randint(1, 20)
        p = [random.randint(1, limit) for _ in range(random.randint(1, 12))]
        assert numRescueBoats(p, limit) == numRescueBoatsCounting(p, limit)
    print("All tests passed.")
