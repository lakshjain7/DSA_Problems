from typing import List
from collections import defaultdict
import heapq

class Solution:
    """
    Count shortest-paths to destination using Dijkstra's algorithm with path counting.
    This method computes the number of distinct shortest paths from node 0 to node n-1
    in an undirected, weighted graph given by `roads`. The answer is returned modulo 10^9 + 7.
    Parameters
    ----------
    n : int
        Number of nodes in the graph. Nodes are expected to be labeled 0..n-1.
    roads : List[List[int]]
        Edge list where each element is [u, v, t] representing an undirected edge
        between nodes u and v with travel time t (non-negative integer).
    Returns
    -------
    int
        The number of different shortest paths from node 0 to node n-1 modulo 10^9 + 7.
        If the destination is unreachable, returns 0.
    Algorithm
    ---------
    - Uses a min-heap (priority queue) to perform Dijkstra's algorithm to find
      shortest distances from node 0 to all nodes.
    - Maintains a parallel `ways` array where ways[x] is the count of shortest
      paths to node x discovered so far.
    - When a strictly shorter path to a neighbor is found, update its distance
      and set its ways equal to the current node's ways.
    - When an equally short path is found, increment the neighbor's ways by
      the current node's ways.
    - All additions are performed modulo MOD = 10**9 + 7.
    Time and Space Complexity
    -------------------------
    - Time: O(E log V) where E is the number of edges and V == n (due to heap operations).
    - Space: O(V + E) for adjacency storage, distance and ways arrays, and the heap.
    Notes
    -----
    - The input graph is treated as undirected: each road adds adjacency in both directions.
    - Assumes non-negative travel times; negative weights will invalidate Dijkstra's approach.
    - Nodes are assumed to be reachable via indices in range [0, n-1].
    """
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        MOD = 10**9 + 7
        graph = defaultdict(list)
        for u, v, t in roads:
            graph[u].append((v, t))
            graph[v].append((u, t))
        
        dist = [float('inf')] * n
        ways = [0] * n
        
        dist[0] = 0
        ways[0] = 1
        heap = [(0, 0)]  # (time, node)
        
        while heap:
            time, node = heapq.heappop(heap)
            
            if time > dist[node]:
                continue
            
            for nei, t in graph[node]:
                new_time = time + t
                if new_time < dist[nei]:
                    dist[nei] = new_time
                    ways[nei] = ways[node] % MOD
                    heapq.heappush(heap, (new_time, nei))
                elif new_time == dist[nei]:
                    ways[nei] = (ways[nei] + ways[node]) % MOD
        
        return ways[n-1] % MOD
