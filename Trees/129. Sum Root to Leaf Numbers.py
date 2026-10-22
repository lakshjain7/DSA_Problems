"""
129. Sum Root to Leaf Numbers
Difficulty: Medium
Topics: Tree, Depth-First Search, Binary Tree

Problem:
You are given the root of a binary tree containing digits from 0 to 9 only.
Each root-to-leaf path in the tree represents a number.
  * For example, the root-to-leaf path 1 -> 2 -> 3 represents the number 123.
Return the total sum of all root-to-leaf numbers. A leaf is a node with no children.

Example 1:
    Input: root = [1,2,3]
    Output: 25
    Explanation: 12 + 13 = 25

Example 2:
    Input: root = [4,9,0,5,1]
    Output: 1026
    Explanation: 495 + 491 + 40 = 1026

Constraints:
  * The number of nodes in the tree is in the range [1, 1000].
  * 0 <= Node.val <= 9
  * The depth of the tree will not exceed 10.

Approach (DFS carrying the prefix value):
Walking down from the root, the number formed so far is updated as
cur = cur * 10 + node.val. When we reach a leaf, cur is a complete
root-to-leaf number, so we add it to the total. Each node is visited once.

Complexity:
  Time:  O(n)
  Space: O(h) recursion stack (h <= 10 here, O(n) worst case in general)
"""
from collections import deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode], cur: int) -> int:
            if not node:
                return 0
            cur = cur * 10 + node.val
            if not node.left and not node.right:
                return cur
            return dfs(node.left, cur) + dfs(node.right, cur)

        return dfs(root, 0)

    # Alternative: iterative BFS carrying the prefix value with each node.
    def sumNumbersBFS(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        total = 0
        q = deque([(root, root.val)])
        while q:
            node, cur = q.popleft()
            if not node.left and not node.right:
                total += cur
                continue
            if node.left:
                q.append((node.left, cur * 10 + node.left.val))
            if node.right:
                q.append((node.right, cur * 10 + node.right.val))
        return total


def build(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from a level-order list (None = missing)."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3], 25),
        ([4, 9, 0, 5, 1], 1026),
        ([0], 0),
        ([5], 5),
        ([1, 0], 10),
        ([1, None, 2, None, 3], 123),
        ([9, 9, 9, 9, 9, 9, 9], 999 * 4),
        ([0, 1], 1),
    ]
    for vals, expected in cases:
        assert s.sumNumbers(build(vals)) == expected, vals
        assert s.sumNumbersBFS(build(vals)) == expected, vals
    print("All tests passed.")
