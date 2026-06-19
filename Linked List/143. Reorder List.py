"""
Problem 143: Reorder List
Difficulty: Medium
Topics: Linked List, Two Pointers, Stack, Recursion

Problem Statement:
    You are given the head of a singly linked-list:
        L0 → L1 → … → Ln-1 → Ln
    Reorder it to:
        L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …
    You may not modify the values in the list's nodes. Only nodes themselves may be changed.

Examples:
    Input: head = [1,2,3,4]
    Output: [1,4,2,3]

    Input: head = [1,2,3,4,5]
    Output: [1,5,2,4,3]

Constraints:
    - The number of nodes in the list is in the range [1, 5 * 10^4].
    - 1 <= Node.val <= 1000

Approach (Three-step in-place, O(1) extra space):
    Step 1 — Find the middle: Use slow/fast pointer technique.
              slow advances 1 step, fast advances 2. When fast reaches the end,
              slow is at the middle.
    Step 2 — Reverse second half: Reverse the list from mid.next onwards.
              Now we have two independent lists: first half and reversed second half.
    Step 3 — Merge: Interleave the two lists one node at a time.

    Why this works: After splitting and reversing, the second half's head is the
    last node of the original. We just alternate pointers.

    Example for [1,2,3,4,5]:
      After find mid: [1,2,3] and [4,5]
      After reverse second: [1,2,3] and [5,4]
      After merge: [1,5,2,4,3] ✓

Complexity:
    Time:  O(n) — three linear passes
    Space: O(1) — in-place pointer manipulation

Alternative Approach (Using a deque):
    Collect all nodes into a deque, then pop from front and back alternately
    to rebuild the list. O(n) time and O(n) space.
"""

from typing import Optional
from collections import deque


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


def reorderList(head: Optional[ListNode]) -> None:
    """
    Reorder the linked list in-place. Modifies head in place (no return value).
    """
    if not head or not head.next:
        return

    # Step 1: Find the middle of the list
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    # slow is now at the middle node

    # Step 2: Reverse the second half (from slow.next onwards)
    prev = None
    curr = slow.next
    slow.next = None  # cut the list in half

    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    second_half = prev  # head of reversed second half

    # Step 3: Merge the two halves
    first, second = head, second_half
    while second:
        tmp1 = first.next
        tmp2 = second.next
        first.next = second
        second.next = tmp1
        first = tmp1
        second = tmp2


def reorderList_deque(head: Optional[ListNode]) -> None:
    """Alternative: collect nodes into a deque, then interleave."""
    if not head or not head.next:
        return

    nodes = deque()
    curr = head
    while curr:
        nodes.append(curr)
        curr = curr.next

    dummy = ListNode(0)
    tail = dummy
    left = True
    while nodes:
        if left:
            tail.next = nodes.popleft()
        else:
            tail.next = nodes.pop()
        tail = tail.next
        left = not left
    tail.next = None


# ─── Helpers for testing ───────────────────────────────────────────────────────

def build_list(vals: list) -> Optional[ListNode]:
    if not vals:
        return None
    head = ListNode(vals[0])
    curr = head
    for v in vals[1:]:
        curr.next = ListNode(v)
        curr = curr.next
    return head


def list_to_array(head: Optional[ListNode]) -> list:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    # Test 1: even length [1,2,3,4] → [1,4,2,3]
    head = build_list([1, 2, 3, 4])
    reorderList(head)
    assert list_to_array(head) == [1, 4, 2, 3], f"Test 1 failed: {list_to_array(head)}"

    # Test 2: odd length [1,2,3,4,5] → [1,5,2,4,3]
    head = build_list([1, 2, 3, 4, 5])
    reorderList(head)
    assert list_to_array(head) == [1, 5, 2, 4, 3], f"Test 2 failed: {list_to_array(head)}"

    # Test 3: single node [1] → [1]
    head = build_list([1])
    reorderList(head)
    assert list_to_array(head) == [1], f"Test 3 failed: {list_to_array(head)}"

    # Test 4: two nodes [1,2] → [1,2]
    head = build_list([1, 2])
    reorderList(head)
    assert list_to_array(head) == [1, 2], f"Test 4 failed: {list_to_array(head)}"

    # Test 5: three nodes [1,2,3] → [1,3,2]
    head = build_list([1, 2, 3])
    reorderList(head)
    assert list_to_array(head) == [1, 3, 2], f"Test 5 failed: {list_to_array(head)}"

    # Test 6: deque alternative on same cases
    head = build_list([1, 2, 3, 4])
    reorderList_deque(head)
    assert list_to_array(head) == [1, 4, 2, 3], f"Test 6 (deque) failed: {list_to_array(head)}"

    head = build_list([1, 2, 3, 4, 5])
    reorderList_deque(head)
    assert list_to_array(head) == [1, 5, 2, 4, 3], f"Test 7 (deque) failed: {list_to_array(head)}"

    print("All tests passed for 143. Reorder List!")
