"""
863. All Nodes Distance K in Binary Tree
Difficulty: Medium
Topics: Tree, Depth-First Search, Breadth-First Search, Hash Table

Problem Statement
-----------------
Given the root of a binary tree, the value of a target node `target`, and an
integer `k`, return an array of the values of all nodes that have a distance
`k` from the target node.

The answer can be returned in any order. Distance is the number of edges on the
path between two nodes.

Examples
--------
Example 1:
    Input:  root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
    Output: [7, 4, 1]
    Explanation: The nodes at distance 2 from target (value 5) are the nodes
                 with values 7, 4, and 1.

Example 2:
    Input:  root = [1], target = 1, k = 3
    Output: []

Constraints
-----------
    The number of nodes in the tree is in the range [1, 500].
    0 <= Node.val <= 500
    All Node.val are unique.
    target is the value of one of the nodes in the tree.
    0 <= k <= 1000

Approach: Build Parent Pointers, then BFS
-----------------------------------------
In a binary tree we can only move downward (to children). Distance-k neighbors
of the target may also lie upward or across the tree, so we need to traverse in
all three directions: left child, right child, and parent.

Step 1 - Record parents: DFS/BFS once over the tree, storing for every node a
reference to its parent in a hash map. This effectively turns the rooted tree
into an undirected graph where each node connects to (left, right, parent).

Step 2 - BFS from target: starting at the target node, do a standard
breadth-first search that expands to left child, right child, and parent at each
step, using a visited set to avoid walking back. All nodes reached at exactly
level k are the answer.

Why it works: BFS explores the graph in order of increasing edge distance, so
every node popped while the frontier is at depth k is exactly distance k from
the target. Adding parent links makes upward movement possible, and the visited
set keeps each node counted once.

Complexity
----------
Time:  O(n) - each node is visited a constant number of times.
Space: O(n) - parent map, visited set, and BFS queue.

An alternative single-DFS solution (returning depth from target and folding in
downward searches on the way back up) is included below.
"""

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def distance_k(root: Optional[TreeNode], target: Optional[TreeNode],
               k: int) -> List[int]:
    """Parent-pointer + BFS. Returns values of all nodes k edges from target."""
    if root is None or target is None:
        return []

    # Step 1: map every node to its parent.
    parent = {root: None}
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)

    # Step 2: BFS outward from target across children and parent.
    visited = {target}
    queue = deque([target])
    dist = 0
    while queue:
        if dist == k:
            return [node.val for node in queue]
        for _ in range(len(queue)):
            node = queue.popleft()
            for nxt in (node.left, node.right, parent[node]):
                if nxt and nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        dist += 1
    return []


def distance_k_single_dfs(root: Optional[TreeNode], target: Optional[TreeNode],
                          k: int) -> List[int]:
    """Alternative: one DFS. Returns target's depth in each subtree and collects
    downward nodes when the target sits above the current node."""
    ans: List[int] = []

    def collect_down(node: Optional[TreeNode], dist: int) -> None:
        if node is None or dist < 0:
            return
        if dist == 0:
            ans.append(node.val)
            return
        collect_down(node.left, dist - 1)
        collect_down(node.right, dist - 1)

    def dfs(node: Optional[TreeNode]) -> int:
        # returns distance from `node` to target if target is in this subtree,
        # else -1.
        if node is None:
            return -1
        if node is target:
            collect_down(node, k)
            return 1
        left = dfs(node.left)
        if left != -1:
            if left == k:
                ans.append(node.val)
            else:
                collect_down(node.right, k - left - 1)
            return left + 1
        right = dfs(node.right)
        if right != -1:
            if right == k:
                ans.append(node.val)
            else:
                collect_down(node.left, k - right - 1)
            return right + 1
        return -1

    dfs(root)
    return ans


def _build(values, index_of_target):
    """Build a tree from a LeetCode-style level-order list (None for missing).
    Returns (root, target_node)."""
    if not values:
        return None, None
    nodes = [TreeNode(v) if v is not None else None for v in values]
    kids = iter(nodes[1:])
    for node in nodes:
        if node is None:
            continue
        left = next(kids, None)
        right = next(kids, None)
        node.left = left
        node.right = right
    target = nodes[index_of_target]
    return nodes[0], target


if __name__ == "__main__":
    # Example 1: root = [3,5,1,6,2,0,8,null,null,7,4], target value 5, k = 2
    values = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
    root, target = _build(values, index_of_target=1)  # node with value 5
    assert target.val == 5
    got = sorted(distance_k(root, target, 2))
    assert got == [1, 4, 7], f"example1 got {got}"
    assert sorted(distance_k_single_dfs(root, target, 2)) == [1, 4, 7]

    # k = 0 returns the target itself.
    assert distance_k(root, target, 0) == [5]
    assert distance_k_single_dfs(root, target, 0) == [5]

    # k = 1 neighbors of value-5 node: parent 3, children 6 and 2.
    assert sorted(distance_k(root, target, 1)) == [2, 3, 6]
    assert sorted(distance_k_single_dfs(root, target, 1)) == [2, 3, 6]

    # Single node tree, k = 3 -> nothing.
    single_root, single_target = _build([1], 0)
    assert distance_k(single_root, single_target, 3) == []
    assert distance_k_single_dfs(single_root, single_target, 3) == []

    # Distance larger than tree height -> empty.
    assert distance_k(root, target, 10) == []
    assert distance_k_single_dfs(root, target, 10) == []

    # Target at the root.
    root2, target2 = _build(values, index_of_target=0)  # value 3
    assert sorted(distance_k(root2, target2, 1)) == [1, 5]
    assert sorted(distance_k_single_dfs(root2, target2, 1)) == [1, 5]

    print("All tests passed for 863. All Nodes Distance K in Binary Tree")
