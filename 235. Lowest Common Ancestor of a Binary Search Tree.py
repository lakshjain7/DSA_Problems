"""
Problem Number: 235
Title: Lowest Common Ancestor of a Binary Search Tree
Difficulty: Medium
Topics: Tree, Binary Search Tree, Depth-First Search, Binary Tree

Problem Statement:
    Given a binary search tree (BST), find the lowest common ancestor (LCA) node
    of two given nodes in the BST.

    The lowest common ancestor is defined between two nodes p and q as the lowest
    node in T that has both p and q as descendants (where we allow a node to be a
    descendant of itself).

Examples:
    Example 1:
        Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
        Output: 6
        Explanation: The LCA of nodes 2 and 8 is 6.

    Example 2:
        Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
        Output: 2
        Explanation: The LCA of nodes 2 and 4 is 2, since a node can be a
        descendant of itself.

    Example 3:
        Input: root = [2,1], p = 2, q = 1
        Output: 2

Constraints:
    - The number of nodes in the tree is in the range [2, 10^5].
    - -10^9 <= Node.val <= 10^9
    - All Node.val are unique.
    - p != q
    - p and q will exist in the BST.

Approach (BST Property Exploit):
    In a BST:
    - All values in the left subtree are LESS than the current node's value.
    - All values in the right subtree are GREATER than the current node's value.

    Starting at root, at each step:
    - If BOTH p and q are less than current node -> LCA is in the left subtree.
    - If BOTH p and q are greater than current node -> LCA is in the right subtree.
    - Otherwise (one is <= current and the other is >= current, or one equals current)
      -> current node IS the LCA (the paths to p and q diverge here).

    This is O(h) time where h is the height of the BST, and O(1) space with the
    iterative approach.

    Note: This is FASTER than the general binary tree LCA (LC 236) which is O(n)
    because that problem cannot exploit BST ordering.

Complexity:
    Time:  O(h) -- h is tree height; O(log n) for balanced BST, O(n) worst case
    Space: O(1) -- iterative solution uses no extra space
           O(h) -- recursive solution uses call stack

Alternative Approach (Recursive):
    Same logic but expressed recursively. Slightly more elegant but uses O(h) stack
    space. Both approaches are shown below.
"""

from __future__ import annotations
from typing import Optional


class TreeNode:
    """Standard binary tree node."""
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


# ---------------------------------------------------------------------------
# Solution 1: Iterative -- O(h) time, O(1) space
# ---------------------------------------------------------------------------

def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Find the LCA of p and q in the given BST iteratively.

    Args:
        root: Root of the BST.
        p:    First target node.
        q:    Second target node.

    Returns:
        The lowest common ancestor node.
    """
    node = root

    while node:
        if p.val < node.val and q.val < node.val:
            # Both targets are in the left subtree
            node = node.left
        elif p.val > node.val and q.val > node.val:
            # Both targets are in the right subtree
            node = node.right
        else:
            # Current node is the split point -- it's the LCA
            return node

    # Should never reach here given valid BST and existing p, q
    raise ValueError("LCA not found -- check that p and q exist in the BST")


# ---------------------------------------------------------------------------
# Solution 2: Recursive -- O(h) time, O(h) space
# ---------------------------------------------------------------------------

def lowestCommonAncestor_recursive(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """Same logic expressed recursively."""
    if p.val < root.val and q.val < root.val:
        return lowestCommonAncestor_recursive(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowestCommonAncestor_recursive(root.right, p, q)
    return root


# ---------------------------------------------------------------------------
# Helpers for tests
# ---------------------------------------------------------------------------

def build_bst(values: list[Optional[int]]) -> Optional[TreeNode]:
    """Build a BST from a level-order list (None = missing node)."""
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


def find_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Find a node by value in a BST."""
    while root:
        if val == root.val:
            return root
        elif val < root.val:
            root = root.left
        else:
            root = root.right
    return None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Build the BST from Example 1 & 2: [6,2,8,0,4,7,9,null,null,3,5]
    #         6
    #        / \
    #       2   8
    #      / \ / \
    #     0  4 7  9
    #       / \
    #      3   5
    root = build_bst([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])

    p = find_node(root, 2)
    q = find_node(root, 8)
    assert lowestCommonAncestor(root, p, q).val == 6, "Expected 6"
    assert lowestCommonAncestor_recursive(root, p, q).val == 6, "Expected 6"

    # Example 2: LCA of 2 and 4 is 2 (node can be ancestor of itself)
    p = find_node(root, 2)
    q = find_node(root, 4)
    assert lowestCommonAncestor(root, p, q).val == 2, "Expected 2"
    assert lowestCommonAncestor_recursive(root, p, q).val == 2, "Expected 2"

    # LCA of 0 and 5: they share 2 as split point
    p = find_node(root, 0)
    q = find_node(root, 5)
    assert lowestCommonAncestor(root, p, q).val == 2, "Expected 2"

    # LCA of 7 and 9: they share 8
    p = find_node(root, 7)
    q = find_node(root, 9)
    assert lowestCommonAncestor(root, p, q).val == 8, "Expected 8"

    # LCA of 3 and 9: diverge at root (6)
    p = find_node(root, 3)
    q = find_node(root, 9)
    assert lowestCommonAncestor(root, p, q).val == 6, "Expected 6"

    # Example 3: [2,1], LCA of 2 and 1 is 2
    root2 = build_bst([2, 1])
    p = find_node(root2, 2)
    q = find_node(root2, 1)
    assert lowestCommonAncestor(root2, p, q).val == 2, "Expected 2"
    assert lowestCommonAncestor_recursive(root2, p, q).val == 2, "Expected 2"

    # Single-depth tree
    root3 = build_bst([5, 3, 7])
    p = find_node(root3, 3)
    q = find_node(root3, 7)
    assert lowestCommonAncestor(root3, p, q).val == 5, "Expected 5"

    print("All tests passed for 235. Lowest Common Ancestor of a Binary Search Tree!")
