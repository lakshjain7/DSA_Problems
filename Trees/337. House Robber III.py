"""
337. House Robber III
Difficulty: Medium
Topics: Dynamic Programming, Tree, Depth-First Search, Binary Tree

Problem:
The thief has found himself a new place for his thievery again. There is only
one entrance to this area, called root. Besides the root, each house has one
and only one parent house. All houses in this place form a binary tree. It
will automatically contact the police if two directly-linked houses were
broken into on the same night.
Given the root of the binary tree, return the maximum amount of money the
thief can rob without alerting the police.

Example 1:
    Input: root = [3,2,3,null,3,null,1]
    Output: 7
    Explanation: 3 + 3 + 1 = 7.
Example 2:
    Input: root = [3,4,5,1,3,null,1]
    Output: 9
    Explanation: 4 + 5 = 9.

Constraints:
    The number of nodes in the tree is in the range [1, 10^4].
    0 <= Node.val <= 10^4

Approach (post-order DP returning a pair):
    For every node compute (rob, skip):
      rob  = node.val + skip(left) + skip(right)       (children must be skipped)
      skip = max(rob,skip)(left) + max(rob,skip)(right) (children are free)
    The answer is max(rob, skip) at the root. Each node is solved once, and
    the pair removes the overlapping subproblems that make naive recursion
    exponential.

Complexity:
    Time:  O(n)
    Space: O(h) recursion stack (iterative version below avoids recursion limits)

Alternative: memoised recursion on node -> best, O(n) time and O(n) space.
"""
from typing import Optional, List


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def rob(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    # iterative post-order to be safe for skewed trees of depth 10^4
    res = {None: (0, 0)}
    stack = [(root, False)]
    while stack:
        node, visited = stack.pop()
        if node is None:
            continue
        if visited:
            lr, ls = res[node.left]
            rr, rs = res[node.right]
            take = node.val + ls + rs
            skip = max(lr, ls) + max(rr, rs)
            res[node] = (take, skip)
        else:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))
    return max(res[root])


def rob_memo(root: Optional[TreeNode]) -> int:
    """Alternative: memoised recursion on (node)."""
    memo = {}

    def go(node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        if node in memo:
            return memo[node]
        take = node.val
        if node.left:
            take += go(node.left.left) + go(node.left.right)
        if node.right:
            take += go(node.right.left) + go(node.right.right)
        memo[node] = max(take, go(node.left) + go(node.right))
        return memo[node]

    return go(root)


def build(vals: List) -> Optional[TreeNode]:
    if not vals or vals[0] is None:
        return None
    nodes = [TreeNode(vals[0])]
    q, i = [nodes[0]], 1
    while q and i < len(vals):
        cur = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            cur.left = TreeNode(vals[i]); q.append(cur.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            cur.right = TreeNode(vals[i]); q.append(cur.right)
        i += 1
    return nodes[0]


if __name__ == "__main__":
    for f in (rob, rob_memo):
        assert f(build([3, 2, 3, None, 3, None, 1])) == 7
        assert f(build([3, 4, 5, 1, 3, None, 1])) == 9
        assert f(build([5])) == 5
        assert f(build([0])) == 0
        assert f(build([2, 1, 3, None, 4])) == 7
        assert f(build([4, 1, None, 2, None, 3])) == 7  # skewed: 4 + 3
    # deep skewed tree
    root = TreeNode(1)
    cur = root
    for _ in range(9999):
        cur.left = TreeNode(1)
        cur = cur.left
    assert rob(root) == 5000
    print("All tests passed")
