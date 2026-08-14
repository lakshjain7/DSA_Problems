"""
LeetCode 399. Evaluate Division
Difficulty: Medium
Topics: Graph, DFS, BFS, Union-Find, Shortest Path

Problem Statement:
    You are given an array of variable pairs equations and an array of real
    numbers values, where equations[i] = [A_i, B_i] and values[i] represent
    the equation A_i / B_i = values[i]. Each A_i or B_i is a string that
    represents a single variable.

    You are also given some queries, where queries[j] = [C_j, D_j] represents
    the j-th query where you must find the answer for C_j / D_j = ?.

    Return the answers to all queries. If a single answer cannot be
    determined, return -1.0.

    Note: The input is always valid. You may assume that evaluating the queries
    will not result in division by zero and that there is no contradiction.

    Note: The variables that do not occur in the list of equations are
    undefined, so the answer cannot be determined for them.

Examples:
    Example 1:
        Input:  equations = [["a","b"],["b","c"]], values = [2.0,3.0],
                queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
        Output: [6.0, 0.5, -1.0, 1.0, -1.0]
        Explanation:
            a/b = 2.0, b/c = 3.0
            a/c = (a/b)*(b/c) = 6.0
            b/a = 1/(a/b) = 0.5
            a/e -> e undefined -> -1.0
            a/a = 1.0
            x/x -> x undefined -> -1.0

    Example 2:
        Input:  equations = [["a","b"],["b","c"],["bc","cd"]],
                values = [1.5,2.5,5.0],
                queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
        Output: [3.75, 0.4, 5.0, 0.2]

    Example 3:
        Input:  equations = [["a","b"]], values = [0.5],
                queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
        Output: [0.5, 2.0, -1.0, -1.0]

Constraints:
    - 1 <= equations.length <= 20
    - equations[i].length == 2
    - 1 <= A_i.length, B_i.length <= 5
    - values.length == equations.length
    - 0.0 < values[i] <= 20.0
    - 1 <= queries.length <= 20
    - queries[i].length == 2
    - 1 <= C_j.length, D_j.length <= 5
    - A_i, B_i, C_j, D_j consist of lower case English letters and digits.

Approach (weighted graph + DFS):
    Model each variable as a node. Each equation A / B = v gives a directed
    edge A -> B with weight v and its inverse edge B -> A with weight 1/v.
    A query C / D then asks: is there a path from C to D, and if so what is the
    product of edge weights along it? That product equals C / D because the
    intermediate variables telescope:
        (C/X1) * (X1/X2) * ... * (Xk/D) = C / D.

    For each query:
        - If C or D is not a known node, the answer is -1.0 (undefined).
        - If C == D and C is known, the answer is 1.0.
        - Otherwise run DFS from C, multiplying weights, until we reach D.
          If D is unreachable, return -1.0.

Why it works:
    The graph is consistent (the problem guarantees no contradictions), so any
    path between two nodes yields the same product. Multiplying edge weights
    accumulates the ratio, and the inverse edges let us traverse in either
    direction.

Complexity:
    Let V be the number of distinct variables and Q the number of queries.
    Building the graph: O(E) where E = number of equations.
    Each query DFS visits each node/edge at most once: O(V + E).
    Time:  O(Q * (V + E)).
    Space: O(V + E) for the adjacency graph plus O(V) recursion/visited.
"""

from typing import List, Dict
from collections import defaultdict


class Solution:
    def calcEquation(
        self,
        equations: List[List[str]],
        values: List[float],
        queries: List[List[str]],
    ) -> List[float]:
        # graph[u][v] = u / v
        graph: Dict[str, Dict[str, float]] = defaultdict(dict)
        for (a, b), v in zip(equations, values):
            graph[a][b] = v
            graph[b][a] = 1.0 / v

        def dfs(src: str, dst: str, visited: set) -> float:
            if src == dst:
                return 1.0
            visited.add(src)
            for neighbor, weight in graph[src].items():
                if neighbor in visited:
                    continue
                sub = dfs(neighbor, dst, visited)
                if sub != -1.0:
                    return weight * sub
            return -1.0

        results: List[float] = []
        for c, d in queries:
            if c not in graph or d not in graph:
                results.append(-1.0)
            else:
                results.append(dfs(c, d, set()))
        return results

    # Alternative approach: Union-Find with ratio-to-parent.
    # Each node stores its value relative to its set representative. Union of
    # a/b = v links the two roots and rescales weights so ratios stay
    # consistent. A query is answerable iff both variables share a root, and the
    # answer is weight[c] / weight[d].
    def calcEquationUnionFind(
        self,
        equations: List[List[str]],
        values: List[float],
        queries: List[List[str]],
    ) -> List[float]:
        parent: Dict[str, str] = {}
        weight: Dict[str, float] = {}  # weight[x] = x / parent[x]

        def find(x: str):
            if parent[x] != x:
                root, w = find(parent[x])
                parent[x] = root
                weight[x] *= w
            return parent[x], weight[x]

        def add(x: str) -> None:
            if x not in parent:
                parent[x] = x
                weight[x] = 1.0

        for (a, b), v in zip(equations, values):
            add(a)
            add(b)
            ra, wa = find(a)
            rb, wb = find(b)
            if ra != rb:
                # a/b = v, weight[a] = a/ra, weight[b] = b/rb.
                # Attach ra under rb: ra/rb = (b/a) * (a/ra)^-1 ... solve:
                # a = wa*ra, b = wb*rb, a/b = v => wa*ra / (wb*rb) = v
                # => ra/rb = v * wb / wa
                parent[ra] = rb
                weight[ra] = v * wb / wa

        results: List[float] = []
        for c, d in queries:
            if c not in parent or d not in parent:
                results.append(-1.0)
                continue
            rc, wc = find(c)
            rd, wd = find(d)
            if rc != rd:
                results.append(-1.0)
            else:
                results.append(wc / wd)
        return results


def _almost_equal(a: List[float], b: List[float], tol: float = 1e-6) -> bool:
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


if __name__ == "__main__":
    sol = Solution()

    for solver in (sol.calcEquation, sol.calcEquationUnionFind):
        # Example 1
        assert _almost_equal(
            solver(
                [["a", "b"], ["b", "c"]],
                [2.0, 3.0],
                [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]],
            ),
            [6.0, 0.5, -1.0, 1.0, -1.0],
        )

        # Example 2
        assert _almost_equal(
            solver(
                [["a", "b"], ["b", "c"], ["bc", "cd"]],
                [1.5, 2.5, 5.0],
                [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]],
            ),
            [3.75, 0.4, 5.0, 0.2],
        )

        # Example 3
        assert _almost_equal(
            solver(
                [["a", "b"]],
                [0.5],
                [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]],
            ),
            [0.5, 2.0, -1.0, -1.0],
        )

        # Single equation, self-division of a known var
        assert _almost_equal(solver([["x", "y"]], [4.0], [["x", "x"]]), [1.0])

        # Disconnected components: a/b known, c/d known, cross query undefined
        assert _almost_equal(
            solver(
                [["a", "b"], ["c", "d"]],
                [2.0, 3.0],
                [["a", "b"], ["c", "d"], ["a", "c"], ["b", "d"]],
            ),
            [2.0, 3.0, -1.0, -1.0],
        )

    print("All tests passed for 399. Evaluate Division")
