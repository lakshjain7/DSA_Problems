"""
236. Lowest Common Ancestor of a Binary Tree
Difficulty: Medium
Topics: Tree, Depth-First Search, Binary Tree

Problem Statement:
------------------
Given a binary tree, find the lowest common ancestor (LCA) of two given
nodes `p` and `q` in the tree.

According to the definition of LCA on Wikipedia: "The lowest common
ancestor is defined between two nodes p and q as the lowest node in T
that has both p and q as descendants (where we allow a node to be a
descendant of itself)."

Examples:
---------
Example 1:
    Input: root = [3,5,1,6,2,0,8,None,None,7,4], p = 5, q = 1
    Output: 3
    Explanation: The LCA of nodes 5 and 1 is 3.

Example 2:
    Input: root = [3,5,1,6,2,0,8,None,None,7,4], p = 5, q = 4
    Output: 5
    Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a
    descendant of itself according to the LCA definition.

Example 3:
    Input: root = [1,2], p = 1, q = 2
    Output: 1

Constraints:
-------------
- The number of nodes in the tree is in the range [2, 10^5].
- -10^9 <= Node.val <= 10^9
- All Node.val are unique.
- p != q
- p and q will exist in the tree.

Approach:
---------
Approach 1 - Recursive postorder search (implemented as the primary
solution):
    Recurse into the left and right subtrees looking for p or q.
    - If the current node is None, or equals p or q, return the current
      node (a node is its own ancestor, and None propagates "not found").
    - Recurse left and right.
    - If both the left and right recursive calls return a non-null node,
      it means p and q were found in different subtrees, so the current
      node is their LCA -> return current node.
    - Otherwise, return whichever side returned a non-null result (that
      side contains both p and q, or just one of them "on the way up").
    This works because the first node at which the search paths for p and
    q diverge (or one of them equals the node itself) is exactly the LCA.

Approach 2 (alternative) - Parent pointers + ancestor path:
    Do a DFS/BFS building a `child -> parent` map for every node. Then
    walk up from `p` to the root, collecting the set of ancestors of p.
    Walk up from `q` towards the root, and the first ancestor we hit that
    is also in p's ancestor set is the LCA. This mirrors how you would
    find the intersection point of two linked lists.

Complexity Analysis:
---------------------
Approach 1 (recursive):
    Time:  O(n) - each node is visited at most once.
    Space: O(h) - recursion stack, where h is the height of the tree
           (O(n) worst case for a skewed tree, O(log n) for balanced).

Approach 2 (parent pointers):
    Time:  O(n) - one pass to build parent map, O(h) to walk up twice.
    Space: O(n) - the parent map stores an entry for every node.
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(
    root: Optional["TreeNode"], p: "TreeNode", q: "TreeNode"
) -> Optional["TreeNode"]:
    """Return the LCA of nodes p and q in the binary tree rooted at root."""
    if root is None or root is p or root is q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left is not None and right is not None:
        # p and q were found in different subtrees -> root is the LCA.
        return root

    # Either both None (not found on this side) or one side has the answer.
    return left if left is not None else right


def lowest_common_ancestor_parent_pointers(
    root: Optional["TreeNode"], p: "TreeNode", q: "TreeNode"
) -> Optional["TreeNode"]:
    """Alternative approach using explicit parent pointers (iterative)."""
    parent = {root: None}
    stack = [root]

    # Build parent map with an iterative DFS until both p and q are found.
    while p not in parent or q not in parent:
        node = stack.pop()
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        if node.right:
            parent[node.right] = node
            stack.append(node.right)

    # Collect all ancestors of p (including p itself).
    ancestors_of_p = set()
    node = p
    while node is not None:
        ancestors_of_p.add(node)
        node = parent[node]

    # Walk up from q until we hit a common ancestor.
    node = q
    while node not in ancestors_of_p:
        node = parent[node]

    return node


if __name__ == "__main__":
    # Build tree: [3,5,1,6,2,0,8,None,None,7,4]
    n7 = TreeNode(7)
    n4 = TreeNode(4)
    n6 = TreeNode(6)
    n2 = TreeNode(2, n7, n4)
    n0 = TreeNode(0)
    n8 = TreeNode(8)
    n5 = TreeNode(5, n6, n2)
    n1 = TreeNode(1, n0, n8)
    root = TreeNode(3, n5, n1)

    # Example 1: LCA(5, 1) == 3
    assert lowest_common_ancestor(root, n5, n1) is root
    assert lowest_common_ancestor_parent_pointers(root, n5, n1) is root

    # Example 2: LCA(5, 4) == 5 (node can be its own ancestor)
    assert lowest_common_ancestor(root, n5, n4) is n5
    assert lowest_common_ancestor_parent_pointers(root, n5, n4) is n5

    # Example 3: two-node tree [1,2]
    small_root = TreeNode(1)
    small_child = TreeNode(2)
    small_root.left = small_child
    assert lowest_common_ancestor(small_root, small_root, small_child) is small_root
    assert (
        lowest_common_ancestor_parent_pointers(small_root, small_root, small_child)
        is small_root
    )

    # Deep nested case: LCA(7, 4) should be node 2
    assert lowest_common_ancestor(root, n7, n4) is n2
    assert lowest_common_ancestor_parent_pointers(root, n7, n4) is n2

    # LCA(6, 2) should be node 5 (grandparent case)
    assert lowest_common_ancestor(root, n6, n2) is n5

    # LCA of a node and its direct child: LCA(1, 8) should be node 1
    assert lowest_common_ancestor(root, n1, n8) is n1

    # LCA(0, 8) should be node 1 (siblings)
    assert lowest_common_ancestor(root, n0, n8) is n1

    print("All tests passed!")
