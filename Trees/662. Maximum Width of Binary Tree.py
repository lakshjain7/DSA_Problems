"""
662. Maximum Width of Binary Tree
Difficulty: Medium
Topics: Tree, Depth-First Search, Breadth-First Search, Binary Tree

Problem Statement
-----------------
Given the root of a binary tree, return the maximum width of the given tree.

The maximum width of a tree is the maximum width among all levels.

The width of one level is defined as the length between the end-nodes (the
leftmost and rightmost non-null nodes), where the null nodes between the
end-nodes that would be present in a complete binary tree extending down to
that level are also counted into the length calculation.

It is guaranteed that the answer will in the range of a 32-bit signed integer.

Examples
--------
Example 1:
    Input: root = [1,3,2,5,3,null,9]
    Output: 4
    Explanation: The maximum width exists in the third level with length 4
    (5,3,null,9).

Example 2:
    Input: root = [1,3,2,5,null,null,9,6,null,7]
    Output: 7
    Explanation: The maximum width exists in the fourth level with length 7
    (6,null,null,null,null,null,7).

Example 3:
    Input: root = [1,3,2,5]
    Output: 2
    Explanation: The maximum width exists in the second level with length 2 (3,2).

Constraints
-----------
- The number of nodes in the tree is in the range [1, 3000].
- -100 <= Node.val <= 100

Approach
--------
Assign every node a positional index as if the tree were a complete binary
tree stored in an array: the root gets index 0, and a node with index i has
its left child at 2*i + 1 and its right child at 2*i + 2. The width of a level
is then (index of rightmost node) - (index of leftmost node) + 1.

We do a level-order (BFS) traversal, carrying each node's index alongside it.
For every level, the first node dequeued is the leftmost and the last is the
rightmost, so we can compute that level's width directly. To keep the indices
from overflowing on deep, skewed trees we normalise each level by subtracting
the leftmost index of that level (this keeps values small and does not change
differences). Python integers are unbounded so this is only a hygiene step,
but it matches how the problem must be solved in fixed-width languages.

Why it works
------------
The heap-style indexing exactly reproduces the "null nodes counted as if the
tree were complete" definition of width: two real nodes that are k array slots
apart have exactly k-1 (possibly null) positions between them, so the span
index_right - index_left + 1 is precisely the required width.

Complexity
----------
Time:  O(n) - each node is visited once.
Space: O(n) - the BFS queue holds at most one level of nodes.

Alternative Approach
--------------------
A DFS (preorder) variant records the first index seen at each depth in a
dictionary. When visiting a node at (depth, index), the candidate width is
index - first_index[depth] + 1. Because preorder visits the leftmost node of
each depth first, first_index[depth] is always the leftmost index. This uses
O(h) space for the recursion stack, better than BFS on wide trees.
"""
from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def width_of_binary_tree(root: Optional[TreeNode]) -> int:
    """BFS with heap-style indexing."""
    if not root:
        return 0
    max_width = 0
    queue: deque = deque([(root, 0)])
    while queue:
        level_size = len(queue)
        _, first_index = queue[0]
        index = first_index  # last processed index on this level
        for _ in range(level_size):
            node, index = queue.popleft()
            norm = index - first_index  # normalise to avoid huge numbers
            if node.left:
                queue.append((node.left, 2 * norm + 1))
            if node.right:
                queue.append((node.right, 2 * norm + 2))
        max_width = max(max_width, index - first_index + 1)
    return max_width


def width_of_binary_tree_dfs(root: Optional[TreeNode]) -> int:
    """DFS variant recording the leftmost index per depth."""
    first_index: dict = {}

    def dfs(node: Optional[TreeNode], depth: int, index: int) -> int:
        if not node:
            return 0
        if depth not in first_index:
            first_index[depth] = index
        cur = index - first_index[depth] + 1
        left = dfs(node.left, depth + 1, 2 * index)
        right = dfs(node.right, depth + 1, 2 * index + 1)
        return max(cur, left, right)

    return dfs(root, 0, 0)


def build_tree(values: list) -> Optional[TreeNode]:
    """Build a tree from a LeetCode-style level-order list with None gaps."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
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
    for fn in (width_of_binary_tree, width_of_binary_tree_dfs):
        assert fn(build_tree([1, 3, 2, 5, 3, None, 9])) == 4
        assert fn(build_tree(
            [1, 3, 2, 5, None, None, 9, 6, None, 7])) == 7
        assert fn(build_tree([1, 3, 2, 5])) == 2
        # Single node
        assert fn(build_tree([1])) == 1
        # Empty tree
        assert fn(None) == 0
        # Left-skewed tree: every level width is 1
        assert fn(build_tree([1, 2, None, 3, None, 4])) == 1
        # Full tree of depth 3: bottom level width 4
        assert fn(build_tree([1, 2, 3, 4, 5, 6, 7])) == 4

    # Sparse level with far-apart end nodes, built explicitly.
    # root(idx0) -> left(idx1) -> left(idx3); root -> right(idx2) -> right(idx6)
    # Bottom level spans indices 3..6 => width 6 - 3 + 1 = 4.
    root = TreeNode(1)
    root.left = TreeNode(1)
    root.right = TreeNode(1)
    root.left.left = TreeNode(1)
    root.right.right = TreeNode(1)
    assert width_of_binary_tree(root) == 4
    assert width_of_binary_tree_dfs(root) == 4

    print("All tests passed.")
