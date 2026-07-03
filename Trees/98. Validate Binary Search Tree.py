"""
98. Validate Binary Search Tree
Difficulty: Medium
Topics: Trees, Binary Search Tree, DFS, Recursion

Problem Statement:
Given the root of a binary tree, determine if it is a valid binary search
tree (BST).

A valid BST is defined as follows:
    - The left subtree of a node contains only nodes with keys strictly
      less than the node's key.
    - The right subtree of a node contains only nodes with keys strictly
      greater than the node's key.
    - Both the left and right subtrees must also be binary search trees.

Examples:
    Input: root = [2,1,3]
    Output: true

    Input: root = [5,1,4,null,null,3,6]
    Output: false
    Explanation: The root node's value is 5 but its right child's value is
    4, and the right subtree of 5's right child (3) is less than 5.

Constraints:
    The number of nodes in the tree is in the range [1, 10^4].
    -2^31 <= Node.val <= 2^31 - 1

Approach (DFS with valid range bounds):
A naive check that only compares each node to its immediate children is
insufficient: a node deep in the right subtree could violate the BST
property with an ancestor several levels up (e.g. example 2 above). The
key insight is that every node must fall within a valid (low, high) open
interval determined by its ancestors: going left tightens the upper bound
to the parent's value, going right tightens the lower bound to the
parent's value. We do a DFS/pre-order traversal carrying these bounds
down; if any node's value falls outside its allowed range, the tree is
invalid. Start the root with bounds (-infinity, +infinity).

Complexity Analysis:
    Time:  O(n) - every node is visited exactly once.
    Space: O(h) - recursion stack depth equals tree height h,
           O(log n) for a balanced tree, O(n) worst case for a skewed tree.

Alternative Approach (Inorder traversal must be strictly increasing):
An inorder traversal of a valid BST visits nodes in strictly increasing
order. So we can do an iterative or recursive inorder traversal and check
that each visited value is strictly greater than the previously visited
value. This also runs in O(n) time and O(h) space and avoids passing
bounds explicitly, tracking only the previous value instead.
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Build a binary tree from a level-order list with None for missing nodes."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values):
            if values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    def validate(node: Optional[TreeNode], low: float, high: float) -> bool:
        if node is None:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)

    return validate(root, float("-inf"), float("inf"))


def is_valid_bst_inorder(root: Optional[TreeNode]) -> bool:
    """Alternative approach: inorder traversal must be strictly increasing."""
    prev = None
    stack = []
    node = root

    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None and node.val <= prev:
            return False
        prev = node.val
        node = node.right

    return True


if __name__ == "__main__":
    assert is_valid_bst(build_tree([2, 1, 3])) is True
    assert is_valid_bst(build_tree([5, 1, 4, None, None, 3, 6])) is False
    assert is_valid_bst(build_tree([1])) is True
    assert is_valid_bst(build_tree([1, 1])) is False
    assert is_valid_bst(build_tree([2, 2, 2])) is False
    assert is_valid_bst(build_tree([10, 5, 15, None, None, 6, 20])) is False
    assert is_valid_bst(build_tree([5, 4, 6, None, None, 3, 7])) is False
    # Large value edge case guards against int overflow tricks in other languages
    assert is_valid_bst(build_tree([2147483647])) is True
    assert is_valid_bst(build_tree([0, None, -1])) is False

    assert is_valid_bst_inorder(build_tree([2, 1, 3])) is True
    assert is_valid_bst_inorder(build_tree([5, 1, 4, None, None, 3, 6])) is False
    assert is_valid_bst_inorder(build_tree([10, 5, 15, None, None, 6, 20])) is False

    print("All tests passed for 98. Validate Binary Search Tree")
