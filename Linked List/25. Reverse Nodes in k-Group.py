"""
Problem 25: Reverse Nodes in k-Group
Difficulty: Hard
Topics: Linked List, Recursion

Problem Statement:
Given the head of a linked list, reverse the nodes of the list k at a time,
and return the modified list.
k is a positive integer and is less than or equal to the length of the linked list.
If the number of nodes is not a multiple of k then the left-out nodes at the end
should remain as they are.
You may not alter the values in the list's nodes, only the nodes themselves may be changed.

Examples:
  Input: head = [1,2,3,4,5], k = 2
  Output: [2,1,4,3,5]

  Input: head = [1,2,3,4,5], k = 3
  Output: [3,2,1,4,5]

Constraints:
  The number of nodes in the list is n.
  1 <= k <= n <= 5000
  0 <= Node.val <= 1000

Approach:
  Iterative with a dummy head node:
  1. Use a dummy node pointing to head for clean handling of the new head.
  2. Use a 'group_prev' pointer marking the node just before the current k-group.
  3. For each k-group:
     a. Find the k-th node from group_prev. If fewer than k nodes remain, stop.
     b. Reverse the k nodes in-place using three pointers (prev, curr, next).
     c. Reconnect: group_prev.next -> (old tail, now group head)
                   group_prev -> (old head, now group tail)
  4. Advance group_prev to the tail of the just-reversed group.

Complexity:
  Time:  O(n) — each node is visited at most twice (once to count, once to reverse)
  Space: O(1) — iterative, only a fixed number of pointers

Alternative Approach:
  Recursive:
    Base case: fewer than k nodes remaining → return head as-is.
    Reverse the first k nodes, then recurse on the rest.
    Connect the reversed segment to the result of the recursive call.
  Time: O(n), Space: O(n/k) for the call stack.
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


def reverseKGroup(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """Iterative solution — O(n) time, O(1) space."""
    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        # Find the k-th node from group_prev
        kth = get_kth(group_prev, k)
        if not kth:
            break

        group_next = kth.next  # node after the current k-group

        # Reverse k nodes starting from group_prev.next
        prev, curr = group_next, group_prev.next
        while curr != group_next:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # Reconnect to the list
        tmp = group_prev.next        # old head of group (now tail after reversal)
        group_prev.next = kth        # kth is the new head of the reversed group
        group_prev = tmp             # advance group_prev to the tail

    return dummy.next


def get_kth(curr: ListNode, k: int) -> Optional[ListNode]:
    """Walk k steps from curr; return the k-th node or None if fewer than k nodes."""
    while curr and k > 0:
        curr = curr.next
        k -= 1
    return curr


def reverseKGroup_recursive(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """Alternative: recursive solution — O(n) time, O(n/k) space."""
    # Check if at least k nodes remain
    count, node = 0, head
    while node and count < k:
        node = node.next
        count += 1
    if count < k:
        return head  # fewer than k nodes: leave as-is

    # Reverse k nodes
    prev, curr = None, head
    for _ in range(k):
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    # head is now the tail of the reversed segment
    # curr is the head of the remaining list
    head.next = reverseKGroup_recursive(curr, k)
    return prev  # prev is the new head of the reversed segment


# ── helpers for testing ──────────────────────────────────────────────────────

def build_list(vals: list) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head: Optional[ListNode]) -> list:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    # Test iterative
    assert list_to_array(reverseKGroup(build_list([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert list_to_array(reverseKGroup(build_list([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]
    assert list_to_array(reverseKGroup(build_list([1, 2, 3, 4, 5]), 1)) == [1, 2, 3, 4, 5]
    assert list_to_array(reverseKGroup(build_list([1, 2, 3, 4, 5]), 5)) == [5, 4, 3, 2, 1]
    assert list_to_array(reverseKGroup(build_list([1]), 1)) == [1]
    # k > remaining tail: tail stays unchanged
    assert list_to_array(reverseKGroup(build_list([1, 2, 3, 4, 5]), 4)) == [4, 3, 2, 1, 5]

    # Test recursive
    assert list_to_array(reverseKGroup_recursive(build_list([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert list_to_array(reverseKGroup_recursive(build_list([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]
    assert list_to_array(reverseKGroup_recursive(build_list([1, 2, 3, 4, 5]), 5)) == [5, 4, 3, 2, 1]

    print("All tests passed!")
