"""
1372. Longest ZigZag Path in a Binary Tree
Difficulty: Medium
Topics: Tree, Depth-First Search, Dynamic Programming, Binary Tree

Problem Statement
-----------------
You are given the root of a binary tree.

A ZigZag path for a binary tree is defined as follows:
  - Choose any node in the binary tree and a direction (right or left).
  - If the current direction is right, move to the right child of the current
    node; otherwise, move to the left child.
  - Change the direction from right to left or from left to right.
  - Repeat the second and third steps until you can't move in the tree.

The zigzag length is defined as the number of nodes visited minus 1.
(A single node has a zigzag length of 0.)

Return the longest ZigZag path contained in that tree.

Examples
--------
Example 1:
    Input:  root = [1,null,1,1,1,null,null,1,1,null,1,null,null,null,1]
    Output: 3
    Explanation: Longest ZigZag path is right -> left -> right (length 3).

Example 2:
    Input:  root = [1,1,1,null,1,null,null,1,1,null,1]
    Output: 4
    Explanation: Longest ZigZag path is left -> right -> left -> right.

Example 3:
    Input:  root = [1]
    Output: 0

Constraints
-----------
    - The number of nodes in the tree is in the range [1, 5 * 10^4].
    - 1 <= Node.val <= 100

Approach
--------
This is a classic "tree DP by post-order DFS" problem. At every node we want to
know two things:
    - go_left:  the length of the zigzag path that STARTS at this node by first
                moving to its LEFT child (then it must alternate).
    - go_right: the length of the zigzag path that STARTS at this node by first
                moving to its RIGHT child.

Key recurrence. If I stand on `node` and I want to step LEFT, then from the left
child I am forced to continue by stepping RIGHT (the direction must alternate).
Therefore:

    go_left(node)  = 1 + go_right(node.left)   (0 if node.left is None)
    go_right(node) = 1 + go_left(node.right)    (0 if node.right is None)

The answer for the whole tree is the maximum of go_left / go_right seen at any
node, because a zigzag path can start anywhere.

We compute this in a single post-order traversal: each call returns the pair
(go_left, go_right) for the current node, and we update a running global maximum.

Why it works: every zigzag path has a unique top-most node (the node closest to
the root). At that top node, the path is exactly "step in some direction, then
alternate" — which is precisely go_left or go_right. By taking the max over all
nodes we consider every possible starting/top node exactly once.

Complexity
----------
    Time:  O(n) - each node is visited once.
    Space: O(h) - recursion stack, where h is the height of the tree
                  (O(n) worst case for a skewed tree, O(log n) if balanced).
"""

from typing import Optional, Tuple


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        self.best = 0

        def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
            # Returns (go_left, go_right) for `node`.
            if node is None:
                # -1 so that a real child contributes 1 + (-1) = 0 correctly
                # when that child is missing.
                return (-1, -1)

            left_pair = dfs(node.left)
            right_pair = dfs(node.right)

            # Stepping left, then must continue right from the left child.
            go_left = 1 + left_pair[1]
            # Stepping right, then must continue left from the right child.
            go_right = 1 + right_pair[0]

            self.best = max(self.best, go_left, go_right)
            return (go_left, go_right)

        dfs(root)
        return self.best


class SolutionIterative:
    """
    Alternative: iterative DFS using an explicit stack, avoiding recursion depth
    limits for very deep (skewed) trees. We memoize (go_left, go_right) per node
    using a dictionary and process children before parents via a two-pass stack.
    """

    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        best = 0
        # memo[node] = (go_left, go_right)
        memo = {}
        # Post-order iterative traversal.
        stack = [(root, False)]
        while stack:
            node, processed = stack.pop()
            if node is None:
                continue
            if processed:
                left = memo.get(node.left, (-1, -1))
                right = memo.get(node.right, (-1, -1))
                go_left = 1 + left[1]
                go_right = 1 + right[0]
                memo[node] = (go_left, go_right)
                best = max(best, go_left, go_right)
            else:
                stack.append((node, True))
                if node.left:
                    stack.append((node.left, False))
                if node.right:
                    stack.append((node.right, False))
        return best


def build_tree(values):
    """Build a binary tree from a level-order list with None for missing nodes."""
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
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
    sol = Solution()
    sol_it = SolutionIterative()

    # Example 1
    t1 = build_tree([1, None, 1, 1, 1, None, None, 1, 1, None, 1,
                     None, None, None, 1])
    assert sol.longestZigZag(t1) == 3
    assert sol_it.longestZigZag(t1) == 3

    # Example 2
    t2 = build_tree([1, 1, 1, None, 1, None, None, 1, 1, None, 1])
    assert sol.longestZigZag(t2) == 4
    assert sol_it.longestZigZag(t2) == 4

    # Example 3: single node
    t3 = build_tree([1])
    assert sol.longestZigZag(t3) == 0
    assert sol_it.longestZigZag(t3) == 0

    # Edge: empty tree
    assert sol.longestZigZag(None) == 0
    assert sol_it.longestZigZag(None) == 0

    # Left-skewed chain: the best zigzag is a single left step (length 1),
    # since after moving left you must move right but there is no right child.
    #      1
    #     /
    #    2
    #   /
    #  3
    chain = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert sol.longestZigZag(chain) == 1
    assert sol_it.longestZigZag(chain) == 1

    # Perfect zigzag: 1 -> right(2) -> left(3) -> right(4), length 3.
    n4 = TreeNode(4)
    n3 = TreeNode(3, None, n4)
    n2 = TreeNode(2, n3, None)
    n1 = TreeNode(1, None, n2)
    assert sol.longestZigZag(n1) == 3
    assert sol_it.longestZigZag(n1) == 3

    # Perfect tree of depth 2: best zigzag is e.g. 1 -> left(2) -> right(5),
    # giving length 2.
    balanced = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert sol.longestZigZag(balanced) == 2
    assert sol_it.longestZigZag(balanced) == 2

    print("All tests passed for 1372. Longest ZigZag Path in a Binary Tree")
