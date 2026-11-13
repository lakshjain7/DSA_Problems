"""
1110. Delete Nodes And Return Forest
Difficulty: Medium
Topics: Array, Hash Table, Tree, Depth-First Search, Binary Tree

Problem:
Given the root of a binary tree, each node in the tree has a distinct value.
After deleting all nodes with a value in to_delete, we are left with a forest
(a disjoint union of trees).
Return the roots of the trees in the remaining forest. You may return the
result in any order.

Example 1:
  Input: root = [1,2,3,4,5,6,7], to_delete = [3,5]
  Output: [[1,2,null,4],[6],[7]]

Example 2:
  Input: root = [1,2,4,null,3], to_delete = [3]
  Output: [[1,2,4]]

Constraints:
  The number of nodes in the given tree is at most 1000.
  Each node has a distinct value between 1 and 1000.
  to_delete.length <= 1000
  to_delete contains distinct values between 1 and 1000.

Approach (Post-order DFS with "is_root" flag):
  Put to_delete in a set for O(1) lookups. Recurse with dfs(node, is_root):
    - deleted = node.val in to_delete
    - If the node survives and its parent was deleted (or it is the original
      root), it starts a new tree → append it to the answer.
    - Recurse into children, telling them they are roots iff THIS node is
      deleted. Each recursive call returns None if that child was deleted, so
      we reassign node.left / node.right to cut the deleted links.
    - Return None if this node is deleted, else the node itself.
  The decision for each node only depends on its own membership and its
  parent's, which is exactly what the flag carries down.

Complexity:
  Time:  O(n + d) — every node is visited once, d = len(to_delete) for the set.
  Space: O(h + d) — recursion depth h plus the set.

Alternative (BFS with parent unlinking):
  Iterate level by level with a queue. When a node is to be deleted, push its
  non-deleted children into the result, and unlink it from its parent. Same
  O(n) time, O(n) space, and avoids recursion limits on skewed trees.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def delNodes(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:
        dels = set(to_delete)
        forest: List[TreeNode] = []

        def dfs(node: Optional[TreeNode], is_root: bool) -> Optional[TreeNode]:
            if not node:
                return None
            deleted = node.val in dels
            if is_root and not deleted:
                forest.append(node)
            node.left = dfs(node.left, deleted)
            node.right = dfs(node.right, deleted)
            return None if deleted else node

        dfs(root, True)
        return forest

    def delNodes_bfs(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:
        if not root:
            return []
        dels = set(to_delete)
        forest: List[TreeNode] = [] if root.val in dels else [root]
        q = deque([root])
        while q:
            node = q.popleft()
            for side in ("left", "right"):
                child = getattr(node, side)
                if not child:
                    continue
                q.append(child)
                if child.val in dels:
                    setattr(node, side, None)
                elif node.val in dels:
                    forest.append(child)
        return forest


# ---------- helpers for tests ----------
def build(vals: List[Optional[int]]) -> Optional[TreeNode]:
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i]); q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i]); q.append(node.right)
        i += 1
    return root


def serialize(root: Optional[TreeNode]) -> List[Optional[int]]:
    out: List[Optional[int]] = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def normalize(forest: List[TreeNode]):
    return sorted(serialize(t) for t in forest)


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3, 4, 5, 6, 7], [3, 5], [[1, 2, None, 4], [6], [7]]),
        ([1, 2, 4, None, 3], [3], [[1, 2, 4]]),
        ([1], [1], []),                                   # delete only node
        ([1], [], [[1]]),                                 # delete nothing
        ([1, 2, 3], [1], [[2], [3]]),                     # delete root
        ([1, 2, 3], [1, 2, 3], []),                       # delete everything
        ([1, 2, None, 3, None, 4], [2, 4], [[1], [3]]),   # skewed chain
        ([1, 2, 3, None, None, None, 4], [1, 3], [[2], [4]]),
    ]
    for vals, dels, exp in cases:
        got = normalize(s.delNodes(build(vals), dels))
        assert got == sorted(exp), (vals, dels, got, exp)
        got2 = normalize(s.delNodes_bfs(build(vals), dels))
        assert got2 == sorted(exp), (vals, dels, got2, exp)
    assert s.delNodes(None, [1]) == [] and s.delNodes_bfs(None, [1]) == []

    print("All tests passed for 1110. Delete Nodes And Return Forest")
