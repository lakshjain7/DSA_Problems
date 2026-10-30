"""
538. Convert BST to Greater Tree
Difficulty: Medium
Topics: Tree, Depth-First Search, Binary Search Tree, Binary Tree

Problem:
    Given the root of a Binary Search Tree (BST), convert it to a Greater Tree
    such that every key of the original BST is changed to the original key plus
    the sum of all keys greater than the original key in the BST.

Examples:
    Input: root = [4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
    Output: [30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
    Input: root = [0,null,1]
    Output: [1,null,1]

Constraints:
    The number of nodes is in [0, 10^4].
    -10^4 <= Node.val <= 10^4; all values are unique; root is a valid BST.

Approach:
    In-order traversal of a BST visits keys ascending, so a reverse in-order
    (right, node, left) visits them descending. Keep a running sum of visited
    values; at each node add the running sum to its value and update the sum.

Complexity:
    Time O(n). Space O(h) recursion (O(1) extra for Morris).
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def convertBST(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Iterative reverse in-order with explicit stack."""
    total = 0
    stack: List[TreeNode] = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.right
        node = stack.pop()
        total += node.val
        node.val = total
        node = node.left
    return root


def convertBST_morris(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Alternative: reverse Morris traversal, O(1) extra space."""
    total = 0
    node = root
    while node:
        if not node.right:
            total += node.val
            node.val = total
            node = node.left
        else:
            succ = node.right
            while succ.left and succ.left is not node:
                succ = succ.left
            if not succ.left:
                succ.left = node
                node = node.right
            else:
                succ.left = None
                total += node.val
                node.val = total
                node = node.left
    return root


def build(vals: list) -> Optional[TreeNode]:
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = [root]
    i = 1
    for n in q:
        if i < len(vals):
            if vals[i] is not None:
                n.left = TreeNode(vals[i]); q.append(n.left)
            i += 1
        if i < len(vals):
            if vals[i] is not None:
                n.right = TreeNode(vals[i]); q.append(n.right)
            i += 1
    return root


def serialize(root: Optional[TreeNode]) -> list:
    if not root:
        return []
    out, q = [], [root]
    for n in q:
        if n is None:
            out.append(None)
        else:
            out.append(n.val); q.append(n.left); q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    big = [4, 1, 6, 0, 2, 5, 7, None, None, None, 3, None, None, None, 8]
    exp = [30, 36, 21, 36, 35, 26, 15, None, None, None, 33, None, None, None, 8]
    for f in (convertBST, convertBST_morris):
        assert serialize(f(build(big))) == exp
        assert serialize(f(build([0, None, 1]))) == [1, None, 1]
        assert f(None) is None
        assert serialize(f(build([5]))) == [5]
        assert serialize(f(build([2, 1, 3]))) == [5, 6, 3]
        assert serialize(f(build([-1, -2, None]))) == [-1, -3]
    print("All tests passed.")
