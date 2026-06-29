"""
Problem: 572. Subtree of Another Tree
Difficulty: Medium
Topics: Trees, DFS, Recursion, String Matching

Problem Statement:
Given the roots of two binary trees root and subRoot, return true if there is a subtree
of root with the same structure and node values of subRoot and false otherwise.

A subtree of a binary tree tree is a tree that consists of a node in tree and all of
this node's descendants. The tree tree could also be considered as a subtree of itself.

Examples:
  Input: root = [3,4,5,1,2], subRoot = [4,1,2]
  Output: true

  Input: root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
  Output: false

Constraints:
  - The number of nodes in the root tree is in the range [1, 2000].
  - The number of nodes in the subRoot tree is in the range [1, 1000].
  - -10^4 <= root.val, subRoot.val <= 10^4

Approach:
  For each node in `root`, check if the tree rooted at that node is identical to `subRoot`.
  - isSameTree(s, t): recursively checks if two trees are identical
  - isSubtree(root, subRoot): tries isSameTree at every node of root via DFS

  This is O(m*n) where m = nodes in root, n = nodes in subRoot.

  Alternative (Serialization): Serialize both trees to strings and check if
  subRoot's serialization is a substring of root's serialization. O(m+n) time
  but requires careful delimiter handling to avoid false matches.

Complexity:
  Time:  O(m * n) — for each of m nodes we do an O(n) comparison
  Space: O(h) — recursion stack depth, h = height of root tree
"""

from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """DFS approach: check isSameTree at every node of root."""
        if root is None:
            return False
        if self._is_same(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def _is_same(self, s: Optional[TreeNode], t: Optional[TreeNode]) -> bool:
        """Returns True if trees rooted at s and t are identical."""
        if s is None and t is None:
            return True
        if s is None or t is None:
            return False
        return s.val == t.val and self._is_same(s.left, t.left) and self._is_same(s.right, t.right)


class SolutionSerialization:
    """Alternative: serialize trees and use substring check."""

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def serialize(node: Optional[TreeNode]) -> str:
            if node is None:
                return "#null"
            return f"#{node.val}{serialize(node.left)}{serialize(node.right)}"

        return serialize(subRoot) in serialize(root)


# ─── Tests ───────────────────────────────────────────────────────────────────

def build(vals: list) -> Optional[TreeNode]:
    """Build a binary tree from level-order list (None = null)."""
    if not vals:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    sol = Solution()
    sol2 = SolutionSerialization()

    # Example 1: subRoot [4,1,2] is a subtree of root [3,4,5,1,2]
    root = build([3, 4, 5, 1, 2])
    subRoot = build([4, 1, 2])
    assert sol.isSubtree(root, subRoot) == True
    assert sol2.isSubtree(root, subRoot) == True

    # Example 2: extra node breaks subtree match
    root2 = build([3, 4, 5, 1, 2, None, None, None, None, 0])
    subRoot2 = build([4, 1, 2])
    assert sol.isSubtree(root2, subRoot2) == False
    assert sol2.isSubtree(root2, subRoot2) == False

    # Edge: single node trees, same value
    assert sol.isSubtree(TreeNode(1), TreeNode(1)) == True

    # Edge: subRoot is the entire root
    root3 = build([1, 2, 3])
    assert sol.isSubtree(root3, build([1, 2, 3])) == True

    # Edge: subRoot larger than root → False
    assert sol.isSubtree(TreeNode(1), build([1, 2])) == False

    # Edge: root is None (shouldn't happen per constraints, but guard)
    assert sol.isSubtree(None, TreeNode(1)) == False

    print("All 572 tests passed!")
