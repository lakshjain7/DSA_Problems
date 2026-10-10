"""
1192. Critical Connections in a Network
Difficulty: Hard
Topics: Depth-First Search, Graph, Biconnected Component

Problem:
There are n servers numbered from 0 to n - 1 connected by undirected
server-to-server connections forming a network where connections[i] = [a, b]
represents a connection between servers a and b. Any server can reach other
servers directly or indirectly through the network.
A critical connection is a connection that, if removed, will make some servers
unable to reach some other server.
Return all critical connections in the network in any order.

Example 1:
    Input: n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]
    Output: [[1,3]]
Example 2:
    Input: n = 2, connections = [[0,1]]
    Output: [[0,1]]

Constraints:
    2 <= n <= 10^5
    n - 1 <= connections.length <= 10^5
    0 <= a_i, b_i <= n - 1, a_i != b_i, no repeated connections

Approach (Tarjan's bridge-finding):
    Run DFS recording disc[u] (discovery time) and low[u] (earliest discovery
    time reachable from u's subtree using at most one back edge). For a tree
    edge u->v, if low[v] > disc[u], then v's subtree cannot reach u or above
    except through this edge, so (u, v) is a bridge. Skip the parent edge
    when updating low. An iterative DFS avoids recursion limits for n = 1e5.

Complexity:
    Time:  O(V + E)
    Space: O(V + E)

Alternative: chain decomposition - remove every edge belonging to a cycle
found by DFS; edges not covered by any cycle are bridges.
"""
from typing import List


def criticalConnections(n: int, connections: List[List[int]]) -> List[List[int]]:
    adj = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)

    disc = [-1] * n
    low = [0] * n
    res: List[List[int]] = []
    timer = 0
    for s in range(n):
        if disc[s] != -1:
            continue
        disc[s] = low[s] = timer
        timer += 1
        stack = [(s, -1, iter(adj[s]))]
        while stack:
            u, parent, it = stack[-1]
            advanced = False
            for v in it:
                if v == parent:
                    continue
                if disc[v] == -1:
                    disc[v] = low[v] = timer
                    timer += 1
                    stack.append((v, u, iter(adj[v])))
                    advanced = True
                    break
                low[u] = min(low[u], disc[v])
            if not advanced:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[u])
                    if low[u] > disc[p]:
                        res.append([p, u])
    return res


def criticalConnections_bruteforce(n: int, connections: List[List[int]]) -> List[List[int]]:
    """Alternative (verification): remove each edge and test connectivity."""
    def connected(skip: int) -> bool:
        adj = [[] for _ in range(n)]
        for i, (a, b) in enumerate(connections):
            if i != skip:
                adj[a].append(b)
                adj[b].append(a)
        seen = {0}
        st = [0]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        return len(seen) == n

    return [c for i, c in enumerate(connections) if not connected(i)]


def _norm(r):
    return sorted(sorted(x) for x in r)


if __name__ == "__main__":
    assert _norm(criticalConnections(4, [[0, 1], [1, 2], [2, 0], [1, 3]])) == [[1, 3]]
    assert _norm(criticalConnections(2, [[0, 1]])) == [[0, 1]]
    # path graph: every edge is a bridge
    assert _norm(criticalConnections(4, [[0, 1], [1, 2], [2, 3]])) == [[0, 1], [1, 2], [2, 3]]
    # a single cycle: no bridges
    assert criticalConnections(3, [[0, 1], [1, 2], [2, 0]]) == []
    # two triangles joined by a bridge
    g = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 3]]
    assert _norm(criticalConnections(6, g)) == [[2, 3]]
    import random
    for _ in range(200):
        n = random.randint(2, 9)
        edges = [[i, random.randint(0, i - 1)] for i in range(1, n)]  # spanning tree
        have = {tuple(sorted(e)) for e in edges}
        for _ in range(random.randint(0, 5)):
            a, b = random.sample(range(n), 2)
            if tuple(sorted((a, b))) not in have:
                have.add(tuple(sorted((a, b))))
                edges.append([a, b])
        assert _norm(criticalConnections(n, edges)) == _norm(criticalConnections_bruteforce(n, edges))
    # large path (no recursion issues)
    n = 100000
    big = [[i, i + 1] for i in range(n - 1)]
    assert len(criticalConnections(n, big)) == n - 1
    print("All tests passed")
