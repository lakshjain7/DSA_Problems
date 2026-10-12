"""
103. Binary Tree Zigzag Level Order Traversal
Difficulty: Medium
Topics: Tree, Breadth-First Search, Binary Tree

Problem:
Given the root of a binary tree, return the zigzag level order traversal of its
nodes' values. (i.e., from left to right, then right to left for the next level
and alternate between).

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: [[3],[20,9],[15,7]]
Example 2:
    Input: root = [1]
    Output: [[1]]
Example 3:
    Input: root = []
    Output: []

Constraints:
    The number of nodes in the tree is in the range [0, 2000].
    -100 <= Node.val <= 100

Approach (BFS with direction flag):
    Do a normal level-order traversal with a queue. For each level collect the
    values in left-to-right order, and reverse the level when the level index
    is odd. Using a deque per level and appendleft avoids the extra reversal.
    Correct because BFS visits each level fully before the next one, so only
    the output order within a level needs to alternate.

Complexity:
    Time:  O(n) - each node visited once.
    Space: O(w) for the queue, where w is max tree width (O(n) worst case).
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
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        res: List[List[int]] = []
        q = deque([root])
        left_to_right = True
        while q:
            level = deque()
            for _ in range(len(q)):
                node = q.popleft()
                if left_to_right:
                    level.append(node.val)
                else:
                    level.appendleft(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(list(level))
            left_to_right = not left_to_right
        return res

    # Alternative: recursive DFS, placing values by depth and reversing odd levels.
    def zigzagLevelOrderDFS(self, root: Optional[TreeNode]) -> List[List[int]]:
        res: List[List[int]] = []

        def dfs(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return
            if depth == len(res):
                res.append([])
            res[depth].append(node.val)
            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)

        dfs(root, 0)
        for i in range(1, len(res), 2):
            res[i].reverse()
        return res


def build(vals):
    """Build a tree from a level-order list with None for missing nodes."""
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
        ([3, 9, 20, None, None, 15, 7], [[3], [20, 9], [15, 7]]),
        ([1], [[1]]),
        ([], []),
        ([1, 2, 3, 4, None, None, 5], [[1], [3, 2], [4, 5]]),
        ([1, 2, None, 3, None, 4], [[1], [2], [3], [4]]),
        ([1, 2, 3, 4, 5, 6, 7], [[1], [3, 2], [4, 5, 6, 7]]),
    ]
    for vals, exp in cases:
        assert s.zigzagLevelOrder(build(vals)) == exp, (vals, exp)
        assert s.zigzagLevelOrderDFS(build(vals)) == exp, (vals, exp)
    print("All tests passed")
