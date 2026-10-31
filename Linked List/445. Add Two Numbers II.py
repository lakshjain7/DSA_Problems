"""
445. Add Two Numbers II
Difficulty: Medium
Topics: Linked List, Math, Stack

You are given two non-empty linked lists representing two non-negative
integers. The most significant digit comes first and each node contains a
single digit. Add the two numbers and return the sum as a linked list.
You may assume the two numbers do not contain any leading zero, except the
number 0 itself.

Example 1:
    Input: l1 = [7,2,4,3], l2 = [5,6,4]
    Output: [7,8,0,7]
Example 2:
    Input: l1 = [2,4,3], l2 = [5,6,4]
    Output: [8,0,7]
Example 3:
    Input: l1 = [0], l2 = [0]
    Output: [0]

Constraints:
    The number of nodes in each list is in the range [1, 100].
    0 <= Node.val <= 9
    Follow up: solve without reversing the input lists.

Approach (two stacks):
    Addition happens from the least significant digit, but lists are stored
    from the most significant. Push all digits of each list onto stacks, then
    pop together, adding with a carry. Each new digit node is prepended to the
    result, so the result ends in the correct order without reversing inputs.

Complexity:
    Time:  O(m + n)
    Space: O(m + n) for stacks

Alternative: reverse both lists, add, reverse the result (O(1) extra space,
but modifies the inputs).
"""
from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        s1, s2 = [], []
        while l1:
            s1.append(l1.val)
            l1 = l1.next
        while l2:
            s2.append(l2.val)
            l2 = l2.next
        head, carry = None, 0
        while s1 or s2 or carry:
            total = carry
            if s1:
                total += s1.pop()
            if s2:
                total += s2.pop()
            carry, digit = divmod(total, 10)
            head = ListNode(digit, head)
        return head

    def addTwoNumbersReverse(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def rev(node):
            prev = None
            while node:
                node.next, prev, node = prev, node, node.next
            return prev

        a, b = rev(l1), rev(l2)
        dummy = cur = ListNode()
        carry = 0
        while a or b or carry:
            total = carry + (a.val if a else 0) + (b.val if b else 0)
            carry, digit = divmod(total, 10)
            cur.next = ListNode(digit)
            cur = cur.next
            a = a.next if a else None
            b = b.next if b else None
        return rev(dummy.next)


def build(arr: List[int]) -> Optional[ListNode]:
    dummy = cur = ListNode()
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(node: Optional[ListNode]) -> List[int]:
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


if __name__ == "__main__":
    s = Solution()
    for f in (s.addTwoNumbers, s.addTwoNumbersReverse):
        assert to_list(f(build([7,2,4,3]), build([5,6,4]))) == [7,8,0,7]
        assert to_list(f(build([2,4,3]), build([5,6,4]))) == [8,0,7]
        assert to_list(f(build([0]), build([0]))) == [0]
        assert to_list(f(build([9,9,9]), build([1]))) == [1,0,0,0]
        assert to_list(f(build([5]), build([5]))) == [1,0]
    print("All tests passed")
