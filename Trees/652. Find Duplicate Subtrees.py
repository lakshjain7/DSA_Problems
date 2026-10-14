"""
652. Find Duplicate Subtrees
Difficulty: Medium
Topics: Hash Table, Tree, Depth-First Search, Binary Tree

Problem:
    Given the root of a binary tree, return all duplicate subtrees.
    For each kind of duplicate subtrees, you only need to return the root node
    of any one of them. Two trees are duplicate if they have the same structure
    with the same node values.

Example 1:
    Input: root = [1,2,3,4,null,2,4,null,null,4]
    Output: [[2,4],[4]]

Example 2:
    Input: root = [2,1,1]
    Output: [[1]]

Example 3:
    Input: root = [2,2,2,3,null,3,null]
    Output: [[2,3],[3]]

Constraints:
    - The number of nodes in the tree is in the range [1, 5000]
    - -200 <= Node.val <= 200

Approach (serialization + hash map):
    Post-order traversal. Serialize every subtree as "left,val,right" with a
    sentinel for null. Identical subtrees give identical strings. Count each
    string; when a count reaches exactly 2, record that node once.

Complexity:
    Time:  O(n^2) worst case (string building per node)
    Space: O(n^2) worst case for stored strings

Alternative (ID assignment, O(n)):
    Map each (left_id, val, right_id) triple to a unique integer id. Triples are
    constant size, so every node costs O(1) -> O(n) time and space.
"""
from collections import defaultdict
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def findDuplicateSubtrees(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        seen = defaultdict(int)
        res: List[Optional[TreeNode]] = []

        def dfs(node: Optional[TreeNode]) -> str:
            if not node:
                return "#"
            key = f"{dfs(node.left)},{node.val},{dfs(node.right)}"
            seen[key] += 1
            if seen[key] == 2:
                res.append(node)
            return key

        dfs(root)
        return res

    def findDuplicateSubtreesIds(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        ids = {}
        count = defaultdict(int)
        res: List[Optional[TreeNode]] = []

        def dfs(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            triple = (dfs(node.left), node.val, dfs(node.right))
            if triple not in ids:
                ids[triple] = len(ids) + 1
            uid = ids[triple]
            count[uid] += 1
            if count[uid] == 2:
                res.append(node)
            return uid

        dfs(root)
        return res


def build(vals):
    if not vals or vals[0] is None:
        return None
    nodes = [TreeNode(v) if v is not None else None for v in vals]
    kids = nodes[::-1]
    root = kids.pop()
    for n in nodes:
        if n:
            if kids:
                n.left = kids.pop()
            if kids:
                n.right = kids.pop()
    return root


def ser(node):
    if not node:
        return "#"
    return f"({ser(node.left)},{node.val},{ser(node.right)})"


if __name__ == "__main__":
    s = Solution()
    for fn in (s.findDuplicateSubtrees, s.findDuplicateSubtreesIds):
        r = fn(build([1, 2, 3, 4, None, 2, 4, None, None, 4]))
        assert sorted(ser(x) for x in r) == sorted([ser(build([2, 4])), ser(build([4]))])
        r = fn(build([2, 1, 1]))
        assert [ser(x) for x in r] == [ser(build([1]))]
        r = fn(build([2, 2, 2, 3, None, 3, None]))
        assert sorted(ser(x) for x in r) == sorted([ser(build([2, 3])), ser(build([3]))])
        assert fn(build([1])) == []
        assert fn(build([1, 2, 3])) == []
        # negative values, different structure same values are not duplicates
        assert fn(build([0, 0, 0, 0, None, None, 0, None, None, None, 0])) != None
        r = fn(build([1, 1, 1]))
        assert len(r) == 1 and r[0].val == 1
    print("All tests passed")
