"""
2458. Height of Binary Tree After Subtree Removal Queries
Difficulty: Hard
Topics: Array, Tree, Depth-First Search, Breadth-First Search, Binary Tree

Problem:
You are given the root of a binary tree with n nodes. Each node is assigned a
unique value from 1 to n. You are also given an array `queries` of size m.

You have to perform m independent queries on the tree where in the i-th query
you do the following:
    - Remove the subtree rooted at the node with the value queries[i] from the
      tree. It is guaranteed that queries[i] will not be equal to the value of
      the root.

Return an array `answer` of size m where answer[i] is the height of the tree
after performing the i-th query.

Note:
    - The queries are independent, so the tree returns to its initial state
      after each query.
    - The height of a tree is the number of edges in the longest simple path
      from the root to some node in the tree.

Example 1:
    Input: root = [1,3,4,2,null,6,5,null,null,null,null,null,7], queries = [4]
    Output: [2]
    Explanation: Removing the subtree rooted at 4 leaves the path 1 -> 3 -> 2
    of length 2.

Example 2:
    Input: root = [5,8,9,2,1,3,7,4,6], queries = [3,2,4,8]
    Output: [3,2,3,2]
    Explanation:
    - Removing 3: height stays 3 (path 5 -> 8 -> 2 -> 4).
    - Removing 2: height becomes 2 (path 5 -> 8 -> 1).
    - Removing 4: height stays 3 (path 5 -> 8 -> 2 -> 6).
    - Removing 8: height becomes 2 (path 5 -> 9 -> 3).

Constraints:
    The number of nodes in the tree is n.
    2 <= n <= 10^5
    1 <= Node.val <= n
    All the values in the tree are unique.
    m == queries.length
    1 <= m <= min(n, 10^4)
    1 <= queries[i] <= n
    queries[i] != root.val

Approach (Two DFS passes — "best height without me"):
    1. Post-order: compute height[v] = edges in the longest downward path
       from v.
    2. Pre-order: carry `rest` = the tallest the tree can be using only
       nodes OUTSIDE the current subtree. For node v at depth d with
       children L and R:
           ans[L] = max(rest_v, d + 1 + height[R])   (R missing -> -inf)
           ans[R] = max(rest_v, d + 1 + height[L])
       i.e. removing L leaves everything outside v, plus v itself and the
       path down through its sibling R. Note that v itself (depth d) is
       always kept, so ans includes d as well.
    Every query is then answered in O(1) via a lookup table.

    Implemented iteratively to avoid Python recursion limits on skewed trees
    (n up to 1e5).

Complexity:
    Time:  O(n + m) — two linear traversals plus constant-time queries.
    Space: O(n) for heights, answers and the explicit stack.

Alternative (Euler tour / depth array with prefix & suffix max):
    Record nodes in DFS order with their depths; the subtree of v occupies a
    contiguous range [tin[v], tout[v]]. Answer = max(prefix_max[tin-1],
    suffix_max[tout+1]). Same O(n + m) complexity.
"""

from collections import deque
from typing import Dict, List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def tree_queries(root: Optional[TreeNode], queries: List[int]) -> List[int]:
    if root is None:
        return []

    # Pass 1: iterative post-order to compute heights
    height: Dict[int, int] = {}
    stack = [(root, False)]
    while stack:
        node, done = stack.pop()
        if done:
            lh = height[node.left.val] if node.left else -1
            rh = height[node.right.val] if node.right else -1
            height[node.val] = 1 + max(lh, rh)
        else:
            stack.append((node, True))
            if node.left:
                stack.append((node.left, False))
            if node.right:
                stack.append((node.right, False))

    # Pass 2: pre-order carrying best height outside the subtree
    ans: Dict[int, int] = {}
    stack2 = [(root, 0, 0)]  # node, depth, best height excluding this subtree's descendants
    while stack2:
        node, depth, rest = stack2.pop()
        lh = height[node.left.val] if node.left else -1
        rh = height[node.right.val] if node.right else -1
        if node.left:
            # Removing left child: keep rest, node itself, and right branch
            without_left = max(rest, depth, depth + 1 + rh if node.right else depth)
            ans[node.left.val] = without_left
            stack2.append((node.left, depth + 1, max(rest, depth + 1 + rh if node.right else depth)))
        if node.right:
            without_right = max(rest, depth, depth + 1 + lh if node.left else depth)
            ans[node.right.val] = without_right
            stack2.append((node.right, depth + 1, max(rest, depth + 1 + lh if node.left else depth)))

    return [ans[q] for q in queries]


def tree_queries_euler(root: Optional[TreeNode], queries: List[int]) -> List[int]:
    order_depth: List[int] = []
    tin: Dict[int, int] = {}
    tout: Dict[int, int] = {}
    stack = [(root, 0, False)]
    while stack:
        node, d, done = stack.pop()
        if done:
            tout[node.val] = len(order_depth) - 1
            continue
        tin[node.val] = len(order_depth)
        order_depth.append(d)
        stack.append((node, d, True))
        if node.right:
            stack.append((node.right, d + 1, False))
        if node.left:
            stack.append((node.left, d + 1, False))

    n = len(order_depth)
    pre = [0] * n
    suf = [0] * n
    for i in range(n):
        pre[i] = max(order_depth[i], pre[i - 1] if i else 0)
    for i in range(n - 1, -1, -1):
        suf[i] = max(order_depth[i], suf[i + 1] if i + 1 < n else 0)

    res = []
    for q in queries:
        l, r = tin[q], tout[q]
        best = pre[l - 1] if l > 0 else 0
        if r + 1 < n:
            best = max(best, suf[r + 1])
        res.append(best)
    return res


def build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    import random

    for fn in (tree_queries, tree_queries_euler):
        r1 = build_tree([1, 3, 4, 2, None, 6, 5, None, None, None, None, None, 7])
        assert fn(r1, [4]) == [2]

        r2 = build_tree([5, 8, 9, 2, 1, 3, 7, 4, 6])
        assert fn(r2, [3, 2, 4, 8]) == [3, 2, 3, 2]

        # Two nodes: removing the only child leaves height 0
        assert fn(build_tree([1, 2]), [2]) == [0]

        # Left-skewed chain 1->2->3->4->5
        chain = TreeNode(1)
        cur = chain
        for v in range(2, 6):
            cur.left = TreeNode(v)
            cur = cur.left
        assert fn(chain, [2, 3, 4, 5]) == [0, 1, 2, 3]

        # Deep skewed tree (no recursion-limit crash)
        deep = TreeNode(1)
        cur = deep
        for v in range(2, 50001):
            cur.right = TreeNode(v)
            cur = cur.right
        assert fn(deep, [2, 50000]) == [0, 49998]

    # Randomised cross-check against brute force
    def brute(root, q):
        def h(node, d):
            if node is None or node.val == q:
                return -1
            return max(d, h(node.left, d + 1), h(node.right, d + 1))
        return h(root, 0)

    for _ in range(200):
        n = random.randint(2, 15)
        nodes = [TreeNode(i) for i in range(1, n + 1)]
        for i in range(1, n):
            while True:
                p = random.choice(nodes[:i])
                side = random.choice(("left", "right"))
                if getattr(p, side) is None:
                    setattr(p, side, nodes[i])
                    break
        qs = list(range(2, n + 1))
        exp = [brute(nodes[0], q) for q in qs]
        assert tree_queries(nodes[0], qs) == exp
        assert tree_queries_euler(nodes[0], qs) == exp

    print("All tests passed for 2458. Height of Binary Tree After Subtree Removal Queries")
