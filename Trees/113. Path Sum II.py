"""
Problem 113. Path Sum II
Difficulty: Medium
Topics: Backtracking, Tree, Depth-First Search, Binary Tree

Given the root of a binary tree and an integer targetSum, return all
root-to-leaf paths where the sum of the node values in the path equals
targetSum. Each path should be returned as a list of the node values, not
node references. A root-to-leaf path is a path starting from the root and
ending at any leaf node. A leaf is a node with no children.

Example 1:
    Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
    Output: [[5,4,11,2],[5,8,4,5]]
Example 2:
    Input: root = [1,2,3], targetSum = 5
    Output: []
Example 3:
    Input: root = [1,2], targetSum = 0
    Output: []

Constraints:
    The number of nodes in the tree is in the range [0, 5000].
    -1000 <= Node.val <= 1000
    -1000 <= targetSum <= 1000

Approach (DFS + backtracking):
    Walk down from the root keeping the current path and the remaining sum.
    Push a node on entry; at a leaf, if the remaining sum equals the node's
    value, copy the path into the answer. Pop on exit so the shared path list
    is restored for sibling branches. Values can be negative, so we cannot
    prune early; every root-to-leaf path must be examined.

Complexity:
    Time:  O(N^2) worst case (O(N) nodes visited, but copying each of up to
           O(N) paths of length O(N) costs extra; O(N log N) for balanced).
    Space: O(H) recursion/path depth, excluding the output.

Alternative (iterative DFS with an explicit stack):
    Store (node, remaining, path) tuples on a stack; extend the path per child.
    Same time complexity, avoids recursion limits on skewed trees.
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
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        res: List[List[int]] = []
        path: List[int] = []

        def dfs(node: Optional[TreeNode], remaining: int) -> None:
            if not node:
                return
            path.append(node.val)
            remaining -= node.val
            if not node.left and not node.right:
                if remaining == 0:
                    res.append(path[:])
            else:
                dfs(node.left, remaining)
                dfs(node.right, remaining)
            path.pop()

        dfs(root, targetSum)
        return res

    def pathSumIterative(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        res: List[List[int]] = []
        if not root:
            return res
        stack = [(root, targetSum - root.val, [root.val])]
        while stack:
            node, rem, path = stack.pop()
            if not node.left and not node.right:
                if rem == 0:
                    res.append(path)
                continue
            if node.right:
                stack.append((node.right, rem - node.right.val, path + [node.right.val]))
            if node.left:
                stack.append((node.left, rem - node.left.val, path + [node.left.val]))
        return res


def build(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from LeetCode level-order list."""
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
    for f in (s.pathSum, s.pathSumIterative):
        t = build([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
        assert sorted(f(t, 22)) == [[5, 4, 11, 2], [5, 8, 4, 5]]
        assert f(build([1, 2, 3]), 5) == []
        assert f(build([1, 2]), 0) == []
        assert f(build([]), 0) == []
        assert f(build([1]), 1) == [[1]]
        assert f(build([1, 2]), 1) == []          # node 1 is not a leaf
        assert f(build([-2, None, -3]), -5) == [[-2, -3]]
        # negative values: multiple valid paths, no early pruning
        t = build([1, -2, -3, 1, 3, -2, None, -1])
        assert sorted(f(t, -1)) == [[1, -2, 1, -1]]
        t = build([0, 1, 1])
        assert sorted(f(t, 1)) == [[0, 1], [0, 1]]
        # deep skewed tree
        t = None
        for _ in range(500):
            t = TreeNode(1, t)
        assert f(t, 500) == [[1] * 500]
    print("All tests passed.")
