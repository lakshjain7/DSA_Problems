"""
Problem 1008: Construct Binary Search Tree from Preorder Traversal
Difficulty: Medium
Topics: Array, Stack, Tree, Binary Search Tree, Binary Tree, Monotonic Stack

Given an array of integers preorder, which represents the preorder traversal
of a BST (i.e., binary search tree), construct the tree and return its root.
It is guaranteed that there is always possible to find a binary search tree
with the given requirements for the given test cases.

Example 1:
    Input: preorder = [8,5,1,7,10,12]
    Output: [8,5,10,1,7,null,12]

Example 2:
    Input: preorder = [1,3]
    Output: [1,null,3]

Constraints:
    1 <= preorder.length <= 100
    1 <= preorder[i] <= 1000
    All values of preorder are unique.

Approach (bounds-based recursion):
    The first element is the root. Walk through the array with a shared index;
    a value may be placed in the current subtree only if it lies inside the
    open interval (lo, hi). Left child gets (lo, val), right child (val, hi).
    Each element is consumed exactly once, so no searching/splitting is needed.

Complexity:
    Time: O(n)   Space: O(h) recursion (O(n) worst case)

Alternative (monotonic stack): keep a stack of the right spine. For a new
value, pop while stack top < value; the last popped (or top) is its parent.
Time O(n), Space O(n).
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def bst_from_preorder(preorder: List[int]) -> Optional[TreeNode]:
    idx = 0
    n = len(preorder)

    def build(lo: float, hi: float) -> Optional[TreeNode]:
        nonlocal idx
        if idx == n or not (lo < preorder[idx] < hi):
            return None
        val = preorder[idx]
        idx += 1
        node = TreeNode(val)
        node.left = build(lo, val)
        node.right = build(val, hi)
        return node

    return build(float("-inf"), float("inf"))


def bst_from_preorder_stack(preorder: List[int]) -> Optional[TreeNode]:
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    stack = [root]
    for v in preorder[1:]:
        node = TreeNode(v)
        parent = None
        while stack and stack[-1].val < v:
            parent = stack.pop()
        if parent:
            parent.right = node
        else:
            stack[-1].left = node
        stack.append(node)
    return root


def _preorder(n: Optional[TreeNode]) -> List[int]:
    return [] if not n else [n.val] + _preorder(n.left) + _preorder(n.right)


def _inorder(n: Optional[TreeNode]) -> List[int]:
    return [] if not n else _inorder(n.left) + [n.val] + _inorder(n.right)


def _height(n: Optional[TreeNode]) -> int:
    return 0 if not n else 1 + max(_height(n.left), _height(n.right))


if __name__ == "__main__":
    for fn in (bst_from_preorder, bst_from_preorder_stack):
        r = fn([8, 5, 1, 7, 10, 12])
        assert r.val == 8 and r.left.val == 5 and r.right.val == 10
        assert r.left.left.val == 1 and r.left.right.val == 7
        assert r.right.left is None and r.right.right.val == 12
        r = fn([1, 3])
        assert r.val == 1 and r.left is None and r.right.val == 3
        r = fn([5])
        assert r.val == 5 and r.left is None and r.right is None
        arr = [10, 9, 8, 7, 6]  # left skewed
        assert _height(fn(arr)) == 5 and _preorder(fn(arr)) == arr
        arr = [1, 2, 3, 4, 5]  # right skewed
        assert _height(fn(arr)) == 5 and _preorder(fn(arr)) == arr
        arr = [50, 30, 20, 40, 70, 60, 80]
        t = fn(arr)
        assert _preorder(t) == arr and _inorder(t) == sorted(arr)
    print("All tests passed")
