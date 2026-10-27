"""
222. Count Complete Tree Nodes
Difficulty: Medium
Topics: Binary Search, Tree, Bit Manipulation, Binary Tree

Problem:
Given the root of a complete binary tree, return the number of the nodes in the tree.
In a complete binary tree every level, except possibly the last, is completely
filled, and all nodes in the last level are as far left as possible. The last
level h has between 1 and 2^h nodes inclusive. Design an algorithm that runs in
less than O(n) time complexity.

Example 1:
    Input: root = [1,2,3,4,5,6]   Output: 6
Example 2:
    Input: root = []              Output: 0
Example 3:
    Input: root = [1]             Output: 1

Constraints:
- The number of nodes is in the range [0, 5 * 10^4].
- 0 <= Node.val <= 5 * 10^4
- The tree is guaranteed to be complete.

Approach (compare left/right heights):
Compute the height of the leftmost path (lh) and rightmost path (rh).
If lh == rh the tree is perfect, so it has 2^lh - 1 nodes. Otherwise recurse on
both children. In a complete tree at least one child subtree is perfect, so
only one side recurses further -> O(log n) levels, each costing O(log n) height
computation.

Complexity:
- Time: O(log^2 n)
- Space: O(log n) recursion stack

Alternative: binary search over the last level's node index, checking existence
by walking from the root using the bits of the index. Also O(log^2 n).
"""
from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def countNodes(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    lh, rh = 0, 0
    l = r = root
    while l:
        lh += 1
        l = l.left
    while r:
        rh += 1
        r = r.right
    if lh == rh:
        return (1 << lh) - 1
    return 1 + countNodes(root.left) + countNodes(root.right)


def countNodesBinarySearch(root: Optional[TreeNode]) -> int:
    """Binary search on the index of the last node in the bottom level."""
    if not root:
        return 0
    depth = 0
    node = root
    while node.left:
        node = node.left
        depth += 1
    if depth == 0:
        return 1

    def exists(idx: int) -> bool:
        lo, hi = 0, (1 << depth) - 1
        cur = root
        for _ in range(depth):
            mid = (lo + hi) // 2
            if idx <= mid:
                cur, hi = cur.left, mid
            else:
                cur, lo = cur.right, mid + 1
        return cur is not None

    lo, hi = 0, (1 << depth) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if exists(mid):
            lo = mid + 1
        else:
            hi = mid - 1
    return (1 << depth) - 1 + lo


def build(n: int) -> Optional[TreeNode]:
    """Build a complete tree with n nodes (heap-style indexing)."""
    if n == 0:
        return None
    nodes = [TreeNode(i + 1) for i in range(n)]
    for i in range(n):
        if 2 * i + 1 < n:
            nodes[i].left = nodes[2 * i + 1]
        if 2 * i + 2 < n:
            nodes[i].right = nodes[2 * i + 2]
    return nodes[0]


if __name__ == "__main__":
    for n in list(range(0, 70)) + [1000, 4095, 4096, 50000]:
        t = build(n)
        assert countNodes(t) == n, n
        assert countNodesBinarySearch(t) == n, n
    print("All tests passed.")
