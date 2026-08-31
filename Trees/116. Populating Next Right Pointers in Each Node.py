"""
116. Populating Next Right Pointers in Each Node
Difficulty: Medium
Topics: Linked List, Tree, Depth-First Search, Breadth-First Search, Binary Tree

Problem Statement
-----------------
You are given a PERFECT binary tree where all leaves are on the same level, and
every parent has two children. The binary tree has the following definition:

    struct Node {
        int val;
        Node *left;
        Node *right;
        Node *next;
    }

Populate each next pointer to point to its next right node. If there is no next
right node, the next pointer should be set to NULL.

Initially, all next pointers are set to NULL.

Example 1:
    Input:  root = [1,2,3,4,5,6,7]
    Output: [1,#,2,3,#,4,5,6,7,#]
    Explanation: Given the perfect binary tree, your function should populate
    each next pointer to point to its next right node, just like in the figure.
    The serialized output is in level order as connected by the next pointers,
    with '#' signifying the end of each level.

Example 2:
    Input:  root = []
    Output: []

Constraints:
    - The number of nodes in the tree is in the range [0, 2^12 - 1].
    - -1000 <= Node.val <= 1000

Follow-up:
    - You may only use constant extra space.
    - The recursive approach is fine. You may assume implicit stack space does
      not count as extra space for this problem.

Approach (O(1) space, level-by-level using established next pointers)
--------------------------------------------------------------------
Because the tree is PERFECT, once level L is fully connected via `next`
pointers, we can traverse level L from left to right (following `next`) and
wire up the children on level L+1:

    For each node `cur` on the current level:
        cur.left.next  = cur.right
        cur.right.next = cur.next.left   (if cur.next exists)

We keep a `leftmost` pointer to the start of each level. When we descend, the
new leftmost is `leftmost.left`. We stop once `leftmost.left` is None (leaves).

This uses only a couple of pointers -> O(1) extra space, and each node is
visited once -> O(n) time. It works precisely because the tree is perfect:
every internal node has both children, so cur.next.left is always the correct
node to the right of cur.right.

Complexity
----------
Time:  O(n)  - every node is processed exactly once.
Space: O(1)  - only pointer variables (the follow-up requirement). The BFS
              alternative below uses O(n) for the queue.
"""

from collections import deque
from typing import Optional


class Node:
    def __init__(self, val: int = 0,
                 left: "Optional[Node]" = None,
                 right: "Optional[Node]" = None,
                 next: "Optional[Node]" = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution:
    def connect(self, root: "Optional[Node]") -> "Optional[Node]":
        """Constant-space level linking, exploiting the perfect-tree property."""
        leftmost = root
        while leftmost and leftmost.left:
            cur = leftmost
            while cur:
                # Connection 1: children of the same parent.
                cur.left.next = cur.right
                # Connection 2: across different parents.
                if cur.next:
                    cur.right.next = cur.next.left
                cur = cur.next
            leftmost = leftmost.left
        return root

    def connect_bfs(self, root: "Optional[Node]") -> "Optional[Node]":
        """Alternative: standard level-order BFS. Clear but uses O(n) space."""
        if not root:
            return None
        q = deque([root])
        while q:
            size = len(q)
            prev = None
            for _ in range(size):
                node = q.popleft()
                if prev:
                    prev.next = node
                prev = node
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
        return root


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------
def build_perfect_tree(values):
    """Build a perfect binary tree from a level-order list; return root."""
    if not values:
        return None
    nodes = [Node(v) for v in values]
    n = len(nodes)
    for i in range(n):
        li, ri = 2 * i + 1, 2 * i + 2
        if li < n:
            nodes[i].left = nodes[li]
        if ri < n:
            nodes[i].right = nodes[ri]
    return nodes[0]


def serialize_by_next(root):
    """Level-order serialization following `next` pointers, '#' ends a level."""
    out = []
    leftmost = root
    while leftmost:
        cur = leftmost
        while cur:
            out.append(cur.val)
            cur = cur.next
        out.append("#")
        leftmost = leftmost.left
    return out


if __name__ == "__main__":
    sol = Solution()

    # Example 1: perfect tree [1..7]
    root = build_perfect_tree([1, 2, 3, 4, 5, 6, 7])
    sol.connect(root)
    assert serialize_by_next(root) == [1, "#", 2, 3, "#", 4, 5, 6, 7, "#"]

    # Example 2: empty tree
    assert sol.connect(None) is None

    # Single node
    single = build_perfect_tree([1])
    sol.connect(single)
    assert single.next is None
    assert serialize_by_next(single) == [1, "#"]

    # Two levels [1,2,3]
    r2 = build_perfect_tree([1, 2, 3])
    sol.connect(r2)
    assert r2.next is None
    assert r2.left.next is r2.right
    assert r2.right.next is None

    # Cross-parent check on level 3: node 5.next should be node 6
    r3 = build_perfect_tree([1, 2, 3, 4, 5, 6, 7])
    sol.connect(r3)
    assert r3.left.left.next is r3.left.right          # 4 -> 5
    assert r3.left.right.next is r3.right.left         # 5 -> 6 (cross parent)
    assert r3.right.left.next is r3.right.right        # 6 -> 7
    assert r3.right.right.next is None                 # 7 -> None

    # BFS variant produces the same wiring
    rb = build_perfect_tree([1, 2, 3, 4, 5, 6, 7])
    sol.connect_bfs(rb)
    assert serialize_by_next(rb) == [1, "#", 2, 3, "#", 4, 5, 6, 7, "#"]

    print("All tests passed for 116. Populating Next Right Pointers in Each Node")
