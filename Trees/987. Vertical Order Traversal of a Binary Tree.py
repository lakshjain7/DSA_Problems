"""
987. Vertical Order Traversal of a Binary Tree
Difficulty: Hard
Topics: Hash Table, Tree, Depth-First Search, Breadth-First Search,
        Binary Tree, Sorting

Problem Statement:
Given the root of a binary tree, calculate the vertical order traversal of
the binary tree.

For each node at position (row, col), its left and right children will be
at positions (row + 1, col - 1) and (row + 1, col + 1) respectively. The
root of the tree is at (0, 0).

The vertical order traversal of a binary tree is a list of top-to-bottom
orderings for each column index starting from the leftmost column and
ending on the rightmost column. There may be multiple nodes in the same
row and same column. In such a case:
  - Sort these nodes by their values.

Return the vertical order traversal of the binary tree.

Examples:
    Input: root = [3,9,20,null,null,15,7]
    Output: [[9],[3,15],[20],[7]]
    Explanation:
        Column -1: [9]
        Column  0: [3, 15]
        Column  1: [20]
        Column  2: [7]

    Input: root = [1,2,3,4,5,6,7]
    Output: [[4],[2],[1,5,6],[3],[7]]
    Explanation: Nodes 5 and 6 are both at row 2, column 0, so they are
    ordered by value: 5 before 6.

    Input: root = [1,2,3,4,6,5,7]
    Output: [[4],[2],[1,5,6],[3],[7]]
    Explanation: Nodes 5 and 6 are still ordered by value (5 before 6),
    even though 6 appears before 5 in the level-order input list.

Constraints:
    The number of nodes in the tree is in the range [1, 1000].
    0 <= Node.val <= 1000

Approach (DFS/BFS + Coordinate Sort):
Every node has a well-defined (row, col) coordinate derived from the root
at (0, 0). We traverse the whole tree (DFS or BFS both work) and record a
triple (col, row, val) for every node.

Once all triples are collected, we need to group nodes by column, and
within each column order them top-to-bottom (by row), and for ties on the
same (col, row), order by value ascending. This is exactly what sorting the
list of tuples (col, row, val) achieves directly, since tuple comparison in
Python compares element-by-element: first by col, then by row, then by
val.

After sorting, we walk through the sorted triples and group consecutive
entries that share the same col into the output sublists.

Why it works: the tuple-sort approach precisely encodes the three-level
ordering the problem demands (column ascending, then row ascending, then
value ascending) in a single sort, avoiding the classic bug of using a
plain dict-of-lists per column without handling the same-row tie-break by
value correctly.

Complexity:
    Time:  O(n log n) — n nodes visited once, dominated by sorting all
           (col, row, val) triples
    Space: O(n) — storing one triple per node, plus the recursion stack
           for DFS (O(h) where h is tree height)

Alternative Approach (BFS Level by Level with Per-Level Column Buckets):
Traverse the tree level by level with BFS. At each level, group node values
into buckets keyed by column. Because we process one full level at a time,
all nodes within a bucket for that level are already at the same row, so
we only need to sort each level's per-column bucket by value before merging
it into the global per-column result list (columns across levels are then
naturally already in top-to-bottom row order by construction).
"""

from collections import defaultdict, deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def vertical_traversal(root: Optional[TreeNode]) -> List[List[int]]:
    triples = []  # (col, row, val)

    def dfs(node: Optional[TreeNode], row: int, col: int) -> None:
        if node is None:
            return
        triples.append((col, row, node.val))
        dfs(node.left, row + 1, col - 1)
        dfs(node.right, row + 1, col + 1)

    dfs(root, 0, 0)
    triples.sort()  # sorts by (col, row, val) lexicographically

    result: List[List[int]] = []
    current_col = None
    for col, _row, val in triples:
        if col != current_col:
            result.append([])
            current_col = col
        result[-1].append(val)

    return result


def vertical_traversal_bfs(root: Optional[TreeNode]) -> List[List[int]]:
    """Alternative approach: BFS level by level, bucket by column per level."""
    if root is None:
        return []

    columns = defaultdict(list)  # col -> list of values, appended level by level
    queue = deque([(root, 0)])

    while queue:
        level_buckets = defaultdict(list)
        for _ in range(len(queue)):
            node, col = queue.popleft()
            level_buckets[col].append(node.val)
            if node.left:
                queue.append((node.left, col - 1))
            if node.right:
                queue.append((node.right, col + 1))

        for col, values in level_buckets.items():
            columns[col].extend(sorted(values))

    return [columns[col] for col in sorted(columns)]


def _build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Builds a binary tree from a level-order list (LeetCode style)."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    for fn in (vertical_traversal, vertical_traversal_bfs):
        # Example 1
        tree1 = _build_tree([3, 9, 20, None, None, 15, 7])
        assert fn(tree1) == [[9], [3, 15], [20], [7]]

        # Example 2
        tree2 = _build_tree([1, 2, 3, 4, 5, 6, 7])
        assert fn(tree2) == [[4], [2], [1, 5, 6], [3], [7]]

        # Example 3: same-column, same-row tie broken by value, not input order
        tree3 = _build_tree([1, 2, 3, 4, 6, 5, 7])
        assert fn(tree3) == [[4], [2], [1, 5, 6], [3], [7]]

        # Single node
        tree4 = _build_tree([1])
        assert fn(tree4) == [[1]]

        # Left-skewed tree
        tree5 = _build_tree([1, 2, None, 3, None, None, None])
        assert fn(tree5) == [[3], [2], [1]]

        # Right-skewed tree
        tree6 = _build_tree([1, None, 2, None, 3])
        assert fn(tree6) == [[1], [2], [3]]

    print("All test cases passed!")
