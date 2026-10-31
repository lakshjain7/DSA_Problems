"""
1857. Largest Color Value in a Directed Graph
Difficulty: Hard
Topics: Graph, Topological Sort, Dynamic Programming, Counting

There is a directed graph of n colored nodes and m edges. The nodes are
numbered from 0 to n - 1. You are given a string colors where colors[i] is a
lowercase English letter representing the color of the ith node, and a 2D
array edges where edges[j] = [aj, bj] indicates a directed edge from aj to bj.

A valid path is a sequence of nodes x1 -> x2 -> ... -> xk such that there is
a directed edge from xi to xi+1 for every 1 <= i < k. The color value of the
path is the number of nodes that are colored the most frequently occurring
color along that path.

Return the largest color value of any valid path in the given graph, or -1 if
the graph contains a cycle.

Example 1:
    Input: colors = "abaca", edges = [[0,1],[0,2],[2,3],[3,4]]
    Output: 3
    Explanation: path 0 -> 2 -> 3 -> 4 has three 'a' nodes.
Example 2:
    Input: colors = "a", edges = [[0,0]]
    Output: -1

Constraints:
    n == colors.length
    m == edges.length
    1 <= n <= 10^5
    0 <= m <= 10^5
    colors consists of lowercase English letters.
    0 <= aj, bj < n

Approach (Kahn's topological sort + DP over 26 colors):
    Let dp[v][c] be the max number of nodes of color c on any path ending at v.
    Process nodes in topological order: when popping u, increment dp[u][color[u]],
    update the answer, and for each edge u->v set dp[v][c] = max(dp[v][c], dp[u][c])
    for all c. If fewer than n nodes are processed, a cycle exists -> -1.

Complexity:
    Time:  O(26 * (n + m))
    Space: O(26 * n + m)

Alternative: DFS with memoization and 3-state cycle detection.
"""
import sys
from collections import deque
from typing import List


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        n = len(colors)
        adj = [[] for _ in range(n)]
        indeg = [0] * n
        for a, b in edges:
            adj[a].append(b)
            indeg[b] += 1
        dp = [[0] * 26 for _ in range(n)]
        q = deque(i for i in range(n) if indeg[i] == 0)
        seen = best = 0
        while q:
            u = q.popleft()
            seen += 1
            dp[u][ord(colors[u]) - 97] += 1
            best = max(best, max(dp[u]))
            for v in adj[u]:
                dv, du = dp[v], dp[u]
                for c in range(26):
                    if du[c] > dv[c]:
                        dv[c] = du[c]
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return best if seen == n else -1

    def largestPathValueDFS(self, colors: str, edges: List[List[int]]) -> int:
        sys.setrecursionlimit(10000)
        n = len(colors)
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
        state = [0] * n  # 0 unvisited, 1 visiting, 2 done
        memo = [None] * n
        cyc = [False]

        def dfs(u: int) -> List[int]:
            if state[u] == 2:
                return memo[u]
            if state[u] == 1:
                cyc[0] = True
                return [0] * 26
            state[u] = 1
            cnt = [0] * 26
            for v in adj[u]:
                r = dfs(v)
                if cyc[0]:
                    return cnt
                for c in range(26):
                    cnt[c] = max(cnt[c], r[c])
            cnt[ord(colors[u]) - 97] += 1
            state[u] = 2
            memo[u] = cnt
            return cnt

        best = 0
        for i in range(n):
            best = max(best, max(dfs(i)))
            if cyc[0]:
                return -1
        return best


if __name__ == "__main__":
    s = Solution()
    for f in (s.largestPathValue, s.largestPathValueDFS):
        assert f("abaca", [[0,1],[0,2],[2,3],[3,4]]) == 3
        assert f("a", [[0,0]]) == -1
        assert f("a", []) == 1
        assert f("ab", []) == 1
        assert f("aab", [[0,1],[1,2]]) == 2
        assert f("abc", [[0,1],[1,2],[2,0]]) == -1
        assert f("aaa", [[0,1],[1,2]]) == 3
        assert f("abab", [[0,1],[2,3]]) == 1
    print("All tests passed")
