"""
1373. Maximum Sum BST in Binary Tree
Difficulty: Hard
Topics: Dynamic Programming, Tree, Depth-First Search, Binary Search Tree,
        Binary Tree

Problem:
Given a binary tree root, return the maximum sum of all keys of any sub-tree
which is also a Binary Search Tree (BST).

Assume a BST is defined as follows:
  - The left subtree of a node contains only nodes with keys less than the
    node's key.
  - The right subtree of a node contains only nodes with keys greater than the
    node's key.
  - Both the left and right subtrees must also be binary search trees.

(The empty tree counts as a BST with sum 0, so the answer is never negative.)

Example 1:
    Input: root = [1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]
    Output: 20
    Explanation: The BST rooted at node 3 has sum 3+2+5+4+6 = 20.

Example 2:
    Input: root = [4,3,null,1,2]
    Output: 2
    Explanation: The single-node BST {2} has the maximum sum.

Example 3:
    Input: root = [-4,-2,-5]
    Output: 0
    Explanation: All values are negative; the empty BST gives 0.

Constraints:
    The number of nodes in the tree is in the range [1, 4 * 10^4].
    -4 * 10^4 <= Node.val <= 4 * 10^4

Approach (Post-order DFS returning subtree summaries):
    For every node we need to know whether its subtree is a BST, and if so its
    sum, min and max key. These can be computed bottom-up from the children:

        dfs(node) -> (is_bst, lo, hi, total)

      - Empty node: (True, +inf, -inf, 0). The sentinel min/max make the
        comparison below succeed automatically for missing children.
      - Node is a BST iff both children are BSTs and
            left.hi < node.val < right.lo
      - If BST: lo = min(left.lo, val), hi = max(right.hi, val),
                total = left.total + val + right.total; update the answer.
      - Otherwise return is_bst=False; ancestors can't be BSTs either.

    Each node is processed once with O(1) work. Recursion is done iteratively
    to avoid Python's recursion limit on skewed trees of 4*10^4 nodes.

Complexity:
    Time:  O(n) — every node visited once.
    Space: O(h) for the stack / per-node summaries kept until parent consumes
           them (O(n) worst case for a skewed tree).
"""

from typing import Dict, List, Optional, Tuple

INF = float("inf")


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


Info = Tuple[bool, float, float, int]  # (is_bst, min, max, sum)
EMPTY: Info = (True, INF, -INF, 0)


class Solution:
    """Iterative post-order DFS (safe for deep, skewed trees)."""

    def maxSumBST(self, root: Optional[TreeNode]) -> int:
        best = 0
        info: Dict[int, Info] = {}
        stack: List[Tuple[TreeNode, bool]] = [(root, False)] if root else []
        while stack:
            node, visited = stack.pop()
            if not visited:
                stack.append((node, True))
                if node.right:
                    stack.append((node.right, False))
                if node.left:
                    stack.append((node.left, False))
                continue
            l = info.pop(id(node.left), EMPTY) if node.left else EMPTY
            r = info.pop(id(node.right), EMPTY) if node.right else EMPTY
            if l[0] and r[0] and l[2] < node.val < r[1]:
                total = l[3] + node.val + r[3]
                best = max(best, total)
                info[id(node)] = (True, min(l[1], node.val), max(r[2], node.val), total)
            else:
                info[id(node)] = (False, 0, 0, 0)
        return best


class SolutionRecursive:
    """
    Alternative: the same post-order logic written recursively, which reads
    closer to the recurrence. Fine for balanced trees; may hit the recursion
    limit on very deep skewed inputs.
    """

    def maxSumBST(self, root: Optional[TreeNode]) -> int:
        best = 0

        def dfs(node: Optional[TreeNode]) -> Info:
            nonlocal best
            if not node:
                return EMPTY
            l, r = dfs(node.left), dfs(node.right)
            if l[0] and r[0] and l[2] < node.val < r[1]:
                total = l[3] + node.val + r[3]
                best = max(best, total)
                return (True, min(l[1], node.val), max(r[2], node.val), total)
            return (False, 0, 0, 0)

        dfs(root)
        return best


def build(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from LeetCode level-order list representation."""
    if not values or values[0] is None:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    queue = [root]
    i = 0
    for v in it:
        if i // 2 >= len(queue):
            break  # remaining values have no parent slot
        parent = queue[i // 2]
        node = TreeNode(v) if v is not None else None
        if i % 2 == 0:
            parent.left = node
        else:
            parent.right = node
        if node:
            queue.append(node)
        i += 1
    return root


def _brute(root: Optional[TreeNode]) -> int:
    def vals(n):
        return [] if not n else vals(n.left) + [n.val] + vals(n.right)

    def is_bst(n, lo=-INF, hi=INF):
        if not n:
            return True
        return lo < n.val < hi and is_bst(n.left, lo, n.val) and is_bst(n.right, n.val, hi)

    best = 0
    stack = [root] if root else []
    while stack:
        n = stack.pop()
        if is_bst(n):
            best = max(best, sum(vals(n)))
        stack.extend(c for c in (n.left, n.right) if c)
    return best


if __name__ == "__main__":
    import random

    cases = [
        ([1, 4, 3, 2, 4, 2, 5, None, None, None, None, None, None, 4, 6], 20),
        ([4, 3, None, 1, 2], 2),
        ([-4, -2, -5], 0),
        ([2, 1, 3], 6),
        ([5, 4, 8, 3, None, 6, 3], 7),
        ([1, None, 10, -5, 20], 25),
        ([7], 7),
        ([-7], 0),
        ([2, 2, 2], 2),                       # duplicates are not BST-valid
    ]
    for S in (Solution(), SolutionRecursive()):
        for arr, exp in cases:
            assert S.maxSumBST(build(arr)) == exp, (arr, exp)

    # deep skewed BST — iterative version must not hit recursion limit
    root = cur = TreeNode(0)
    for v in range(1, 40000):
        cur.right = TreeNode(v)
        cur = cur.right
    assert Solution().maxSumBST(root) == sum(range(40000))

    # randomized cross-check against brute force
    random.seed(1373)
    for _ in range(500):
        n = random.randint(1, 12)
        arr = [random.randint(-10, 10)] + [
            random.choice([None, random.randint(-10, 10)]) for _ in range(n)
        ]
        t = build(arr)
        exp = _brute(t)
        assert Solution().maxSumBST(t) == exp, arr
        assert SolutionRecursive().maxSumBST(t) == exp, arr

    print("All tests passed for 1373. Maximum Sum BST in Binary Tree")
