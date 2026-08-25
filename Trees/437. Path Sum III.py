"""
437. Path Sum III
Difficulty: Medium
Topics: Trees, Depth-First Search, Prefix Sum, Hash Map, Binary Tree

Problem Statement
-----------------
Given the root of a binary tree and an integer targetSum, return the number of
paths where the sum of the values along the path equals targetSum.

The path does not need to start or end at the root or a leaf, but it must go
downwards (i.e., traveling only from parent nodes to child nodes).

Examples
--------
Example 1:
    Input: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
    Output: 3
    Explanation: The paths that sum to 8 are:
        5 -> 3
        5 -> 2 -> 1
        -3 -> 11

Example 2:
    Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
    Output: 3

Constraints
-----------
- The number of nodes in the tree is in the range [0, 1000].
- -10^9 <= Node.val <= 10^9
- -1000 <= targetSum <= 1000

Approach (Prefix Sum + Hash Map)
--------------------------------
This is the tree analogue of the classic "Subarray Sum Equals K" (LeetCode 560)
technique.

As we DFS down from the root, we keep a running sum `curr` of node values along
the current root-to-node path. A downward path that ends at the current node and
sums to `targetSum` corresponds to some earlier ancestor whose prefix sum was
`curr - targetSum`. If we have counted how many ancestors on the current path
had each prefix-sum value, then the number of valid paths ending at this node is
exactly `prefix[curr - targetSum]`.

We maintain a hash map `prefix` mapping prefix-sum value -> count of ancestors
(including a virtual empty prefix of 0, so that paths starting at the root are
counted). On entering a node we add its contribution, recurse into children,
then remove its contribution on the way back up (backtracking) so counts stay
consistent for sibling subtrees.

Why it works
------------
Every downward path is uniquely identified by its deepest node and its shallowest
node. Fixing the deepest node = current node, a path summing to targetSum exists
for each ancestor prefix equal to curr - targetSum. Summing over all deepest
nodes counts every qualifying path exactly once.

Complexity
----------
Time:  O(n) - each node is visited once, and hash map operations are O(1) average.
Space: O(n) - the prefix map and recursion stack are bounded by the tree height,
       up to O(n) in the worst case (skewed tree).

Alternative Approach (Brute Force, O(n^2))
------------------------------------------
For each node, treat it as the start of a path and DFS downward counting all
paths that sum to targetSum. This is simpler but O(n^2) in the worst case (or
O(n log n) for a balanced tree). Included below as `path_sum_bruteforce`.
"""

from collections import defaultdict
from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


def path_sum(root: Optional[TreeNode], target_sum: int) -> int:
    """Prefix-sum + hash map solution. O(n) time."""
    prefix = defaultdict(int)
    prefix[0] = 1  # virtual empty prefix so root-starting paths are counted

    def dfs(node: Optional[TreeNode], curr: int) -> int:
        if node is None:
            return 0
        curr += node.val
        count = prefix[curr - target_sum]
        prefix[curr] += 1
        count += dfs(node.left, curr)
        count += dfs(node.right, curr)
        prefix[curr] -= 1  # backtrack
        return count

    return dfs(root, 0)


def path_sum_bruteforce(root: Optional[TreeNode], target_sum: int) -> int:
    """Brute force: try every node as a path start. O(n^2) time."""
    def count_from(node: Optional[TreeNode], remaining: int) -> int:
        if node is None:
            return 0
        remaining -= node.val
        found = 1 if remaining == 0 else 0
        return (found
                + count_from(node.left, remaining)
                + count_from(node.right, remaining))

    if root is None:
        return 0
    return (count_from(root, target_sum)
            + path_sum_bruteforce(root.left, target_sum)
            + path_sum_bruteforce(root.right, target_sum))


def build_tree(values: list) -> Optional[TreeNode]:
    """Build a binary tree from a level-order list with None placeholders."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values):
            if values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


if __name__ == "__main__":
    # Example 1
    t1 = build_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1])
    assert path_sum(t1, 8) == 3
    assert path_sum_bruteforce(t1, 8) == 3

    # Example 2
    t2 = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
    assert path_sum(t2, 22) == 3
    assert path_sum_bruteforce(t2, 22) == 3

    # Empty tree
    assert path_sum(None, 0) == 0
    assert path_sum_bruteforce(None, 0) == 0

    # Single node equal to target
    assert path_sum(build_tree([5]), 5) == 1
    assert path_sum(build_tree([5]), 4) == 0

    # Single node, negative target
    assert path_sum(build_tree([-3]), -3) == 1

    # Tree of zeros: 0 -> 0, 0
    # paths summing to 0: each single node (3) + root->left + root->right = 5
    t3 = build_tree([0, 0, 0])
    assert path_sum(t3, 0) == 5
    assert path_sum_bruteforce(t3, 0) == 5

    # Straight chain 1 -> 2 -> 3 -> 4 (each node's left child is next value)
    line = build_tree([1, 2, None, 3, None, 4])
    assert path_sum(line, 6) == 1    # 1+2+3
    assert path_sum(line, 9) == 1    # 2+3+4
    assert path_sum(line, 10) == 1   # 1+2+3+4
    # sums equal to 3 along chain: [1,2] and [3] => 2 paths
    assert path_sum(line, 3) == 2
    assert path_sum_bruteforce(line, 3) == 2

    print("All tests passed for 437. Path Sum III")
