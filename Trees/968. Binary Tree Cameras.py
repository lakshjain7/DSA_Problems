"""
968. Binary Tree Cameras
Difficulty: Hard
Topics: Tree, Depth-First Search, Dynamic Programming (Tree DP), Greedy

Problem
-------
You are given the root of a binary tree. We install cameras on the tree nodes
where each camera at a node can monitor its parent, itself, and its immediate
children.

Return the minimum number of cameras needed to monitor all nodes of the tree.

Examples
--------
Example 1:
    Input:  root = [0, 0, null, 0, 0]
    Output: 1
    Explanation: One camera is enough to monitor all nodes if placed as shown.

Example 2:
    Input:  root = [0, 0, null, 0, null, 0, null, null, 0]
    Output: 2
    Explanation: At least two cameras are needed to monitor all nodes of the tree.

Constraints
-----------
    The number of nodes in the tree is in the range [1, 1000].
    Node.val == 0

Approach — Greedy post-order DFS with three states
--------------------------------------------------
Traverse bottom-up. Each node reports one of three states to its parent:

    0 = NEEDS_COVER : this node is not covered by any camera and has no camera.
    1 = HAS_CAMERA  : this node has a camera installed.
    2 = COVERED     : this node is covered (by a child's camera) but has no
                      camera itself.

Treat a null child as COVERED (state 2) so that leaves are forced to report
NEEDS_COVER — we never waste a camera on a leaf; it is cheaper to place the
camera on the leaf's parent, which also covers siblings and the grandparent.

Rules when combining the two children's states at a node:
    1. If either child NEEDS_COVER (0)  -> we MUST place a camera here.
       Increment the count and return HAS_CAMERA.
    2. Else if either child HAS_CAMERA (1) -> this node is COVERED. Return COVERED.
    3. Otherwise (both children COVERED)   -> this node is NOT yet covered.
       Return NEEDS_COVER and let the parent decide.

After the DFS, if the root itself still reports NEEDS_COVER, add one final
camera for the root.

Why greedy is optimal: placing cameras as high as possible (on parents of
uncovered nodes) is never worse than placing them lower, because a camera on a
parent covers strictly more of the "upward" structure (itself, its children,
and its own parent). A standard exchange argument shows this leaf-driven,
bottom-up placement achieves the minimum.

Complexity
----------
    Time:  O(n)  — each node visited once
    Space: O(h)  — recursion stack, h = tree height (O(n) worst case)
"""

from typing import Optional

# State constants
NEEDS_COVER = 0
HAS_CAMERA = 1
COVERED = 2


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def min_camera_cover(root: Optional[TreeNode]) -> int:
    """Return the minimum number of cameras to monitor every node."""
    cameras = 0

    def dfs(node: Optional[TreeNode]) -> int:
        nonlocal cameras
        if node is None:
            return COVERED  # null nodes are considered already covered

        left = dfs(node.left)
        right = dfs(node.right)

        # A child needs cover -> we must put a camera here.
        if left == NEEDS_COVER or right == NEEDS_COVER:
            cameras += 1
            return HAS_CAMERA

        # A child has a camera -> this node is covered.
        if left == HAS_CAMERA or right == HAS_CAMERA:
            return COVERED

        # Both children covered, but nothing covers this node.
        return NEEDS_COVER

    # If the root ends up uncovered, it still needs its own camera.
    if dfs(root) == NEEDS_COVER:
        cameras += 1
    return cameras


def build_tree(values) -> Optional[TreeNode]:
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
    # Example 1: [0, 0, null, 0, 0] -> 1
    assert min_camera_cover(build_tree([0, 0, None, 0, 0])) == 1

    # Example 2: [0, 0, null, 0, null, 0, null, null, 0] -> 2
    assert min_camera_cover(
        build_tree([0, 0, None, 0, None, 0, None, None, 0])
    ) == 2

    # Single node -> needs one camera
    assert min_camera_cover(build_tree([0])) == 1

    # Two nodes -> one camera on the parent covers both
    assert min_camera_cover(build_tree([0, 0])) == 1

    # Perfect tree of 3 nodes -> root camera covers all
    assert min_camera_cover(build_tree([0, 0, 0])) == 1

    # Perfect tree of 7 nodes -> two cameras (on the two internal children)
    assert min_camera_cover(build_tree([0, 0, 0, 0, 0, 0, 0])) == 2

    # Long left-leaning chain of 4 -> two cameras needed.
    # chain: 1 - 2 - 3 - 4 (camera at node 3 covers 2/3/4, then root needs one).
    assert min_camera_cover(
        build_tree([0, 0, None, 0, None, 0])
    ) == 2

    # Empty tree -> 0 cameras
    assert min_camera_cover(None) == 0

    print("All tests passed for 968. Binary Tree Cameras")
