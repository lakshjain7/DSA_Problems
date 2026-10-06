"""
106. Construct Binary Tree from Inorder and Postorder Traversal
Difficulty: Medium
Topics: Array, Hash Table, Divide and Conquer, Tree, Binary Tree

Given two integer arrays inorder and postorder where inorder is the inorder
traversal of a binary tree and postorder is the postorder traversal of the
same tree, construct and return the binary tree.

Example 1:
    Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
    Output: [3,9,20,null,null,15,7]
Example 2:
    Input: inorder = [-1], postorder = [-1]
    Output: [-1]

Constraints:
    1 <= inorder.length <= 3000
    postorder.length == inorder.length
    -3000 <= inorder[i], postorder[i] <= 3000
    inorder and postorder consist of unique values.
    Each value of postorder also appears in inorder.

Approach:
    The last element of postorder is the root. Its position in inorder splits
    the remaining values into left and right subtrees. Consuming postorder from
    the END yields root, then right subtree, then left subtree, so build the
    right subtree first. A value->index map makes each split O(1).

Complexity:
    Time: O(n)   Space: O(n)
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def buildTree(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    idx = {v: i for i, v in enumerate(inorder)}
    pos = len(postorder) - 1

    def build(lo: int, hi: int) -> Optional[TreeNode]:
        nonlocal pos
        if lo > hi:
            return None
        val = postorder[pos]
        pos -= 1
        node = TreeNode(val)
        m = idx[val]
        node.right = build(m + 1, hi)
        node.left = build(lo, m - 1)
        return node

    return build(0, len(inorder) - 1)


# Alternative: slicing-based recursion (simpler, O(n^2) worst case).
def buildTreeSlicing(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    if not inorder:
        return None
    root = TreeNode(postorder[-1])
    m = inorder.index(postorder[-1])
    root.left = buildTreeSlicing(inorder[:m], postorder[:m])
    root.right = buildTreeSlicing(inorder[m + 1:], postorder[m:-1])
    return root


def _in(n):
    return _in(n.left) + [n.val] + _in(n.right) if n else []


def _post(n):
    return _post(n.left) + _post(n.right) + [n.val] if n else []


if __name__ == "__main__":
    cases = [
        ([9, 3, 15, 20, 7], [9, 15, 7, 20, 3]),
        ([-1], [-1]),
        ([1, 2, 3], [3, 2, 1]),   # right-skewed
        ([3, 2, 1], [3, 2, 1]),   # left-skewed
        ([2, 1, 3], [2, 3, 1]),
    ]
    for f in (buildTree, buildTreeSlicing):
        for i, p in cases:
            t = f(i, p)
            assert _in(t) == i and _post(t) == p
    t = buildTree([9, 3, 15, 20, 7], [9, 15, 7, 20, 3])
    assert t.val == 3 and t.left.val == 9 and t.right.val == 20
    assert t.right.left.val == 15 and t.right.right.val == 7
    print("All tests passed.")
