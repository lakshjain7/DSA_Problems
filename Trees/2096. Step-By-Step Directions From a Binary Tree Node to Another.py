"""
2096. Step-By-Step Directions From a Binary Tree Node to Another
Difficulty: Medium
Topics: String, Tree, Depth-First Search, Binary Tree, Lowest Common Ancestor

Problem:
You are given the root of a binary tree with n nodes. Each node is uniquely
assigned a value from 1 to n. You are also given an integer startValue
representing the value of the start node s, and a different integer destValue
representing the value of the destination node t.

Find the shortest path starting from node s and ending at node t. Generate
step-by-step directions of such path as a string consisting of only the
uppercase letters 'L', 'R', and 'U'. Each letter indicates a specific direction:
    'L' means to go from a node to its left child node.
    'R' means to go from a node to its right child node.
    'U' means to go from a node to its parent node.
Return the step-by-step directions of the shortest path from node s to node t.

Example 1:
    Input: root = [5,1,2,3,null,6,4], startValue = 3, destValue = 6
    Output: "UURL"
    Explanation: The shortest path is: 3 -> 1 -> 5 -> 2 -> 6.

Example 2:
    Input: root = [2,1], startValue = 2, destValue = 1
    Output: "L"
    Explanation: The shortest path is: 2 -> 1.

Constraints:
    The number of nodes in the tree is n.
    2 <= n <= 10^5
    1 <= Node.val <= n
    All the values in the tree are unique.
    1 <= startValue, destValue <= n
    startValue != destValue

Approach (Root paths + strip common prefix = implicit LCA):
    Record the L/R path from the root to start and from the root to dest.
    Both paths share a common prefix — exactly the path from the root to the
    lowest common ancestor. Strip that prefix. What remains of start's path is
    the number of steps to climb up ('U' each); what remains of dest's path is
    the exact L/R descent from the LCA. Answer = 'U' * len(rest_s) + rest_d.

    Path finding uses an iterative DFS (n up to 1e5 would blow Python's
    recursion limit on a skewed tree).

Complexity:
    Time:  O(n) — each path search visits each node at most once.
    Space: O(n) — explicit stack and path strings (O(h) on balanced trees).
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def _path_from_root(root: TreeNode, target: int) -> str:
    """Iterative DFS returning the L/R path from root to target."""
    path: List[str] = []
    # stack entries: (node, direction taken to reach it, depth)
    stack = [(root, "", 0)]
    while stack:
        node, d, depth = stack.pop()
        del path[max(depth - 1, 0):]
        if depth:
            path.append(d)
        if node.val == target:
            return "".join(path)
        if node.right:
            stack.append((node.right, "R", depth + 1))
        if node.left:
            stack.append((node.left, "L", depth + 1))
    return ""


def get_directions(root: Optional[TreeNode], start_value: int, dest_value: int) -> str:
    ps = _path_from_root(root, start_value)
    pd = _path_from_root(root, dest_value)
    i = 0
    while i < len(ps) and i < len(pd) and ps[i] == pd[i]:
        i += 1
    return "U" * (len(ps) - i) + pd[i:]


def get_directions_parent_bfs(root: Optional[TreeNode], start_value: int,
                              dest_value: int) -> str:
    """
    Alternative: treat the tree as an undirected graph (add parent links) and
    BFS from start, remembering for each node the (prev, move) that reached it.
    Reconstruct by backtracking from dest. Also O(n) time/space, but uses more
    memory and constant factor than the prefix-stripping method.
    """
    from collections import deque
    parent = {root.val: None}
    nodes = {root.val: root}
    stack = [root]
    while stack:
        n = stack.pop()
        for c in (n.left, n.right):
            if c:
                parent[c.val] = n
                nodes[c.val] = c
                stack.append(c)
    came = {start_value: (None, "")}
    q = deque([nodes[start_value]])
    while q:
        n = q.popleft()
        if n.val == dest_value:
            break
        for nxt, mv in ((n.left, "L"), (n.right, "R"), (parent[n.val], "U")):
            if nxt and nxt.val not in came:
                came[nxt.val] = (n.val, mv)
                q.append(nxt)
    out = []
    cur = dest_value
    while came[cur][0] is not None:
        prev, mv = came[cur]
        out.append(mv)
        cur = prev
    return "".join(reversed(out))


def build(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from LeetCode level-order list."""
    if not values or values[0] is None:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    q = [root]
    i = 0
    for v in it:
        parent = q[i // 2]
        node = TreeNode(v) if v is not None else None
        if i % 2 == 0:
            parent.left = node
        else:
            parent.right = node
        if node:
            q.append(node)
        i += 1
    return root


if __name__ == "__main__":
    for fn in (get_directions, get_directions_parent_bfs):
        t = build([5, 1, 2, 3, None, 6, 4])
        assert fn(t, 3, 6) == "UURL"
        assert fn(t, 6, 3) == "UULL"
        assert fn(t, 5, 4) == "RR"
        assert fn(t, 4, 5) == "UU"
        assert fn(t, 6, 4) == "UR"
        assert fn(build([2, 1]), 2, 1) == "L"
        assert fn(build([2, 1]), 1, 2) == "U"
        assert fn(build([1, None, 2, None, 3]), 1, 3) == "RR"

    # deep skewed tree: make sure no recursion-limit issues
    n = 100000
    root = TreeNode(1)
    cur = root
    for v in range(2, n + 1):
        cur.left = TreeNode(v)
        cur = cur.left
    assert get_directions(root, n, 1) == "U" * (n - 1)
    assert get_directions(root, 1, n) == "L" * (n - 1)

    # random cross-check
    import random
    random.seed(2096)
    for _ in range(300):
        size = random.randint(2, 30)
        vals = list(range(1, size + 1))
        random.shuffle(vals)
        r = TreeNode(vals[0])
        all_nodes = [r]
        for v in vals[1:]:
            while True:
                p = random.choice(all_nodes)
                side = random.choice("LR")
                if side == "L" and p.left is None:
                    p.left = TreeNode(v); all_nodes.append(p.left); break
                if side == "R" and p.right is None:
                    p.right = TreeNode(v); all_nodes.append(p.right); break
        s, d = random.sample(vals, 2)
        assert get_directions(r, s, d) == get_directions_parent_bfs(r, s, d), (s, d)
    print("All tests passed for 2096. Step-By-Step Directions From a Binary Tree Node to Another")
