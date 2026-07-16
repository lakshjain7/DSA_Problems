"""
1448. Count Good Nodes in Binary Tree
Difficulty: Medium
Topics: Tree, Depth-First Search, Binary Tree

Problem Statement:
Given a binary tree `root`, a node X in the tree is named *good* if in
the path from root to X there are no nodes with a value greater than X.
Return the number of good nodes in the binary tree.

Example 1:
    Input:  root = [3, 1, 4, 3, null, 1, 5]
    Output: 4
    Explanation: Nodes in blue are good.
        Root Node (3) is always a good node.
        Node 4 -> (3, 4) is the maximum value in the path starting from
                  the root.
        Node 5 -> (3, 4, 5) is the maximum value in the path.
        Node 3 -> (3, 1, 3) is the maximum value in the path.

Example 2:
    Input:  root = [3, 3, null, 4, 2]
    Output: 3
    Explanation: Node 2 -> (3, 3, 2) is not good, because "3" is higher
                 than it.

Example 3:
    Input:  root = [1]
    Output: 1
    Explanation: Root is considered as good.

Constraints:
    The number of nodes in the binary tree is in the range [1, 10^5].
    Each node's value is between [-10^4, 10^4].

------------------------------------------------------------------------
Approach: DFS carrying the running maximum along the path
------------------------------------------------------------------------
A node is "good" exactly when its value is >= the maximum value seen on
the path from the root down to (and including) its parent. So we walk
the tree depth-first, threading along `path_max`, the largest value
encountered so far on the current root-to-node path.

At each node:
    - It is good iff node.val >= path_max.
    - The maximum passed to its children becomes max(path_max, node.val).

The root is always good because it is compared against itself
(path_max initialized to -infinity, or to root.val).

Why it works: "no node greater than X on the path" is equivalent to
"X >= max of the path so far". Because the maximum is monotonically
non-decreasing as we descend, a single carried value is enough - we
never need the whole path, just its running max.

Complexity:
    Time:  O(n) - every node visited once.
    Space: O(h) - recursion stack, where h is the tree height
           (O(n) worst case for a skewed tree, O(log n) if balanced).
"""

from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def good_nodes(root: Optional[TreeNode]) -> int:
    """Count good nodes using recursive DFS with a running maximum."""
    def dfs(node: Optional[TreeNode], path_max: int) -> int:
        if node is None:
            return 0
        good = 1 if node.val >= path_max else 0
        new_max = max(path_max, node.val)
        good += dfs(node.left, new_max)
        good += dfs(node.right, new_max)
        return good

    return dfs(root, float("-inf"))


# ------------------------------------------------------------------------
# Alternative approach: iterative DFS with an explicit stack
# ------------------------------------------------------------------------
# Avoids Python's recursion limit for deep/skewed trees (n up to 1e5).
# Each stack entry pairs a node with the running max valid at that node.
def good_nodes_iterative(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    count = 0
    stack = [(root, float("-inf"))]
    while stack:
        node, path_max = stack.pop()
        if node.val >= path_max:
            count += 1
        new_max = max(path_max, node.val)
        if node.left:
            stack.append((node.left, new_max))
        if node.right:
            stack.append((node.right, new_max))
    return count


def build_tree(values: list) -> Optional[TreeNode]:
    """Build a binary tree from a level-order list (LeetCode format)."""
    if not values or values[0] is None:
        return None
    from collections import deque
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    # Example 1
    assert good_nodes(build_tree([3, 1, 4, 3, None, 1, 5])) == 4
    # Example 2
    assert good_nodes(build_tree([3, 3, None, 4, 2])) == 3
    # Example 3 - single node
    assert good_nodes(build_tree([1])) == 1
    # Empty tree
    assert good_nodes(None) == 0
    # Left-skewed strictly increasing -> every node good
    assert good_nodes(build_tree([1, 2, None, 3, None, 4])) == 4
    # Strictly decreasing down a path -> only the root is good
    root = TreeNode(5, TreeNode(4, TreeNode(3, TreeNode(2, TreeNode(1)))))
    assert good_nodes(root) == 1
    # Negative values
    assert good_nodes(build_tree([-1, -2, -3])) == 1
    assert good_nodes(build_tree([-5, -4, -6])) == 2
    # Equal values along the path still count (>= comparison)
    assert good_nodes(build_tree([2, 2, 2])) == 3

    # Cross-check recursive vs iterative on the same inputs.
    for vals in (
        [3, 1, 4, 3, None, 1, 5], [3, 3, None, 4, 2], [1],
        [-1, -2, -3], [2, 2, 2], [1, 2, None, 3, None, 4],
    ):
        t = build_tree(vals)
        assert good_nodes(t) == good_nodes_iterative(t)

    print("All tests passed for 1448. Count Good Nodes in Binary Tree")
