"""
Problem: 102. Binary Tree Level Order Traversal
Difficulty: Medium
Topics: Tree, Breadth-First Search (BFS), Binary Tree

Problem Statement:
    Given the root of a binary tree, return the level order traversal of its nodes'
    values (i.e., from left to right, level by level).

Examples:
    Input: root = [3,9,20,null,null,15,7]
    Output: [[3],[9,20],[15,7]]

    Input: root = [1]
    Output: [[1]]

    Input: root = []
    Output: []

Constraints:
    - The number of nodes in the tree is in the range [0, 2000].
    - -1000 <= Node.val <= 1000

Approach:
    BFS with a queue. Process the tree level by level:
    1. Enqueue the root.
    2. At each iteration, record how many nodes are currently in the queue (= level size).
    3. Dequeue exactly that many nodes, collecting their values into a level list.
    4. For each dequeued node, enqueue its left and right children (if they exist).
    5. After processing all nodes in the level, append the level list to the result.

    The key insight: snapshot the queue size BEFORE processing each level.
    This cleanly separates one level from the next without needing sentinel nodes.

Complexity:
    Time:  O(n) — each node is enqueued and dequeued exactly once
    Space: O(n) — queue holds at most n/2 nodes (the last level of a complete binary tree)

Alternative Approach:
    DFS (recursive) with level index tracking:
    Pass a `level` parameter through the DFS. If result[level] doesn't exist yet,
    create it. Append node.val to result[level]. Recurse left (level+1), right (level+1).
    Same O(n) time, O(h) space for the call stack (h = tree height).
"""

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right


def levelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result


def levelOrder_dfs(root: Optional[TreeNode]) -> List[List[int]]:
    result = []

    def dfs(node: Optional[TreeNode], level: int) -> None:
        if not node:
            return
        if level == len(result):
            result.append([])
        result[level].append(node.val)
        dfs(node.left, level + 1)
        dfs(node.right, level + 1)

    dfs(root, 0)
    return result


def build_tree(values: List) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    assert levelOrder(None) == []
    assert levelOrder_dfs(None) == []
    root = TreeNode(1)
    assert levelOrder(root) == [[1]]
    assert levelOrder_dfs(root) == [[1]]
    root = build_tree([3, 9, 20, None, None, 15, 7])
    assert levelOrder(root) == [[3], [9, 20], [15, 7]]
    assert levelOrder_dfs(root) == [[3], [9, 20], [15, 7]]
    root = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert levelOrder(root) == [[1], [2, 3], [4, 5, 6, 7]]
    root = build_tree([5, 3, 8, 1, 4, 7, 9, None, 2])
    assert levelOrder(root) == levelOrder_dfs(root)
    print("All tests passed for 102. Binary Tree Level Order Traversal!")
