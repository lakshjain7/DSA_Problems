"""
979. Distribute Coins in Binary Tree
Difficulty: Medium
Topics: Tree, Depth-First Search, Binary Tree

Problem:
You are given the root of a binary tree with n nodes where each node in the
tree has node.val coins. There are n coins in total throughout the whole tree.

In one move, we may choose two adjacent nodes and move one coin from one node
to another. A move may be from parent to child, or from child to parent.

Return the minimum number of moves required to make every node have exactly
one coin.

Example 1:
    Input: root = [3,0,0]
    Output: 2
    Explanation: From the root, move one coin to its left child and one coin
    to its right child.

Example 2:
    Input: root = [0,3,0]
    Output: 3
    Explanation: From the left child, move two coins to the root (two moves).
    Then move one coin from the root to the right child.

Constraints:
    The number of nodes in the tree is n.
    1 <= n <= 100
    0 <= Node.val <= n
    The sum of all Node.val is n.

Approach (post-order "excess" flow):
    For each subtree define excess = (coins in subtree) - (nodes in subtree).
    That subtree must push exactly |excess| coins across the single edge to
    its parent (out if positive, in if negative) - no fewer, since nothing
    else connects it to the rest of the tree, and no more is ever needed.
    So the answer is the sum of |excess| over every non-root subtree.

    A post-order DFS returns excess(node) = node.val - 1 + excess(left) +
    excess(right), and adds |excess(left)| + |excess(right)| to the move
    count while unwinding.

Complexity:
    Time:  O(n)  - each node visited once.
    Space: O(h)  - recursion stack, h = tree height (O(n) worst case).

Alternative (iterative post-order):
    Same excess computation with an explicit stack, avoiding recursion-depth
    limits on very skewed trees.
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def distributeCoins(root: Optional[TreeNode]) -> int:
    moves = 0

    def dfs(node: Optional[TreeNode]) -> int:
        nonlocal moves
        if node is None:
            return 0
        left = dfs(node.left)
        right = dfs(node.right)
        moves += abs(left) + abs(right)
        return node.val - 1 + left + right

    dfs(root)
    return moves


def distributeCoins_iterative(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    excess = {None: 0}
    moves = 0
    stack = [(root, False)]
    while stack:
        node, done = stack.pop()
        if done:
            l, r = excess[node.left], excess[node.right]
            moves += abs(l) + abs(r)
            excess[node] = node.val - 1 + l + r
        else:
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
    return moves


def build(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from LeetCode level-order list representation."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    for node in queue:
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
        if i >= len(values):
            break
    return root


if __name__ == "__main__":
    cases = [
        ([3, 0, 0], 2),
        ([0, 3, 0], 3),
        ([1], 0),
        ([1, 0, 2], 2),
        ([1, 0, 0, None, 3], 4),
        ([0, 0, None, 0, None, 4], 6),   # left-skewed chain: 0-0-0-4
        ([4, 0, None, 0, None, 0], 6),   # coins at the root of a chain
        ([0, 0, 0, 0, 0, 0, 7], 16),
    ]
    for vals, exp in cases:
        assert distributeCoins(build(vals)) == exp, (vals, distributeCoins(build(vals)))
        assert distributeCoins_iterative(build(vals)) == exp, vals

    # deep skewed tree: all n coins at the bottom leaf
    n = 2000
    root = cur = TreeNode(0)
    for _ in range(n - 2):
        cur.left = TreeNode(0)
        cur = cur.left
    cur.left = TreeNode(n)
    assert distributeCoins_iterative(root) == sum(range(1, n))

    print("All tests passed for 979. Distribute Coins in Binary Tree")
