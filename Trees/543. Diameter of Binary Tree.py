"""
Problem 543: Diameter of Binary Tree
Difficulty: Medium
Topics: Trees, DFS, Recursion

Problem Statement:
Given the root of a binary tree, return the length of the diameter of the tree.
The diameter of a binary tree is the length of the longest path between any two nodes
in a tree. This path may or may not pass through the root.
The length of a path between two nodes is represented by the number of edges between them.

Examples:
    Input: root = [1,2,3,4,5]
    Output: 3
    Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3].

    Input: root = [1,2]
    Output: 1

Constraints:
    - The number of nodes in the tree is in the range [1, 10^4].
    - -100 <= Node.val <= 100

Approach:
    For each node, the longest path passing through it = left_depth + right_depth.
    We DFS to compute the depth of each subtree while tracking the global max diameter.
    This avoids recomputing depths — O(n) single pass.

Complexity:
    Time:  O(n) — visit each node once
    Space: O(h) — recursion stack, h = height of tree (O(n) worst case, O(log n) balanced)
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.diameter = 0

        def depth(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            # Update global diameter: path through current node
            self.diameter = max(self.diameter, left + right)
            return 1 + max(left, right)

        depth(root)
        return self.diameter


# Alternative approach: return (max_diameter, depth) tuple to avoid global state
class SolutionFunctional:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode]):
            """Returns (diameter, depth) for the subtree."""
            if not node:
                return 0, 0
            left_diam, left_depth = dfs(node.left)
            right_diam, right_depth = dfs(node.right)
            curr_diam = max(left_diam, right_diam, left_depth + right_depth)
            return curr_diam, 1 + max(left_depth, right_depth)

        diameter, _ = dfs(root)
        return diameter


def build_tree(vals: list, i: int = 0) -> Optional[TreeNode]:
    if i >= len(vals) or vals[i] is None:
        return None
    node = TreeNode(vals[i])
    node.left = build_tree(vals, 2 * i + 1)
    node.right = build_tree(vals, 2 * i + 2)
    return node


if __name__ == "__main__":
    sol = Solution()
    sol2 = SolutionFunctional()

    # Test 1: [1,2,3,4,5] -> diameter = 3
    root = build_tree([1, 2, 3, 4, 5])
    assert sol.diameterOfBinaryTree(root) == 3
    root = build_tree([1, 2, 3, 4, 5])
    assert sol2.diameterOfBinaryTree(root) == 3

    # Test 2: [1,2] -> diameter = 1
    root = build_tree([1, 2])
    assert sol.diameterOfBinaryTree(root) == 1

    # Test 3: single node -> diameter = 0
    root = TreeNode(1)
    assert sol.diameterOfBinaryTree(root) == 0

    # Test 4: linear chain [1,2,None,3] -> diameter = 2
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    assert sol.diameterOfBinaryTree(root) == 2
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    assert sol2.diameterOfBinaryTree(root) == 2

    # Test 5: path not through root
    # Tree:     1
    #          /
    #         2
    #        / \
    #       3   4
    #      /     \
    #     5       6
    # diameter = 4 (5->3->2->4->6)
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    root.left.left.left = TreeNode(5)
    root.left.right.right = TreeNode(6)
    assert sol.diameterOfBinaryTree(root) == 4
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    root.left.left.left = TreeNode(5)
    root.left.right.right = TreeNode(6)
    assert sol2.diameterOfBinaryTree(root) == 4

    print("All tests passed!")
