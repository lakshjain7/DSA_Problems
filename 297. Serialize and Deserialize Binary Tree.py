"""
Problem 297 - Serialize and Deserialize Binary Tree
Difficulty: Hard
Topics: Trees, DFS, BFS, String, Design

Problem Statement:
Serialization is the process of converting a data structure or object into a
sequence of bits so that it can be stored in a file or transmitted across a
network link, and reconstructed later in the same or another computer
environment.

Design an algorithm to serialize and deserialize a binary tree. There is no
restriction on how your serialization/deserialization algorithm should work.
You just need to ensure that a binary tree can be serialized to a string and
this string can be deserialized to the original tree structure.

Example 1:
    Input: root = [1,2,3,null,null,4,5]
    Output: [1,2,3,null,null,4,5]

Example 2:
    Input: root = []
    Output: []

Constraints:
    The number of nodes in the tree is in the range [0, 10^4].
    -1000 <= Node.val <= 1000

Approach (DFS Preorder):
    Serialize:
        DFS preorder traversal -- record root value, then left subtree, then right.
        Use "null" for None nodes, commas as delimiters.
        Example: tree [1,2,3] -> "1,2,null,null,3,null,null"

    Deserialize:
        Split on commas, consume tokens left-to-right using an iterator.
        Reconstruct in the same preorder:
            - Read token -> if "null", return None
            - Create node with current value
            - Recurse for left child, then right child

    Preorder serialization is self-describing: no ambiguity about structure
    because null markers encode the exact shape of the tree.

Complexity:
    Time:  O(n) for both serialize and deserialize (visit each node once)
    Space: O(n) for the serialized string; O(h) recursion stack (h = height)
           Worst case O(n) stack space for a skewed tree.

Alternative Approach (BFS / Level-order):
    Serialize via BFS -- mirrors LeetCode's own tree representation.
    More intuitive to read, but requires tracking non-null nodes to know
    when to stop enqueueing children.
    Same O(n) time and space complexity.
"""
from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val: int = 0,
                 left: 'Optional[TreeNode]' = None,
                 right: 'Optional[TreeNode]' = None):
        self.val = val
        self.left = left
        self.right = right


# --------------------------------------------------------------------------- #
#  Primary approach: DFS preorder
# --------------------------------------------------------------------------- #

class Codec:
    """Serialize / deserialize using DFS preorder traversal."""

    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encode tree -> comma-separated preorder string."""
        parts: list = []

        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                parts.append("null")
                return
            parts.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(parts)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decode preorder string -> tree."""
        tokens = iter(data.split(","))

        def dfs() -> Optional[TreeNode]:
            val = next(tokens)
            if val == "null":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()


# --------------------------------------------------------------------------- #
#  Alternative approach: BFS level-order
# --------------------------------------------------------------------------- #

class CodecBFS:
    """Serialize / deserialize using BFS level-order traversal."""

    def serialize(self, root: Optional[TreeNode]) -> str:
        if not root:
            return ""
        parts: list = []
        queue: deque = deque([root])

        while queue:
            node = queue.popleft()
            if node is None:
                parts.append("null")
            else:
                parts.append(str(node.val))
                queue.append(node.left)   # enqueue even if None
                queue.append(node.right)

        # Trim trailing nulls (they carry no structural information)
        while parts and parts[-1] == "null":
            parts.pop()

        return ",".join(parts)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        if not data:
            return None
        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        queue: deque = deque([root])
        i = 1

        while queue and i < len(vals):
            node = queue.popleft()

            # Left child
            if i < len(vals) and vals[i] != "null":
                node.left = TreeNode(int(vals[i]))
                queue.append(node.left)
            i += 1

            # Right child
            if i < len(vals) and vals[i] != "null":
                node.right = TreeNode(int(vals[i]))
                queue.append(node.right)
            i += 1

        return root


# --------------------------------------------------------------------------- #
#  Helpers & tests
# --------------------------------------------------------------------------- #

def trees_equal(t1: Optional[TreeNode], t2: Optional[TreeNode]) -> bool:
    """Structural + value equality check for two trees."""
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    return (t1.val == t2.val
            and trees_equal(t1.left, t2.left)
            and trees_equal(t1.right, t2.right))


def build_tree(val: int,
               left: Optional[TreeNode] = None,
               right: Optional[TreeNode] = None) -> TreeNode:
    node = TreeNode(val)
    node.left = left
    node.right = right
    return node


if __name__ == "__main__":
    codec = Codec()
    codec_bfs = CodecBFS()

    # Test 1: [1,2,3,null,null,4,5]
    root = build_tree(1,
                      build_tree(2),
                      build_tree(3, build_tree(4), build_tree(5)))
    for c in (codec, codec_bfs):
        result = c.deserialize(c.serialize(root))
        assert trees_equal(root, result), f"Mismatch for codec {type(c).__name__}"

    # Test 2: empty tree
    for c in (codec, codec_bfs):
        assert c.deserialize(c.serialize(None)) is None

    # Test 3: single node
    single = TreeNode(42)
    for c in (codec, codec_bfs):
        assert trees_equal(single, c.deserialize(c.serialize(single)))

    # Test 4: left-skewed tree (worst-case recursion depth)
    left_skew = build_tree(1, build_tree(2, build_tree(3, build_tree(4))))
    for c in (codec, codec_bfs):
        assert trees_equal(left_skew, c.deserialize(c.serialize(left_skew)))

    # Test 5: right-skewed tree
    right_skew = build_tree(1, None, build_tree(2, None, build_tree(3)))
    for c in (codec, codec_bfs):
        assert trees_equal(right_skew, c.deserialize(c.serialize(right_skew)))

    # Test 6: negative values and value boundaries
    neg_tree = build_tree(-1000, build_tree(-500), build_tree(1000))
    for c in (codec, codec_bfs):
        assert trees_equal(neg_tree, c.deserialize(c.serialize(neg_tree)))

    # Test 7: full binary tree
    full = build_tree(1,
                      build_tree(2, build_tree(4), build_tree(5)),
                      build_tree(3, build_tree(6), build_tree(7)))
    for c in (codec, codec_bfs):
        assert trees_equal(full, c.deserialize(c.serialize(full)))

    print("All tests passed!")
