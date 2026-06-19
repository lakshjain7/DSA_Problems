import heapq
from collections import defaultdict
from typing import List

class Solution:
    """
    Calculates the minimum time required for all nodes to receive a signal sent from a starting node in a directed, weighted graph.
    Uses Dijkstra's algorithm to find the shortest path from the starting node `k` to all other nodes. If it is impossible for all nodes to receive the signal, returns -1.
    Args:
        arr (List[List[int]]): A list of directed edges, where each edge is represented as [u, v, w] indicating a signal travels from node u to node v in w units of time.
        n (int): The total number of nodes in the graph, labeled from 1 to n.
        k (int): The starting node from which the signal is sent.
    Returns:
        int: The minimum time required for all nodes to receive the signal. Returns -1 if not all nodes can be reached.
    """
    def networkDelayTime(self, arr: List[List[int]], n: int, k: int) -> int:
        g = defaultdict(list)
        for u, v, w in arr:
            g[u].append((v, w))
        
        # Min-heap for (time, node)
        heap = [(0.0, k)]
        visited = set()
        dist = {i: float('inf') for i in range(1, n + 1)}
        dist[k] = 0.0
        
        while heap:
            time, node = heapq.heappop(heap)
            
            # Skip if already visited
            if node in visited:
                continue
            visited.add(node)
            
            # Update neighbors
            for nei, wt in g[node]:
                if time + wt < dist[nei]:
                    dist[nei] = time + wt
                    heapq.heappush(heap, (float(dist[nei]), nei))
        
        # If all nodes are reached, return max time; else -1
        ans = max(dist.values())
        return int(ans) if ans < float('inf') else -1
