"""
82. Remove Duplicates from Sorted List II
Difficulty: Medium
Topics: Linked List, Two Pointers

Problem Statement
-----------------
Given the head of a sorted linked list, delete all nodes that have duplicate
numbers, leaving only distinct numbers from the original list. Return the linked
list sorted as well.

Example 1:
    Input:  head = [1,2,3,3,4,4,5]
    Output: [1,2,5]

Example 2:
    Input:  head = [1,1,1,2,3]
    Output: [2,3]

Constraints:
    - The number of nodes in the list is in the range [0, 300].
    - -100 <= Node.val <= 100
    - The list is guaranteed to be sorted in ascending order.

Approach (dummy head + skip whole runs of duplicates)
-----------------------------------------------------
Because the list is sorted, all equal values are adjacent. We use a dummy node
in front of the head so we can uniformly delete nodes even at the beginning.

We keep `prev` pointing at the last node known to be kept (starts at dummy) and
`cur` scanning forward. Whenever `cur` starts a run of duplicates
(cur.next exists and cur.next.val == cur.val), we advance `cur` to the END of
that run, then splice the whole run out with `prev.next = cur.next`. Otherwise
the value is unique, so we simply move `prev` forward to `cur`.

In both cases `cur` advances, so the scan is linear.

Why a dummy node: the head itself can be a duplicate that must be removed
(Example 2). Anchoring `prev` at a dummy avoids special-casing the head.

Complexity
----------
Time:  O(n)  - single pass over the list.
Space: O(1)  - a few pointers only (iterative). The recursive variant uses
              O(n) call-stack space.
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head: "Optional[ListNode]") -> "Optional[ListNode]":
        dummy = ListNode(0, head)
        prev = dummy
        cur = head
        while cur:
            # If this node begins a run of duplicates, skip the entire run.
            if cur.next and cur.next.val == cur.val:
                dup_val = cur.val
                while cur and cur.val == dup_val:
                    cur = cur.next
                prev.next = cur          # unlink all duplicate nodes
            else:
                prev = cur               # keep this distinct node
                cur = cur.next
        return dummy.next

    def deleteDuplicates_recursive(
        self, head: "Optional[ListNode]"
    ) -> "Optional[ListNode]":
        """Alternative recursive formulation."""
        if not head or not head.next:
            return head
        if head.val == head.next.val:
            # Skip every node equal to head.val, then recurse on the remainder.
            val = head.val
            while head and head.val == val:
                head = head.next
            return self.deleteDuplicates_recursive(head)
        head.next = self.deleteDuplicates_recursive(head.next)
        return head


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------
def build_list(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    assert to_list(sol.deleteDuplicates(build_list([1, 2, 3, 3, 4, 4, 5]))) == [1, 2, 5]
    # Example 2
    assert to_list(sol.deleteDuplicates(build_list([1, 1, 1, 2, 3]))) == [2, 3]

    # Edge cases
    assert to_list(sol.deleteDuplicates(build_list([]))) == []
    assert to_list(sol.deleteDuplicates(build_list([1]))) == [1]
    assert to_list(sol.deleteDuplicates(build_list([1, 1]))) == []          # all removed
    assert to_list(sol.deleteDuplicates(build_list([1, 1, 2, 2]))) == []    # all removed
    assert to_list(sol.deleteDuplicates(build_list([1, 2, 2]))) == [1]      # trailing dup run
    assert to_list(sol.deleteDuplicates(build_list([-1, -1, 0, 0, 0, 7]))) == [7]

    # Recursive variant matches
    assert to_list(sol.deleteDuplicates_recursive(build_list([1, 2, 3, 3, 4, 4, 5]))) == [1, 2, 5]
    assert to_list(sol.deleteDuplicates_recursive(build_list([1, 1, 1, 2, 3]))) == [2, 3]
    assert to_list(sol.deleteDuplicates_recursive(build_list([1, 1]))) == []

    print("All tests passed for 82. Remove Duplicates from Sorted List II")
