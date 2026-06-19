"""
Problem #19 — Remove Nth Node From End of List
Difficulty : Medium
Topics     : Linked List, Two Pointers

─────────────────────────────────────────────────────────────────────────────
PROBLEM STATEMENT
─────────────────────────────────────────────────────────────────────────────
Given the head of a linked list, remove the nth node from the end of the
list and return its head.

Examples:
  Input : head = [1,2,3,4,5], n = 2    Output: [1,2,3,5]
  Input : head = [1], n = 1            Output: []
  Input : head = [1,2], n = 1          Output: [1]

Constraints:
  The number of nodes in the list is sz.
  1 <= sz <= 30
  0 <= Node.val <= 100
  1 <= n <= sz

Follow-up: Can you do this in one pass?

─────────────────────────────────────────────────────────────────────────────
APPROACH — Two Pointers (one pass)
─────────────────────────────────────────────────────────────────────────────
Use a dummy node to simplify edge cases (removing the head).

1. Place a dummy node before head. Set fast = slow = dummy.
2. Advance fast by (n + 1) steps so the gap between fast and slow is n+1.
3. Move both fast and slow together until fast reaches None.
4. At this point slow.next is the node to remove.
5. Unlink: slow.next = slow.next.next.

Why n+1 steps? We want slow to land on the node BEFORE the target so we
can relink easily. Advancing n+1 positions creates exactly that offset.

─────────────────────────────────────────────────────────────────────────────
COMPLEXITY
─────────────────────────────────────────────────────────────────────────────
Time  : O(sz)  — single pass through the list
Space : O(1)   — only two extra pointers
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """Remove the nth node from the end and return the modified head."""
    dummy = ListNode(0, head)
    fast = slow = dummy

    # Advance fast by n+1 steps
    for _ in range(n + 1):
        fast = fast.next

    # Move both until fast is None
    while fast is not None:
        fast = fast.next
        slow = slow.next

    # slow.next is the node to remove
    slow.next = slow.next.next

    return dummy.next


# ─────────────────────────────────────────────────────────────────────────────
# ALTERNATIVE APPROACH — Two pass (count length first)
# ─────────────────────────────────────────────────────────────────────────────
def removeNthFromEnd_two_pass(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    First pass: count length L.
    Second pass: advance (L - n) steps and unlink.

    Time : O(sz)   Space: O(1)
    Simpler logic but requires two traversals.
    """
    dummy = ListNode(0, head)

    # Count nodes
    length = 0
    node = head
    while node:
        length += 1
        node = node.next

    # Advance to node just before the target
    curr = dummy
    for _ in range(length - n):
        curr = curr.next

    curr.next = curr.next.next
    return dummy.next


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def list_to_linked(values: list) -> Optional[ListNode]:
    dummy = ListNode()
    curr = dummy
    for v in values:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def linked_to_list(head: Optional[ListNode]) -> list:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def run(values, n):
        return linked_to_list(removeNthFromEnd(list_to_linked(values), n))

    def run2(values, n):
        return linked_to_list(removeNthFromEnd_two_pass(list_to_linked(values), n))

    # Examples from the problem statement
    assert run([1, 2, 3, 4, 5], 2) == [1, 2, 3, 5], "TC1 failed"
    assert run([1], 1) == [],                         "TC2 failed"
    assert run([1, 2], 1) == [1],                     "TC3 failed"

    # Additional edge cases
    assert run([1, 2], 2) == [2],                     "Remove head of two-node list"
    assert run([1, 2, 3], 3) == [2, 3],               "Remove head"
    assert run([1, 2, 3], 1) == [1, 2],               "Remove tail"
    assert run([1, 2, 3, 4, 5], 5) == [2, 3, 4, 5],  "Remove head of 5-node list"
    assert run([1, 2, 3, 4, 5], 1) == [1, 2, 3, 4],  "Remove tail of 5-node list"

    # Two-pass gives same results
    assert run2([1, 2, 3, 4, 5], 2) == [1, 2, 3, 5]
    assert run2([1], 1) == []
    assert run2([1, 2], 1) == [1]

    print("All tests passed for 19. Remove Nth Node From End of List ✓")
