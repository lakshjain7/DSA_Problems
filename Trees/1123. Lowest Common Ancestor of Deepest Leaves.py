"""
1123. Lowest Common Ancestor of Deepest Leaves
Difficulty: Medium
Topics: Hash Table, Tree, Depth-First Search, Breadth-First Search, Binary Tree

Problem Statement
-----------------
Given the root of a binary tree, return the lowest common ancestor (LCA) of
its deepest leaves.

Recall that:
    - The node of a binary tree is a leaf if and only if it has no children.
    - The depth of the root of the tree is 0. If the depth of a node is d,
      the depth of each of its children is d + 1.
    - The lowest common ancestor of a set S of nodes is the node A with the
      largest depth such that every node in S is in the subtree with root A.

Example 1:
    Input: root = [3,5,1,6,2,0,8,null,null,7,4]
    Output: [2,7,4]
    Explanation: The deepest leaves are 7 and 4, and their LCA is node 2.

Example 2:
    Input: root = [1]
    Output: [1]
    Explanation: The root is the deepest leaf and is its own LCA.

Example 3:
    Input: root = [0,1,3,null,2]
    Output: [2]
    Explanation: The deepest leaf is node 2; the LCA of one node is itself.

Constraints:
    The number of nodes in the tree will be in the range [1, 1000].
    0 <= Node.val <= 1000
    The values of the nodes in the tree are unique.

Note: This problem is identical to LeetCode 865 - Smallest Subtree with all
the Deepest Nodes.

Approach (Single Post-order DFS returning (depth, lca))
-------------------------------------------------------
Do one bottom-up DFS. For each node, recurse into both children and get back,
for each side, the maximum depth reachable in that subtree together with the
LCA of the deepest leaves within that subtree.

Combine at the current node:
    - If left depth == right depth, then the deepest leaves live in BOTH
      subtrees, so the current node is their lowest common ancestor.
    - If left depth  > right depth, the deepest leaves are entirely on the
      left, so propagate the left subtree's answer.
    - If right depth > left depth, propagate the right subtree's answer.

Each call returns (1 + max(childDepths), chosenLCA). A null node returns
(0, None). The root call yields the LCA of the globally deepest leaves.

Why it works: the deepest leaves overall are exactly the deepest leaves of
whichever subtree(s) reach the maximum depth. Balancing depths at a node is
precisely the condition that both subtrees contribute deepest leaves, making
that node the tightest common ancestor.

Complexity
----------
Time:  O(n) - each node visited once.
Space: O(h) - recursion stack, h = tree height (O(n) worst case, skewed tree).

Alternative Approach (Two-pass: BFS for max depth, then DFS for LCA)
-------------------------------------------------------------------
First a BFS/DFS records the maximum depth and the set of deepest-leaf nodes.
Then a second DFS computes the LCA of that node set. This is also O(n) time
but requires two traversals and extra bookkeeping, so the single-pass method
above is preferred. The single pass is used for the primary solution below.
"""

from typing import Optional, Tuple


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def lcaDeepestLeaves(root: Optional[TreeNode]) -> Optional[TreeNode]:
    def dfs(node: Optional[TreeNode]) -> Tuple[int, Optional[TreeNode]]:
        if not node:
            return 0, None

        left_depth, left_lca = dfs(node.left)
        right_depth, right_lca = dfs(node.right)

        if left_depth == right_depth:
            return left_depth + 1, node
        elif left_depth > right_depth:
            return left_depth + 1, left_lca
        else:
            return right_depth + 1, right_lca

    return dfs(root)[1]


# ---- Helpers for testing ----------------------------------------------------

def build_tree(values):
    """Build a binary tree from a LeetCode-style level-order list (with None)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values):
            if values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


if __name__ == "__main__":
    # Example 1: deepest leaves 7 and 4, LCA is node 2
    root1 = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    ans1 = lcaDeepestLeaves(root1)
    assert ans1 is not None and ans1.val == 2

    # Example 2: single node
    root2 = build_tree([1])
    ans2 = lcaDeepestLeaves(root2)
    assert ans2 is not None and ans2.val == 1

    # Example 3: single deepest leaf -> itself
    root3 = build_tree([0, 1, 3, None, 2])
    ans3 = lcaDeepestLeaves(root3)
    assert ans3 is not None and ans3.val == 2

    # Empty tree
    assert lcaDeepestLeaves(None) is None

    # Perfectly balanced tree: root is the LCA of all deepest leaves
    root4 = build_tree([1, 2, 3, 4, 5, 6, 7])
    ans4 = lcaDeepestLeaves(root4)
    assert ans4 is not None and ans4.val == 1

    # Left-skewed tree: deepest leaf is the last node, LCA is itself
    root5 = build_tree([1, 2, None, 3, None, 4])
    ans5 = lcaDeepestLeaves(root5)
    assert ans5 is not None and ans5.val == 4

    # Deepest leaves share a non-root ancestor
    #        1
    #       / \
    #      2   3
    #     /
    #    4
    #   / \
    #  5   6   -> deepest leaves 5,6 ; LCA = 4
    root6 = build_tree([1, 2, 3, 4, None, None, None, 5, 6])
    ans6 = lcaDeepestLeaves(root6)
    assert ans6 is not None and ans6.val == 4

    print("All tests passed for 1123. Lowest Common Ancestor of Deepest Leaves")
