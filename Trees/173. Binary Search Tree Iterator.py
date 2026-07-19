"""
173. Binary Search Tree Iterator
Difficulty: Medium
Topics: Stack, Tree, Design, Binary Search Tree, Binary Tree, Iterator

Problem Statement
-----------------
Implement the BSTIterator class that represents an iterator over the in-order
traversal of a binary search tree (BST):

- BSTIterator(TreeNode root) Initializes an object of the BSTIterator class. The
  root of the BST is given as part of the constructor. The pointer should be
  initialized to a non-existent number smaller than any element in the BST.
- boolean hasNext() Returns true if there exists a number in the traversal to the
  right of the pointer, otherwise returns false.
- int next() Moves the pointer to the right, then returns the number at the pointer.

Notice that by initializing the pointer to a non-existent smallest number, the
first call to next() will return the smallest element in the BST.

You may assume that next() calls will always be valid. That is, there will be at
least a next number in the in-order traversal when next() is called.

Example 1:
    Input:
        ["BSTIterator", "next", "next", "hasNext", "next", "hasNext",
         "next", "hasNext", "next", "hasNext"]
        [[[7, 3, 15, null, null, 9, 20]], [], [], [], [], [], [], [], [], []]
    Output:
        [null, 3, 7, true, 9, true, 15, true, 20, false]
    Explanation:
        BSTIterator bSTIterator = new BSTIterator([7, 3, 15, null, null, 9, 20]);
        bSTIterator.next();    // return 3
        bSTIterator.next();    // return 7
        bSTIterator.hasNext(); // return True
        bSTIterator.next();    // return 9
        bSTIterator.hasNext(); // return True
        bSTIterator.next();    // return 15
        bSTIterator.hasNext(); // return True
        bSTIterator.next();    // return 20
        bSTIterator.hasNext(); // return False

Constraints:
    - The number of nodes in the tree is in the range [1, 10^5].
    - 0 <= Node.val <= 10^6
    - At most 10^5 calls will be made to hasNext and next.

Follow-up:
    Could you implement next() and hasNext() to run in average O(1) time and use
    O(h) memory, where h is the height of the tree?


Approach: Controlled In-order Traversal with an Explicit Stack
--------------------------------------------------------------
A naive solution flattens the entire in-order traversal into a list in the
constructor, then serves elements one by one. That costs O(n) time up front and
O(n) memory, which violates the follow-up's O(h) memory goal.

Instead we simulate the recursion of an in-order traversal using an explicit
stack that stores only the "left spine" of the part of the tree we still need to
visit. In in-order traversal we always go as far left as possible, visit the node,
then move to its right subtree and repeat.

- In the constructor we push the entire left spine starting at the root.
- next(): the top of the stack is the smallest unvisited node. Pop it, and before
  returning its value, push the left spine of its right child (those nodes are the
  next-smallest values that come after it in-order).
- hasNext(): simply whether the stack is non-empty.

Why it works: the stack always holds exactly the ancestors (via left edges) of the
current smallest unvisited node, which is precisely the state an in-order recursion
would keep on its call stack. Each node is pushed once and popped once.

Complexity Analysis
-------------------
- Constructor: O(h) time and the stack holds at most h nodes.
- next(): amortized O(1). Although a single call may push a whole left spine, each
  node is pushed and popped exactly once across the life of the iterator, so N
  calls to next() do O(n) total work -> O(1) amortized each.
- hasNext(): O(1).
- Space: O(h) for the stack, where h is the tree height (O(n) worst case for a
  skewed tree, O(log n) for a balanced tree). This meets the follow-up requirement.
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


class BSTIterator:
    def __init__(self, root: Optional[TreeNode]) -> None:
        self.stack: List[TreeNode] = []
        self._push_left_spine(root)

    def _push_left_spine(self, node: Optional[TreeNode]) -> None:
        """Push node and all of its left descendants onto the stack."""
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        """Return the next smallest element in the in-order traversal."""
        node = self.stack.pop()
        # Everything smaller than node has been served; queue up node's right subtree.
        self._push_left_spine(node.right)
        return node.val

    def hasNext(self) -> bool:
        """Return True if there is a next element."""
        return len(self.stack) > 0


# ----------------------------------------------------------------------------
# Alternative approach: Flatten to a list in the constructor (O(n) memory).
# Simpler to reason about but does not meet the O(h) memory follow-up.
# ----------------------------------------------------------------------------
class BSTIteratorFlatten:
    def __init__(self, root: Optional[TreeNode]) -> None:
        self.values: List[int] = []
        self._inorder(root)
        self.index = 0

    def _inorder(self, node: Optional[TreeNode]) -> None:
        if not node:
            return
        self._inorder(node.left)
        self.values.append(node.val)
        self._inorder(node.right)

    def next(self) -> int:
        val = self.values[self.index]
        self.index += 1
        return val

    def hasNext(self) -> bool:
        return self.index < len(self.values)


def _build_bst_from_sorted(values: List[int]) -> Optional[TreeNode]:
    """Helper to build a balanced BST from a sorted list (for testing)."""
    if not values:
        return None
    mid = len(values) // 2
    root = TreeNode(values[mid])
    root.left = _build_bst_from_sorted(values[:mid])
    root.right = _build_bst_from_sorted(values[mid + 1:])
    return root


if __name__ == "__main__":
    # Example 1 from the problem statement.
    #        7
    #       / \
    #      3   15
    #         /  \
    #        9    20
    root = TreeNode(7,
                    TreeNode(3),
                    TreeNode(15, TreeNode(9), TreeNode(20)))
    it = BSTIterator(root)
    assert it.next() == 3
    assert it.next() == 7
    assert it.hasNext() is True
    assert it.next() == 9
    assert it.hasNext() is True
    assert it.next() == 15
    assert it.hasNext() is True
    assert it.next() == 20
    assert it.hasNext() is False

    # Single node.
    it = BSTIterator(TreeNode(42))
    assert it.hasNext() is True
    assert it.next() == 42
    assert it.hasNext() is False

    # Left-skewed tree: 3 -> 2 -> 1 (each node only has a left child).
    skewed = TreeNode(3, TreeNode(2, TreeNode(1)))
    it = BSTIterator(skewed)
    assert [it.next() for _ in range(3)] == [1, 2, 3]
    assert it.hasNext() is False

    # Larger balanced BST built from a sorted range; iterator must yield sorted order.
    ordered = list(range(0, 100))
    bst = _build_bst_from_sorted(ordered)
    it = BSTIterator(bst)
    out = []
    while it.hasNext():
        out.append(it.next())
    assert out == ordered

    # The flatten-based alternative must agree with the stack-based iterator.
    it2 = BSTIteratorFlatten(bst)
    out2 = []
    while it2.hasNext():
        out2.append(it2.next())
    assert out2 == ordered

    print("All tests passed for 173. Binary Search Tree Iterator")
