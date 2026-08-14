"""
LeetCode 2. Add Two Numbers
Difficulty: Medium
Topics: Linked List, Math, Recursion

Problem Statement:
    You are given two non-empty linked lists representing two non-negative
    integers. The digits are stored in reverse order, and each of their nodes
    contains a single digit. Add the two numbers and return the sum as a
    linked list.

    You may assume the two numbers do not contain any leading zero, except the
    number 0 itself.

Examples:
    Example 1:
        Input:  l1 = [2,4,3], l2 = [5,6,4]
        Output: [7,0,8]
        Explanation: 342 + 465 = 807.

    Example 2:
        Input:  l1 = [0], l2 = [0]
        Output: [0]

    Example 3:
        Input:  l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
        Output: [8,9,9,9,0,0,0,1]
        Explanation: 9999999 + 9999 = 10009998.

Constraints:
    - The number of nodes in each linked list is in the range [1, 100].
    - 0 <= Node.val <= 9
    - It is guaranteed that the list represents a number that does not have
      leading zeros.

Approach:
    Because digits are stored in reverse order, the head of each list holds the
    least significant digit. This lines up perfectly with grade-school
    addition: we walk both lists from head to tail (i.e. from ones place
    upward), adding corresponding digits plus any carry from the previous
    position.

    At each step:
        total = val1 + val2 + carry
        new_digit = total % 10
        carry     = total // 10

    We append new_digit to the result list. When one list is shorter, we treat
    its missing digits as 0. We continue until both lists are exhausted AND the
    carry is 0 (a final carry produces one extra leading node, e.g. 1 in the
    9999999 + 9999 example).

    Using a dummy head node avoids special-casing the first append and lets us
    return dummy.next cleanly.

Why it works:
    Positional addition with carry is exact for base-10 integers of arbitrary
    length. Reverse storage means we never have to know the total length in
    advance or reverse anything - the carry always flows toward the tail, which
    is the more significant end.

Complexity:
    Time:  O(max(m, n)) where m, n are the lengths of the two lists - we visit
           each node once.
    Space: O(max(m, n)) for the output list (O(1) auxiliary beyond the result).
"""

from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        dummy = ListNode()
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            total = v1 + v2 + carry
            carry, digit = divmod(total, 10)
            current.next = ListNode(digit)
            current = current.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next

    # Alternative approach: recursion.
    # Conceptually identical (positional add with carry) but expresses the
    # traversal via the call stack instead of an explicit loop.
    def addTwoNumbersRecursive(
        self,
        l1: Optional[ListNode],
        l2: Optional[ListNode],
        carry: int = 0,
    ) -> Optional[ListNode]:
        if not l1 and not l2 and carry == 0:
            return None
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry
        node = ListNode(total % 10)
        node.next = self.addTwoNumbersRecursive(
            l1.next if l1 else None,
            l2.next if l2 else None,
            total // 10,
        )
        return node


# ---------------------------------------------------------------------------
# Helpers for testing
# ---------------------------------------------------------------------------
def build_list(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(node: Optional[ListNode]) -> List[int]:
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


if __name__ == "__main__":
    sol = Solution()

    for solver in (sol.addTwoNumbers, sol.addTwoNumbersRecursive):
        # Example 1: 342 + 465 = 807
        assert to_list(solver(build_list([2, 4, 3]), build_list([5, 6, 4]))) == [7, 0, 8]

        # Example 2: 0 + 0 = 0
        assert to_list(solver(build_list([0]), build_list([0]))) == [0]

        # Example 3: 9999999 + 9999 = 10009998
        assert to_list(
            solver(build_list([9, 9, 9, 9, 9, 9, 9]), build_list([9, 9, 9, 9]))
        ) == [8, 9, 9, 9, 0, 0, 0, 1]

        # Different lengths, no final carry: 1 + 999 = 1000 -> reversed digits
        assert to_list(solver(build_list([1]), build_list([9, 9, 9]))) == [0, 0, 0, 1]

        # Single digit carry: 5 + 5 = 10
        assert to_list(solver(build_list([5]), build_list([5]))) == [0, 1]

        # Equal length with internal carry: 81 + 19 = 100
        assert to_list(solver(build_list([1, 8]), build_list([9, 1]))) == [0, 0, 1]

    print("All tests passed for 2. Add Two Numbers")
