"""
Problem Number: 787
Title: Cheapest Flights Within K Stops
Difficulty: Hard
Topics: Dynamic Programming, Depth-First Search, Breadth-First Search, Graph, Heap (Priority Queue),
        Shortest Path

Problem Statement:
There are n cities connected by some number of flights. You are given an array `flights` where
flights[i] = [from_i, to_i, price_i] indicates that there is a flight from city from_i to city
to_i with cost price_i.

Given three integers src, dst, and k, return the cheapest price from src to dst with at most k
stops. If there is no such route, return -1.

Examples:
    Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1
    Output: 700
    Explanation: Optimal path: 0 -> 1 -> 3 (cost 700, 1 stop)

    Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
    Output: 200
    Explanation: 0 -> 1 -> 2 (cost 200, 1 stop)

    Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
    Output: 500
    Explanation: Must go direct 0 -> 2 (no stops allowed)

Constraints:
    1 <= n <= 100
    0 <= flights.length <= (n * (n - 1) / 2)
    flights[i].length == 3
    0 <= from_i, to_i < n
    from_i != to_i
    1 <= price_i <= 10^4
    There will not be any multiple flights between two cities.
    0 <= src, dst, k < n
    src != dst

Approach (Bellman-Ford with k+1 relaxations):
    Run at most k+1 rounds of Bellman-Ford relaxation (one per edge we can traverse,
    meaning k stops = k+1 edges). Key insight: after round i, dist[v] = cheapest cost
    to reach v using exactly i edges from src.

    To avoid using edges added in the same round (which would let us chain more than
    one hop per round), copy the dist array before each round and only update from the copy.

    This runs in O(k * |flights|) time and O(n) space, which is ideal for sparse graphs.

Complexity:
    Time:  O(k * E) where E = number of flights
    Space: O(n) for the dist array

Alternative Approach (Modified Dijkstra with stop count):
    Use a min-heap with state (cost, node, stops_remaining). Unlike standard Dijkstra,
    we can't prune a node just because we visited it cheaply -- a more expensive path with
    more stops remaining might still be useful. We prune if stops_remaining is exhausted.
"""

import heapq
from typing import List
from collections import defaultdict


def findCheapestPrice(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """Bellman-Ford: k+1 edge relaxations."""
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0

    for _ in range(k + 1):
        # Work from a copy so we don't chain edges within a single round
        temp = dist[:]
        for u, v, price in flights:
            if dist[u] < INF:
                temp[v] = min(temp[v], dist[u] + price)
        dist = temp

    return dist[dst] if dist[dst] < INF else -1


def findCheapestPriceDijkstra(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """Modified Dijkstra with (cost, node, stops_used) state."""
    graph = defaultdict(list)
    for u, v, price in flights:
        graph[u].append((v, price))

    # (cost, node, stops_used)
    heap = [(0, src, 0)]
    visited = {}

    while heap:
        cost, node, stops = heapq.heappop(heap)
        if node == dst:
            return cost
        if stops > k:
            continue
        if (node, stops) in visited:
            continue
        visited[(node, stops)] = cost
        for neighbor, price in graph[node]:
            heapq.heappush(heap, (cost + price, neighbor, stops + 1))

    return -1


if __name__ == "__main__":
    # Example 1: path 0->1->3 costs 700 (1 stop)
    flights1 = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
    assert findCheapestPrice(4, flights1, 0, 3, 1) == 700
    assert findCheapestPriceDijkstra(4, flights1, 0, 3, 1) == 700

    # Example 2: 0->1->2 costs 200 (1 stop allowed)
    flights2 = [[0,1,100],[1,2,100],[0,2,500]]
    assert findCheapestPrice(3, flights2, 0, 2, 1) == 200
    assert findCheapestPriceDijkstra(3, flights2, 0, 2, 1) == 200

    # Example 3: k=0, must go direct
    assert findCheapestPrice(3, flights2, 0, 2, 0) == 500
    assert findCheapestPriceDijkstra(3, flights2, 0, 2, 0) == 500

    # No route exists
    assert findCheapestPrice(3, [[0,1,100]], 0, 2, 1) == -1
    assert findCheapestPriceDijkstra(3, [[0,1,100]], 0, 2, 1) == -1

    # Direct route cheaper than multi-hop
    flights4 = [[0,1,50],[0,2,200],[2,1,50]]
    assert findCheapestPrice(3, flights4, 0, 1, 1) == 50
    assert findCheapestPriceDijkstra(3, flights4, 0, 1, 1) == 50

    print("All tests passed!")
