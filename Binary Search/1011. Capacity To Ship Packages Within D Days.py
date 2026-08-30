"""
1011. Capacity To Ship Packages Within D Days
Difficulty: Medium
Topics: Array, Binary Search (on the answer space)

PROBLEM STATEMENT
-----------------
A conveyor belt has packages that must be shipped from one port to another
within `days` days.

The i-th package on the belt has a weight of `weights[i]`. Each day, we load the
ship with packages on the conveyor belt (in the order given by `weights`). We may
not load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages
being shipped within `days` days.

EXAMPLES
--------
Example 1:
  Input:  weights = [1,2,3,4,5,6,7,8,9,10], days = 5
  Output: 15
  Explanation: A ship capacity of 15 is the minimum to ship all packages in 5 days:
    Day 1: 1, 2, 3, 4, 5
    Day 2: 6, 7
    Day 3: 8
    Day 4: 9
    Day 5: 10
    Note that packages cannot be split, so capacities like 14 fail.

Example 2:
  Input:  weights = [3,2,2,4,1,4], days = 3
  Output: 6

Example 3:
  Input:  weights = [1,2,3,1,1], days = 4
  Output: 3

CONSTRAINTS
-----------
  - 1 <= days <= weights.length <= 5 * 10^4
  - 1 <= weights[i] <= 500

APPROACH (Binary Search on the Answer)
--------------------------------------
The answer (the ship capacity) is monotonic: if a capacity C can ship everything
within `days`, then any capacity > C can too. This monotonicity lets us binary
search over the capacity value rather than over an index.

Search bounds:
  - lo = max(weights): capacity must at least hold the single heaviest package,
    otherwise that package can never be loaded.
  - hi = sum(weights): with this capacity we can ship everything in a single day.

Feasibility check `can_ship(capacity)`:
  Greedily fill each day. Walk the packages in order, accumulating weight into the
  current day. When adding the next package would exceed `capacity`, start a new
  day. Count the days used; the capacity is feasible if days_used <= days.

Binary search:
  Find the smallest capacity in [lo, hi] for which `can_ship` returns True. Because
  feasibility is monotonic, standard lower-bound binary search converges to the
  minimum feasible capacity.

Why greedy feasibility is correct: loading order is fixed, so for a given capacity
there is exactly one way to pack "as much as fits each day"; taking the maximum
allowed each day minimizes the number of days, giving the true minimum day count.

COMPLEXITY
----------
  Let n = len(weights), S = sum(weights), W = max(weights).
  Time:  O(n * log(S - W)) - each feasibility check is O(n) and we run
         O(log(sum - max)) iterations of binary search.
  Space: O(1) extra.
"""

from typing import List


def ship_within_days(weights: List[int], days: int) -> int:
    """Return the minimum ship capacity to ship all packages within `days` days."""

    def can_ship(capacity: int) -> bool:
        days_used = 1
        current = 0
        for w in weights:
            if current + w > capacity:
                days_used += 1
                current = 0
            current += w
            if days_used > days:
                return False
        return days_used <= days

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(mid):
            hi = mid          # mid feasible; try to go smaller
        else:
            lo = mid + 1      # mid too small; need more capacity
    return lo


def ship_within_days_bruteforce(weights: List[int], days: int) -> int:
    """
    Linear scan over every candidate capacity from max(weights) to sum(weights).
    Correct but slow: O((sum - max) * n). Used only to cross-check tests.
    """
    def days_needed(capacity: int) -> int:
        d, cur = 1, 0
        for w in weights:
            if cur + w > capacity:
                d += 1
                cur = 0
            cur += w
        return d

    for cap in range(max(weights), sum(weights) + 1):
        if days_needed(cap) <= days:
            return cap
    return sum(weights)


if __name__ == "__main__":
    # Example cases
    assert ship_within_days([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
    assert ship_within_days([3, 2, 2, 4, 1, 4], 3) == 6
    assert ship_within_days([1, 2, 3, 1, 1], 4) == 3

    # One day -> capacity must equal the total sum
    assert ship_within_days([5, 4, 3, 2, 1], 1) == 15

    # As many days as packages -> capacity equals the heaviest package
    assert ship_within_days([5, 4, 3, 2, 1], 5) == 5

    # Single package
    assert ship_within_days([7], 1) == 7

    # All equal weights
    assert ship_within_days([2, 2, 2, 2], 2) == 4

    # Random cross-check against brute force
    import random
    for _ in range(300):
        n = random.randint(1, 12)
        weights = [random.randint(1, 20) for _ in range(n)]
        days = random.randint(1, n)
        assert ship_within_days(weights, days) == ship_within_days_bruteforce(weights, days)

    print("All tests passed for 1011. Capacity To Ship Packages Within D Days")
