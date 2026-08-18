"""
114. Flatten Binary Tree to Linked List
Difficulty: Medium
Topics: Linked List, Stack, Tree, Depth-First Search, Binary Tree

Problem Statement
-----------------
Given the root of a binary tree, flatten the tree into a "linked list":
- The "linked list" should use the same TreeNode class where the right child
  pointer points to the next node in the list and the left child pointer is
  always null.
- The "linked list" should be in the same order as a pre-order traversal of the
  binary tree.

Example 1:
    Input:  root = [1,2,5,3,4,null,6]
    Output: [1,null,2,null,3,null,4,null,5,null,6]

Example 2:
    Input:  root = []
    Output: []

Example 3:
    Input:  root = [0]
    Output: [0]

Constraints:
    - The number of nodes in the tree is in the range [0, 2000].
    - -100 <= Node.val <= 100

Follow up: Can you flatten the tree in-place (with O(1) extra space)?

Approach (Morris-style / reverse pre-order, O(1) space)
-------------------------------------------------------
Pre-order visits node, then left subtree, then right subtree. When we flatten a
node we want: node.right = (flattened left subtree), and the flattened left
subtree's tail should connect to the original right subtree.

The elegant O(1) trick: for each node, if it has a left child, find the
rightmost node (the predecessor) of that left subtree. Rewire that predecessor's
right pointer to the node's current right subtree, then move the whole left
subtree to the right and null out left. Advance to node.right and repeat.

Why it works: the rightmost node of the left subtree is exactly the last node
visited in a pre-order traversal of that left subtree, so attaching the original
right subtree there preserves pre-order order.

Complexity
----------
Time:  O(n). Each edge is traversed a constant number of times; finding
       predecessors totals O(n) across the whole tree.
Space: O(1) extra (in-place), ignoring the recursion-free iteration.
"""

from __future__ import annotations

from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional["TreeNode"] = None,
                 right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """Flatten the tree in-place to a right-leaning linked list. O(1) space."""
        curr = root
        while curr:
            if curr.left:
                # Find the rightmost node of the left subtree (pre-order predecessor).
                predecessor = curr.left
                while predecessor.right:
                    predecessor = predecessor.right
                # Rewire: attach current right subtree after that predecessor.
                predecessor.right = curr.right
                # Move left subtree to the right, clear left.
                curr.right = curr.left
                curr.left = None
            curr = curr.right


class SolutionRecursive:
    """Alternative: reverse pre-order (right, left, node) with a running tail."""

    def flatten(self, root: Optional[TreeNode]) -> None:
        self._prev: Optional[TreeNode] = None

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.right)
            dfs(node.left)
            node.right = self._prev
            node.left = None
            self._prev = node

        dfs(root)


# ----------------------------- Test helpers ----------------------------------
def build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a binary tree from level-order list with None for missing nodes."""
    if not values:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    queue = [root]
    while queue:
        node = queue.pop(0)
        try:
            left_val = next(it)
        except StopIteration:
            break
        if left_val is not None:
            node.left = TreeNode(left_val)
            queue.append(node.left)
        try:
            right_val = next(it)
        except StopIteration:
            break
        if right_val is not None:
            node.right = TreeNode(right_val)
            queue.append(node.right)
    return root


def to_flat_list(root: Optional[TreeNode]) -> List[int]:
    """Read the flattened right-chain into a list, asserting no left children."""
    out: List[int] = []
    node = root
    while node:
        assert node.left is None, "Flattened list must have no left children"
        out.append(node.val)
        node = node.right
    return out


if __name__ == "__main__":
    for SolClass in (Solution, SolutionRecursive):
        sol = SolClass()

        # Example 1
        t1 = build_tree([1, 2, 5, 3, 4, None, 6])
        sol.flatten(t1)
        assert to_flat_list(t1) == [1, 2, 3, 4, 5, 6], SolClass.__name__

        # Example 2: empty tree
        t2 = build_tree([])
        sol.flatten(t2)
        assert to_flat_list(t2) == [], SolClass.__name__

        # Example 3: single node
        t3 = build_tree([0])
        sol.flatten(t3)
        assert to_flat_list(t3) == [0], SolClass.__name__

        # Left-skewed tree
        t4 = build_tree([1, 2, None, 3])
        sol.flatten(t4)
        assert to_flat_list(t4) == [1, 2, 3], SolClass.__name__

        # Right-skewed tree stays the same order
        t5 = build_tree([1, None, 2, None, 3])
        sol.flatten(t5)
        assert to_flat_list(t5) == [1, 2, 3], SolClass.__name__

        # Larger balanced tree, verify against pre-order
        t6 = build_tree([1, 2, 3, 4, 5, 6, 7])
        sol.flatten(t6)
        assert to_flat_list(t6) == [1, 2, 4, 5, 3, 6, 7], SolClass.__name__

    print("All tests passed for 114. Flatten Binary Tree to Linked List")
