"""
96. Unique Binary Search Trees
Difficulty: Medium
Topics: Math, Dynamic Programming, Tree, Binary Search Tree, Binary Tree

Problem:
Given an integer n, return the number of structurally unique BSTs (binary
search trees) which have exactly n nodes of unique values from 1 to n.

Example 1:
    Input: n = 3
    Output: 5
Example 2:
    Input: n = 1
    Output: 1

Constraints:
    1 <= n <= 19

Approach (DP / Catalan numbers):
Let G[n] be the count of BSTs with n nodes. Choose root i (1..n): the left
subtree uses i-1 nodes and the right uses n-i nodes, and they are independent,
so G[n] = sum_{i=1..n} G[i-1] * G[n-i], with G[0] = G[1] = 1. Only the number
of nodes matters, not the actual values, because any sorted range of k values
forms the same set of shapes.

Complexity: Time O(n^2), Space O(n).

Alternative: closed form Catalan number C(n) = C(2n, n) / (n + 1), O(n) time.
"""
from math import comb


def num_trees(n: int) -> int:
    G = [0] * (n + 2)
    G[0] = G[1] = 1
    for nodes in range(2, n + 1):
        for root in range(1, nodes + 1):
            G[nodes] += G[root - 1] * G[nodes - root]
    return G[n]


def num_trees_catalan(n: int) -> int:
    return comb(2 * n, n) // (n + 1)


if __name__ == "__main__":
    for f in (num_trees, num_trees_catalan):
        assert f(1) == 1
        assert f(2) == 2
        assert f(3) == 5
        assert f(4) == 14
        assert f(5) == 42
        assert f(19) == 1767263190
    for n in range(1, 20):
        assert num_trees(n) == num_trees_catalan(n)
    print("All tests passed.")
