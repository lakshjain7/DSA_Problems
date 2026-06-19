"""
Problem 297 - Serialize and Deserialize Binary Tree
Difficulty: Hard
Topics: Trees, DFS, BFS, String, Design

Design an algorithm to serialize and deserialize a binary tree.

Approach (DFS Preorder):
    Serialize: DFS preorder, "null" for None nodes, comma-delimited.
    Deserialize: Split on commas, consume tokens with iterator in preorder.

Complexity: O(n) time, O(n) space for both operations.

Alternative: BFS level-order (also shown below).
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


class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
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


class CodecBFS:
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
                queue.append(node.left)
                queue.append(node.right)
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
            if i < len(vals) and vals[i] != "null":
                node.left = TreeNode(int(vals[i]))
                queue.append(node.left)
            i += 1
            if i < len(vals) and vals[i] != "null":
                node.right = TreeNode(int(vals[i]))
                queue.append(node.right)
            i += 1
        return root


def trees_equal(t1, t2):
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    return t1.val == t2.val and trees_equal(t1.left, t2.left) and trees_equal(t1.right, t2.right)


if __name__ == "__main__":
    def bt(val, left=None, right=None):
        n = TreeNode(val); n.left = left; n.right = right; return n
    codec = Codec()
    codec_bfs = CodecBFS()
    root = bt(1, bt(2), bt(3, bt(4), bt(5)))
    for c in (codec, codec_bfs):
        assert trees_equal(root, c.deserialize(c.serialize(root)))
        assert c.deserialize(c.serialize(None)) is None
        assert trees_equal(TreeNode(42), c.deserialize(c.serialize(TreeNode(42))))
    print("All tests passed!")
