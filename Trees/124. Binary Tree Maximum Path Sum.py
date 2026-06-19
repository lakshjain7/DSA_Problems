"""
Problem Number: 124
Title: Binary Tree Maximum Path Sum
Difficulty: Hard
Topics: Tree, Depth-First Search, Dynamic Programming, Binary Tree

Problem Statement:
------------------
A path in a binary tree is a sequence of nodes where each pair of adjacent
nodes in the sequence has an edge connecting them. A node can only appear
in the sequence at most once. Note that the path does not need to pass
through the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any
non-empty path.

Examples:
---------
Input: root = [1, 2, 3]
Output: 6
Explanation: The optimal path is 2 -> 1 -> 3 with path sum 2 + 1 + 3 = 6.

Input: root = [-10, 9, 20, null, null, 15, 7]
Output: 42
Explanation: The optimal path is 15 -> 20 -> 7 with path sum 15 + 20 + 7 = 42.

Constraints:
------------
- The number of nodes in the tree is in the range [1, 3 * 10^4].
- -1000 <= Node.val <= 1000

Approach:
---------
Post-order DFS with a global maximum tracker.

For every node, we compute the best "gain" we can get if we enter this
node from its parent. That gain is:
    node.val + max(0, left_gain) + max(0, right_gain)  — if we use BOTH
    sides this forms a complete path through the node.

However, we can only pass ONE side up to the parent (a path cannot split).
So the return value to the parent is:
    node.val + max(0, left_gain, right_gain)

At each node we update the global best with the "split" value (both sides).

Why we clamp to 0:
If a subtree produces negative gain, we simply don't include it (it's
always better to ignore a negative-sum branch).

Complexity Analysis:
--------------------
Time  : O(n) — every node is visited exactly once
Space : O(h) — recursion stack where h is the tree height
"""

from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root: Optional[TreeNode]) -> int:
    global_max = [float("-inf")]

    def dfs(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        left_gain = max(0, dfs(node.left))
        right_gain = max(0, dfs(node.right))
        path_through = node.val + left_gain + right_gain
        global_max[0] = max(global_max[0], path_through)
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return global_max[0]


def build_tree(values: list) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    assert maxPathSum(build_tree([1, 2, 3])) == 6
    assert maxPathSum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42
    assert maxPathSum(TreeNode(5)) == 5
    assert maxPathSum(build_tree([-3, -2, -1])) == -1
    t = TreeNode(1)
    t.left = TreeNode(10)
    t.right = TreeNode(-5)
    assert maxPathSum(t) == 11
    t2 = TreeNode(7)
    t2.left = TreeNode(-3)
    t2.right = TreeNode(-2)
    assert maxPathSum(t2) == 7
    t3 = build_tree([1, 2, 3, 4, 5])
    assert maxPathSum(t3) == 11
    chain = TreeNode(1)
    chain.right = TreeNode(2)
    chain.right.right = TreeNode(3)
    assert maxPathSum(chain) == 6
    print("All tests passed!")
