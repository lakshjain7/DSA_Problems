"""
815. Bus Routes
Difficulty: Hard
Topics: Array, Hash Table, Breadth-First Search, Graph

Problem Statement
-----------------
You are given an array `routes` representing bus routes where routes[i] is a
bus route that the i-th bus repeats forever.

    - For example, if routes[0] = [1, 5, 7], this means that the 0-th bus
      travels in the sequence 1 -> 5 -> 7 -> 1 -> 5 -> 7 -> 1 -> ... forever.

You will start at the bus stop `source` (you are not on any bus initially),
and you want to go to the bus stop `target`. You can travel between bus stops
by buses only.

Return the least number of buses you must take to travel from `source` to
`target`. Return -1 if it is not possible.

Example 1:
    Input: routes = [[1,2,7],[3,6,7]], source = 1, target = 6
    Output: 2
    Explanation: The best strategy is take the first bus to the bus stop 7,
    then take the second bus to the bus stop 6.

Example 2:
    Input: routes = [[7,12],[4,5,15],[6],[15,19],[9,12,13]],
           source = 15, target = 12
    Output: -1

Constraints:
    1 <= routes.length <= 500
    1 <= routes[i].length <= 10^5
    All the values of routes[i] are unique.
    sum(routes[i].length) <= 10^5
    0 <= routes[i][j] < 10^6
    0 <= source, target < 10^6

Approach (BFS over BUSES, not stops)
------------------------------------
The key insight for a minimum-transfer question is to treat each *bus route*
as a node and do a BFS where one "level" = boarding one additional bus. Two
buses are connected if they share at least one stop (you can transfer between
them there).

Steps:
    1. Edge case: if source == target, the answer is 0 (no bus needed).
    2. Build stop -> list of buses that serve that stop (adjacency by stop).
    3. BFS seeded with every bus that serves `source`, distance = 1 (we must
       board at least one bus to move).
    4. For each bus dequeued, if any of its stops is `target`, return the
       current bus count. Otherwise, for each stop on that bus, enqueue all
       unvisited buses sharing that stop with count + 1. Mark stops as
       processed so we never re-expand a shared stop, keeping it near-linear.
    5. If BFS drains without reaching target, return -1.

Why BFS over buses gives the minimum: each BFS layer adds exactly one bus to
the journey, so the first time we encounter a bus covering `target`, we have
used the fewest buses possible (BFS explores in nondecreasing layer order).

Complexity
----------
Let N = number of routes and K = total stops across all routes (<= 10^5).
Time:  O(N^2 + K) in the worst case where many buses share stops, but each
       stop is expanded only once (O(K)) and each bus visited once; the
       N^2 term reflects buses pairwise sharing stops.
Space: O(N + K) for the stop->buses map, visited sets, and the queue.

Alternative Approach (BFS over stops with route-used tracking)
-------------------------------------------------------------
One can BFS over stops instead, marking whole routes as consumed once ridden.
It is equivalent in complexity but bookkeeping is messier (must avoid
re-walking a used route's stops). The bus-level BFS above is cleaner and is
the primary solution; a stop-level variant is provided for cross-checking.
"""

from typing import List
from collections import defaultdict, deque


def numBusesToDestination(routes: List[List[int]], source: int,
                          target: int) -> int:
    if source == target:
        return 0

    # stop -> buses serving it
    stop_to_buses = defaultdict(list)
    for bus, route in enumerate(routes):
        for stop in route:
            stop_to_buses[stop].append(bus)

    # If target (or source) never appears on any route, it's unreachable.
    if target not in stop_to_buses or source not in stop_to_buses:
        return -1

    visited_buses = set()
    visited_stops = set()
    queue = deque()

    # Seed BFS with all buses reachable from the source stop.
    for bus in stop_to_buses[source]:
        visited_buses.add(bus)
        queue.append((bus, 1))
    visited_stops.add(source)

    while queue:
        bus, count = queue.popleft()
        for stop in routes[bus]:
            if stop == target:
                return count
            if stop in visited_stops:
                continue
            visited_stops.add(stop)
            for nxt in stop_to_buses[stop]:
                if nxt not in visited_buses:
                    visited_buses.add(nxt)
                    queue.append((nxt, count + 1))

    return -1


def numBusesToDestinationStops(routes: List[List[int]], source: int,
                               target: int) -> int:
    """Alternative BFS over stops; marks routes as used once ridden."""
    if source == target:
        return 0

    stop_to_buses = defaultdict(list)
    for bus, route in enumerate(routes):
        for stop in route:
            stop_to_buses[stop].append(bus)

    visited_stops = {source}
    used_buses = set()
    queue = deque([(source, 0)])

    while queue:
        stop, buses_taken = queue.popleft()
        for bus in stop_to_buses[stop]:
            if bus in used_buses:
                continue
            used_buses.add(bus)
            for nxt in routes[bus]:
                if nxt == target:
                    return buses_taken + 1
                if nxt not in visited_stops:
                    visited_stops.add(nxt)
                    queue.append((nxt, buses_taken + 1))

    return -1


if __name__ == "__main__":
    for fn in (numBusesToDestination, numBusesToDestinationStops):
        # Example 1
        assert fn([[1, 2, 7], [3, 6, 7]], 1, 6) == 2

        # Example 2 - unreachable
        assert fn([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12) == -1

        # Source equals target -> 0 buses
        assert fn([[1, 2, 7], [3, 6, 7]], 1, 1) == 0
        assert fn([[1, 2, 3]], 2, 2) == 0

        # Single bus direct
        assert fn([[1, 2, 3, 4, 5]], 1, 5) == 1

        # Target not present anywhere
        assert fn([[1, 2, 3]], 1, 99) == -1

        # Source not present anywhere
        assert fn([[1, 2, 3]], 99, 3) == -1

        # Chain of transfers: 1->10 (bus0), 10->20 (bus1), 20->30 (bus2)
        assert fn([[1, 10], [10, 20], [20, 30]], 1, 30) == 3

        # Two independent buses meeting at a shared stop
        assert fn([[1, 2, 7], [3, 6, 7], [6, 8, 9]], 1, 9) == 3

        # Single stop route, source==target handled; disjoint otherwise
        assert fn([[6]], 6, 6) == 0

    print("All tests passed for 815. Bus Routes")
