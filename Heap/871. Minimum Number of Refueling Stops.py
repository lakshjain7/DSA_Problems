"""
871. Minimum Number of Refueling Stops
Difficulty: Hard
Topics: Array, Dynamic Programming, Greedy, Heap (Priority Queue)

Problem Statement:
    A car travels from a starting position to a destination which is `target`
    miles east of the starting position.

    There are gas stations along the way. The stations are given as an array
    `stations` where stations[i] = [position_i, fuel_i] indicates that the i-th
    gas station is position_i miles east of the starting position and has fuel_i
    liters of gas.

    The car starts with an infinite tank of gas, which initially has `startFuel`
    liters of fuel in it. It uses one liter of gas per one mile that it drives.
    When the car reaches a gas station, it may stop and refuel, transferring all
    the gas from the station into the car.

    Return the minimum number of refueling stops the car must make in order to
    reach its destination. If it cannot reach the destination, return -1.

    Note: If the car reaches a gas station with 0 fuel left, the car can still
    refuel there. If the car reaches the destination with 0 fuel left, it is
    still considered to have arrived.

Examples:
    Example 1:
        Input:  target = 1, startFuel = 1, stations = []
        Output: 0
        Explanation: We can reach the target without refueling.

    Example 2:
        Input:  target = 100, startFuel = 1, stations = [[10,100]]
        Output: -1
        Explanation: We can not reach the target (or even the first station).

    Example 3:
        Input:  target = 100, startFuel = 10,
                stations = [[10,60],[20,30],[30,30],[60,40]]
        Output: 2
        Explanation: Start with 10 fuel, drive to position 10 (fuel 0), refuel
                     60 -> 60, drive to position 60 (fuel 10), refuel 40 -> 50,
                     drive to the target. Two refueling stops.

Constraints:
    - 1 <= target, startFuel <= 10^9
    - 0 <= stations.length <= 500
    - 1 <= position_i < position_{i+1} < target
    - 1 <= fuel_i < 10^9


Approach (Greedy + Max-Heap):
    Key insight: it does not matter WHEN we choose to take a station's fuel, only
    that we have passed it. So we defer the decision: as we advance, we "bank"
    every reachable station's fuel amount in a max-heap. Whenever we run out of
    fuel before reaching the next milestone, we retroactively pour in the biggest
    banked tank — that greedily buys the most distance for a single stop.

    Algorithm:
    1. Keep `fuel` = current reachable distance from start, and a max-heap of the
       fuel amounts of stations we have already driven past.
    2. Iterate over the stations (they are sorted by position), plus a virtual
       final station at `target` with 0 fuel.
    3. For each milestone at `position`, while `fuel < position`, pop the largest
       banked fuel and add it (incrementing the stop count). If the heap empties
       before we can reach `position`, the target is unreachable -> return -1.
    4. After ensuring we can reach `position`, push this station's fuel onto the
       heap.
    5. When we clear the virtual `target` milestone, return the stop count.

    Why it works (exchange argument): any optimal plan that reaches `target` using
    k stops uses some set of k stations, all at or before the point we ran dry.
    Greedily choosing the largest available tanks each time we stall gives, at
    every prefix, at least as much accumulated fuel as any other choice of the
    same number of stops — so it never needs more stops than optimal.

Complexity:
    Let n = number of stations.
    Time:  O(n log n) — each station is pushed and popped from the heap at most
           once, each heap operation O(log n).
    Space: O(n) — the heap can hold up to n station fuel amounts.


Alternative Approach (Dynamic Programming, O(n^2)):
    Let dp[t] be the farthest distance reachable using exactly t refueling stops.
    Initialize dp[0] = startFuel. For each station (pos, fuel), iterate t from
    high to low; if dp[t] >= pos then dp[t+1] = max(dp[t+1], dp[t] + fuel). The
    answer is the smallest t with dp[t] >= target. This is included below and
    cross-checked against the heap solution in the tests.
"""

import heapq
from typing import List


class Solution:
    def minRefuelStops(
        self, target: int, startFuel: int, stations: List[List[int]]
    ) -> int:
        """Greedy max-heap. Time O(n log n), space O(n)."""
        max_heap: List[int] = []  # store negatives for a max-heap
        fuel = startFuel
        stops = 0

        # Append a virtual station at the target with no fuel.
        for position, amount in stations + [[target, 0]]:
            while fuel < position:
                if not max_heap:
                    return -1
                fuel += -heapq.heappop(max_heap)
                stops += 1
            heapq.heappush(max_heap, -amount)

        return stops

    def minRefuelStopsDP(
        self, target: int, startFuel: int, stations: List[List[int]]
    ) -> int:
        """Dynamic programming. Time O(n^2), space O(n)."""
        n = len(stations)
        # dp[t] = farthest distance reachable with exactly t stops.
        dp = [startFuel] + [0] * n
        for i, (position, amount) in enumerate(stations):
            for t in range(i, -1, -1):
                if dp[t] >= position:
                    dp[t + 1] = max(dp[t + 1], dp[t] + amount)
        for t in range(n + 1):
            if dp[t] >= target:
                return t
        return -1


if __name__ == "__main__":
    sol = Solution()

    def check(target, start, stations, expected):
        assert (
            sol.minRefuelStops(target, start, [s[:] for s in stations]) == expected
        )
        assert (
            sol.minRefuelStopsDP(target, start, [s[:] for s in stations]) == expected
        )

    # Example cases
    check(1, 1, [], 0)
    check(100, 1, [[10, 100]], -1)
    check(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]], 2)

    # Edge: exactly enough start fuel, no stations
    check(50, 50, [], 0)

    # Edge: arrives with 0 fuel at target (counts as arrived)
    check(10, 10, [], 0)

    # Must use every station
    check(100, 10, [[10, 10], [20, 10], [30, 30], [60, 40]], 4)

    # Small first tank is not enough to reach the next station -> unreachable.
    check(100, 10, [[10, 5], [20, 40], [30, 5], [40, 60]], -1)

    # Greedy prefers the single big tank over several small ones.
    check(100, 10, [[10, 30], [20, 5], [30, 5], [40, 90]], 2)

    # Cannot reach the first station at all
    check(1000, 5, [[10, 1000]], -1)

    # Single station is enough with one stop
    check(200, 100, [[50, 200]], 1)

    # Larger deterministic check against brute-force minimum via DP already inside
    check(
        1000,
        1,
        [[1, 100], [100, 200], [200, 300], [300, 400], [400, 500], [500, 600]],
        4,
    )

    print("All tests passed for 871. Minimum Number of Refueling Stops")
