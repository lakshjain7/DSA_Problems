"""
Problem Number: 875
Title: Koko Eating Bananas
Difficulty: Medium
Topics: Binary Search, Array

Problem Statement:
    Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas.
    The guards have gone and will come back in h hours.
    Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of
    bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all
    of them instead and will not eat any more bananas during this hour.
    Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.
    Return the minimum integer k such that she can eat all the bananas within h hours.

Examples:
    Input: piles = [3,6,7,11], h = 8
    Output: 4

    Input: piles = [30,11,23,4,20], h = 5
    Output: 30

    Input: piles = [30,11,23,4,20], h = 6
    Output: 23

Constraints:
    1 <= piles.length <= 10^4
    piles.length <= h <= 10^9
    1 <= piles[i] <= 10^9

Approach:
    Binary search on the answer space [1, max(piles)].
    - Lower bound: 1 (minimum possible speed)
    - Upper bound: max(piles) (eating the largest pile in one hour is always sufficient)
    For a given speed k, total hours = sum(ceil(pile/k) for pile in piles).
    We binary search for the smallest k where total_hours <= h.

    Why binary search works: the feasibility function is monotone — if speed k works,
    then any speed > k also works. So we find the leftmost valid k.

Complexity:
    Time:  O(n log m) where n = len(piles), m = max(piles)
    Space: O(1)
"""

import math
from typing import List


def minEatingSpeed(piles: List[int], h: int) -> int:
    lo, hi = 1, max(piles)

    while lo < hi:
        mid = (lo + hi) // 2
        hours_needed = sum(math.ceil(p / mid) for p in piles)
        if hours_needed <= h:
            hi = mid       # mid might be optimal, try smaller
        else:
            lo = mid + 1   # too slow, need higher speed

    return lo


# Alternative: same logic with integer ceiling trick (avoids math.ceil import overhead)
def minEatingSpeed_v2(piles: List[int], h: int) -> int:
    lo, hi = 1, max(piles)

    while lo < hi:
        mid = (lo + hi) // 2
        hours_needed = sum((p + mid - 1) // mid for p in piles)
        if hours_needed <= h:
            hi = mid
        else:
            lo = mid + 1

    return lo


if __name__ == "__main__":
    # Basic examples
    assert minEatingSpeed([3, 6, 7, 11], 8) == 4
    assert minEatingSpeed([30, 11, 23, 4, 20], 5) == 30
    assert minEatingSpeed([30, 11, 23, 4, 20], 6) == 23

    # Edge: single pile, h == 1 must eat it all at once
    assert minEatingSpeed([1000000000], 1) == 1000000000

    # Edge: single pile, plenty of time
    assert minEatingSpeed([1000000000], 1000000000) == 1

    # All same piles
    assert minEatingSpeed([5, 5, 5, 5], 4) == 5   # exactly 4 hours at speed 5
    assert minEatingSpeed([5, 5, 5, 5], 8) == 3   # ceil(5/3)*4 = 2*4=8 hours

    # v2 matches v1
    assert minEatingSpeed_v2([3, 6, 7, 11], 8) == 4
    assert minEatingSpeed_v2([30, 11, 23, 4, 20], 5) == 30

    print("All tests passed for 875. Koko Eating Bananas")
