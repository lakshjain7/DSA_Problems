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
    Example 1: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8 -> Output: 6
    Example 2: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4 -> Output: 2
    Example 3: root = [2,1], p = 2, q = 1 -> Output: 2

Approach (BST Property):
    If BOTH p and q < current node -> go left.
    If BOTH p and q > current node -> go right.
    Otherwise -> current node IS the LCA.

Complexity:
    Time:  O(h) -- O(log n) balanced, O(n) worst case
    Space: O(1) iterative / O(h) recursive
"""

from __future__ import annotations
from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    node = root
    while node:
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node
    raise ValueError("LCA not found")


def lowestCommonAncestor_recursive(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    if p.val < root.val and q.val < root.val:
        return lowestCommonAncestor_recursive(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowestCommonAncestor_recursive(root.right, p, q)
    return root


def build_bst(values):
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


def find_node(root, val):
    while root:
        if val == root.val:
            return root
        root = root.left if val < root.val else root.right
    return None


if __name__ == "__main__":
    root = build_bst([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    assert lowestCommonAncestor(root, find_node(root, 2), find_node(root, 8)).val == 6
    assert lowestCommonAncestor(root, find_node(root, 2), find_node(root, 4)).val == 2
    assert lowestCommonAncestor(root, find_node(root, 0), find_node(root, 5)).val == 2
    assert lowestCommonAncestor(root, find_node(root, 7), find_node(root, 9)).val == 8
    root2 = build_bst([2, 1])
    assert lowestCommonAncestor(root2, find_node(root2, 2), find_node(root2, 1)).val == 2
    print("All tests passed for 235. Lowest Common Ancestor of a Binary Search Tree!")
