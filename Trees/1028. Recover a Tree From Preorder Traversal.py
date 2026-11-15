"""
1028. Recover a Tree From Preorder Traversal
Difficulty: Hard
Topics: String, Tree, Depth-First Search, Binary Tree, Stack

Problem:
We run a preorder depth-first search (DFS) on the root of a binary tree.

At each node in this traversal, we output D dashes (where D is the depth of
this node), then we output the value of this node. If the depth of a node is
D, the depth of its immediate child is D + 1. The depth of the root node is 0.

If a node has only one child, that child is guaranteed to be the left child.

Given the output traversal of this traversal, recover the tree and return its
root.

Example 1:
    Input: traversal = "1-2--3--4-5--6--7"
    Output: [1,2,5,3,4,6,7]

Example 2:
    Input: traversal = "1-2--3---4-5--6---7"
    Output: [1,2,5,3,null,6,null,4,null,7]

Example 3:
    Input: traversal = "1-401--349---90--88"
    Output: [1,401,null,349,88,90]

Constraints:
    The number of nodes in the original tree is in the range [1, 1000].
    1 <= Node.val <= 10^9

Approach (Iterative Stack of the Current Root-to-Node Path):
    Parse the string into (depth, value) tokens. Keep a stack holding the
    path from the root to the most recently created node, so stack[i] is the
    node at depth i on that path.
      - For a new token at depth d, pop until len(stack) == d. The top is now
        the parent (preorder guarantees the parent is the latest node at
        depth d-1).
      - Attach as left child if the parent has none, otherwise as right child
        (a single child is always left, and the left subtree is fully emitted
        before the right in preorder).
      - Push the new node.
    stack[0] is the root at the end.

Complexity:
    Time:  O(L) where L = len(traversal); each char is read once and each node
           is pushed/popped at most once.
    Space: O(H) for the stack, H = tree height (O(n) worst case).
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def recover_from_preorder(traversal: str) -> Optional[TreeNode]:
    stack: List[TreeNode] = []
    i, n = 0, len(traversal)
    while i < n:
        depth = 0
        while i < n and traversal[i] == "-":
            depth += 1
            i += 1
        val = 0
        while i < n and traversal[i].isdigit():
            val = val * 10 + ord(traversal[i]) - 48
            i += 1

        node = TreeNode(val)
        while len(stack) > depth:
            stack.pop()
        if stack:
            parent = stack[-1]
            if parent.left is None:
                parent.left = node
            else:
                parent.right = node
        stack.append(node)
    return stack[0] if stack else None


def recover_from_preorder_recursive(traversal: str) -> Optional[TreeNode]:
    """Alternative: recursive descent. build(d) consumes the next token only if
    its depth equals d, then recursively builds left and right at depth d+1."""
    tokens = []
    i, n = 0, len(traversal)
    while i < n:
        d = 0
        while traversal[i] == "-":
            d += 1
            i += 1
        j = i
        while j < n and traversal[j].isdigit():
            j += 1
        tokens.append((d, int(traversal[i:j])))
        i = j

    idx = 0

    def build(d: int) -> Optional[TreeNode]:
        nonlocal idx
        if idx == len(tokens) or tokens[idx][0] != d:
            return None
        node = TreeNode(tokens[idx][1])
        idx += 1
        node.left = build(d + 1)
        node.right = build(d + 1)
        return node

    return build(0)


# ---------- helpers for testing ----------
def to_level_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """LeetCode-style level-order serialization with trailing Nones stripped."""
    if not root:
        return []
    out: List[Optional[int]] = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def to_preorder_string(root: Optional[TreeNode], depth: int = 0) -> str:
    if not root:
        return ""
    return ("-" * depth + str(root.val)
            + to_preorder_string(root.left, depth + 1)
            + to_preorder_string(root.right, depth + 1))


if __name__ == "__main__":
    import random

    cases = [
        ("1-2--3--4-5--6--7", [1, 2, 5, 3, 4, 6, 7]),
        ("1-2--3---4-5--6---7", [1, 2, 5, 3, None, 6, None, 4, None, 7]),
        ("1-401--349---90--88", [1, 401, None, 349, 88, 90]),
        ("7", [7]),                                   # single node
        ("1-2--3---4", [1, 2, None, 3, None, 4]),      # left-only chain
        ("1000000000-1", [1000000000, 1]),            # large value
    ]
    for f in (recover_from_preorder, recover_from_preorder_recursive):
        for s, expected in cases:
            assert to_level_list(f(s)) == expected, (f.__name__, s)

    # Round-trip on random trees that respect "single child is left".
    random.seed(7)

    def rand_tree(depth: int) -> Optional[TreeNode]:
        if depth > 6 or random.random() < 0.25:
            return None
        node = TreeNode(random.randint(1, 999))
        node.left = rand_tree(depth + 1)
        if node.left:
            node.right = rand_tree(depth + 1)
        return node

    for _ in range(300):
        t = rand_tree(0) or TreeNode(1)
        s = to_preorder_string(t)
        assert to_preorder_string(recover_from_preorder(s)) == s
        assert to_preorder_string(recover_from_preorder_recursive(s)) == s

    print("All tests passed for 1028. Recover a Tree From Preorder Traversal")
