"""
450. Delete Node in a BST
Difficulty: Medium
Topics: Tree, Binary Search Tree, Binary Tree

Problem Statement:
Given a root node reference of a BST and a key, delete the node with the given
key in the BST. Return the root node reference (possibly updated) of the BST.
Deletion has two stages: search for the node to remove, then remove it.

Example 1:
    Input: root = [5,3,6,2,4,null,7], key = 3
    Output: [5,4,6,2,null,null,7]
Example 2:
    Input: root = [5,3,6,2,4,null,7], key = 0
    Output: [5,3,6,2,4,null,7]
Example 3:
    Input: root = [], key = 0
    Output: []

Constraints:
- The number of nodes is in [0, 10^4].
- -10^5 <= Node.val <= 10^5; all values unique; root is a valid BST.
- -10^5 <= key <= 10^5
Follow up: do it with time complexity O(height of tree).

Approach:
Walk down using BST ordering. When the node is found:
 - no left child -> return right child; no right child -> return left child;
 - two children -> replace its value with its in-order successor (smallest
   value in the right subtree), then delete that successor from the right
   subtree. The successor has no left child so that deletion is easy.

Complexity:
Time: O(h). Space: O(h) recursion (O(1) for the iterative version).

Alternative approach: iterative version tracking the parent pointer.
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            succ = root.right
            while succ.left:
                succ = succ.left
            root.val = succ.val
            root.right = self.deleteNode(root.right, succ.val)
        return root

    def deleteNodeIterative(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        parent, cur = None, root
        while cur and cur.val != key:
            parent = cur
            cur = cur.left if key < cur.val else cur.right
        if not cur:
            return root

        if cur.left and cur.right:
            sp, succ = cur, cur.right
            while succ.left:
                sp, succ = succ, succ.left
            cur.val = succ.val
            parent, cur = sp, succ  # now delete succ (has no left child)

        child = cur.left or cur.right
        if not parent:
            return child
        if parent.left is cur:
            parent.left = child
        else:
            parent.right = child
        return root


def build(vals: List[Optional[int]]) -> Optional[TreeNode]:
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q, i = [root], 1
    while q and i < len(vals):
        node = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i]); q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i]); q.append(node.right)
        i += 1
    return root


def inorder(n: Optional[TreeNode]) -> List[int]:
    return inorder(n.left) + [n.val] + inorder(n.right) if n else []


def is_bst(n: Optional[TreeNode]) -> bool:
    v = inorder(n)
    return all(a < b for a, b in zip(v, v[1:]))


if __name__ == "__main__":
    for fn in ("deleteNode", "deleteNodeIterative"):
        sol = Solution()
        f = getattr(sol, fn)
        r = f(build([5, 3, 6, 2, 4, None, 7]), 3)
        assert inorder(r) == [2, 4, 5, 6, 7] and is_bst(r)
        r = f(build([5, 3, 6, 2, 4, None, 7]), 0)
        assert inorder(r) == [2, 3, 4, 5, 6, 7]
        assert f(None, 0) is None
        # delete root with two children
        r = f(build([5, 3, 6, 2, 4, None, 7]), 5)
        assert inorder(r) == [2, 3, 4, 6, 7] and is_bst(r)
        # delete only node
        assert f(TreeNode(1), 1) is None
        # root with one child
        r = f(build([1, None, 2]), 1)
        assert r.val == 2 and r.left is None and r.right is None
        # leaf
        r = f(build([5, 3, 6, 2, 4, None, 7]), 7)
        assert inorder(r) == [2, 3, 4, 5, 6]
        # successor deeper than direct right child
        r = f(build([5, 3, 8, None, None, 6, 9, None, 7]), 5)
        assert inorder(r) == [3, 6, 7, 8, 9] and is_bst(r)
    print("All tests passed.")
