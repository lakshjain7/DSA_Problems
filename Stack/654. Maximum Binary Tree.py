"""
654. Maximum Binary Tree
Difficulty: Medium
Topics: Array, Stack, Monotonic Stack, Tree, Divide and Conquer, Binary Tree

Problem:
You are given an integer array nums with no duplicates. A maximum binary tree is built:
1. Create a root whose value is the maximum in nums.
2. Recursively build the left subtree from the subarray left of the maximum.
3. Recursively build the right subtree from the subarray right of the maximum.
Return the maximum binary tree built from nums.

Example 1:
    Input: nums = [3,2,1,6,0,5]
    Output: [6,3,5,null,2,0,null,null,1]
Example 2:
    Input: nums = [3,2,1]
    Output: [3,null,2,null,1]

Constraints:
    1 <= nums.length <= 1000
    0 <= nums[i] <= 1000
    All integers in nums are unique.

Approach (monotonic stack, O(n)):
Keep a stack of nodes with decreasing values (the current right spine). For each new
value, pop all smaller nodes; the last popped becomes the new node's left child (it is
the max of the elements between). If the stack is non-empty, the new node becomes the
right child of the stack top. Push the new node. The bottom of the stack is the root.

Complexity:
    Time:  O(n) - each element pushed/popped once
    Space: O(n)
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def constructMaximumBinaryTree(nums: List[int]) -> Optional[TreeNode]:
    stack: List[TreeNode] = []
    for x in nums:
        node = TreeNode(x)
        last = None
        while stack and stack[-1].val < x:
            last = stack.pop()
        node.left = last
        if stack:
            stack[-1].right = node
        stack.append(node)
    return stack[0] if stack else None


# Alternative: recursive divide and conquer, O(n^2) worst case.
def constructMaximumBinaryTree_recursive(nums: List[int]) -> Optional[TreeNode]:
    if not nums:
        return None
    i = nums.index(max(nums))
    return TreeNode(nums[i],
                    constructMaximumBinaryTree_recursive(nums[:i]),
                    constructMaximumBinaryTree_recursive(nums[i + 1:]))


def serialize(root: Optional[TreeNode]) -> list:
    out, q = [], [root]
    i = 0
    while i < len(q):
        n = q[i]
        i += 1
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    import random
    for f in (constructMaximumBinaryTree, constructMaximumBinaryTree_recursive):
        assert serialize(f([3, 2, 1, 6, 0, 5])) == [6, 3, 5, None, 2, 0, None, None, 1]
        assert serialize(f([3, 2, 1])) == [3, None, 2, None, 1]
        assert serialize(f([1])) == [1]
        assert serialize(f([1, 2, 3])) == [3, 2, None, 1]
        assert f([]) is None
    for _ in range(300):
        n = random.randint(1, 30)
        a = random.sample(range(0, 1001), n)
        assert serialize(constructMaximumBinaryTree(a)) == serialize(constructMaximumBinaryTree_recursive(a))
    print("All tests passed")
