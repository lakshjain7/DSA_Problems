"""
Problem: 199. Binary Tree Right Side View
Difficulty: Medium
Topics: Tree, BFS, DFS

Problem Statement:
Given the root of a binary tree, imagine yourself standing on the right side of it.
Return the values of the nodes you can see ordered from top to bottom.
A node is visible from the right side if it is the rightmost node at its depth level.

Examples:
    Input: root = [1,2,3,null,5,null,4]
    Output: [1,3,4]

    Input: root = [1,null,3]
    Output: [1,3]

    Input: root = []
    Output: []

Constraints:
    - The number of nodes in the tree is in the range [0, 100].
    - -100 <= Node.val <= 100

Approach (BFS - Level Order):
    Perform BFS level-order traversal using a deque. At each level, record the
    value of the LAST node processed — that's the rightmost visible node.
    We know the level size upfront (len(queue) before popping), so we can
    identify the last element without post-processing.

    Time: O(n) — every node is enqueued/dequeued exactly once
    Space: O(n) — queue holds at most one full level (up to n/2 nodes at leaf level)

Alternative Approach (DFS - Right-first):
    DFS traversing right child before left child. Maintain current depth.
    If depth == len(result), this is the FIRST node seen at this depth in our
    right-first traversal — it's the rightmost node. Append it.

    Time: O(n), Space: O(h) where h is tree height (recursion stack)
"""

from collections import deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right


def rightSideView(root: Optional[TreeNode]) -> List[int]:
    """BFS approach: take the last element at each level."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:  # last node at this level = rightmost visible
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result


def rightSideView_dfs(root: Optional[TreeNode]) -> List[int]:
    """DFS (right-first) approach: first node encountered at each depth is rightmost."""
    result = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return
        if depth == len(result):         # first visit to this depth from the right
            result.append(node.val)
        dfs(node.right, depth + 1)       # explore right subtree first
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return result


# ---------------------------------------------------------------------------
# Helpers for testing
# ---------------------------------------------------------------------------

def build_tree(vals: list) -> Optional[TreeNode]:
    """Build tree from level-order list (None = missing node)."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while queue and i < len(vals):
        node = queue.popleft()
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
    # Test 1: [1,2,3,null,5,null,4] -> [1,3,4]
    root = build_tree([1, 2, 3, None, 5, None, 4])
    assert rightSideView(root) == [1, 3, 4], "Test 1 BFS"
    assert rightSideView_dfs(root) == [1, 3, 4], "Test 1 DFS"

    # Test 2: right-heavy [1,null,3] -> [1,3]
    root = build_tree([1, None, 3])
    assert rightSideView(root) == [1, 3], "Test 2 BFS"
    assert rightSideView_dfs(root) == [1, 3], "Test 2 DFS"

    # Test 3: empty tree -> []
    assert rightSideView(None) == [], "Test 3 BFS"
    assert rightSideView_dfs(None) == [], "Test 3 DFS"

    # Test 4: single node -> [1]
    root = build_tree([1])
    assert rightSideView(root) == [1], "Test 4 BFS"
    assert rightSideView_dfs(root) == [1], "Test 4 DFS"

    # Test 5: left-skewed (only left children visible from right) [1,2,null,3]
    root = build_tree([1, 2, None, 3, None])
    assert rightSideView(root) == [1, 2, 3], "Test 5 BFS"
    assert rightSideView_dfs(root) == [1, 2, 3], "Test 5 DFS"

    # Test 6: perfect binary tree — only rightmost path visible
    root = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert rightSideView(root) == [1, 3, 7], "Test 6 BFS"
    assert rightSideView_dfs(root) == [1, 3, 7], "Test 6 DFS"

    print("All tests passed!")
