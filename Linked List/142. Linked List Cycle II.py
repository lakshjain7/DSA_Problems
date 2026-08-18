"""
142. Linked List Cycle II
Difficulty: Medium
Topics: Hash Table, Linked List, Two Pointers (Floyd's Cycle Detection)

Problem Statement
-----------------
Given the head of a linked list, return the node where the cycle begins. If
there is no cycle, return null.

There is a cycle in a linked list if there is some node in the list that can be
reached again by continuously following the next pointer. Internally, pos is
used to denote the index of the node that tail's next pointer is connected to
(0-indexed). It is -1 if there is no cycle. Note that pos is not passed as a
parameter.

Do not modify the linked list.

Example 1:
    Input:  head = [3,2,0,-4], pos = 1
    Output: tail connects to node index 1 (value 2)

Example 2:
    Input:  head = [1,2], pos = 0
    Output: tail connects to node index 0 (value 1)

Example 3:
    Input:  head = [1], pos = -1
    Output: no cycle

Constraints:
    - The number of nodes in the list is in the range [0, 10^4].
    - -10^5 <= Node.val <= 10^5
    - pos is -1 or a valid index in the linked list.

Follow up: Can you solve it using O(1) (i.e. constant) memory?

Approach (Floyd's Tortoise and Hare, O(1) space)
------------------------------------------------
Phase 1 - detect a cycle: advance slow by 1 and fast by 2. If they ever meet,
a cycle exists. If fast reaches the end (null), there is no cycle.

Phase 2 - find the entrance: Let L be the distance from head to the cycle
entrance, and let the meeting point be k steps into the cycle. When slow and
fast meet, one can show (distance covered by fast = 2 * distance by slow) that
the distance from head to the entrance equals the distance from the meeting
point to the entrance (mod cycle length). So reset one pointer to head and
advance both one step at a time; they meet exactly at the cycle entrance.

Complexity
----------
Time:  O(n) - linear passes for detection and for locating the entrance.
Space: O(1) - only two pointers.
"""

from __future__ import annotations

from typing import List, Optional


class ListNode:
    def __init__(self, x: int) -> None:
        self.val = x
        self.next: Optional["ListNode"] = None


class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        # Phase 1: find a meeting point inside the cycle (if any).
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                break
        else:
            # Loop ended because fast hit the end -> no cycle.
            return None

        # Phase 2: walk from head and meeting point in lockstep to the entrance.
        ptr = head
        while ptr is not slow:
            ptr = ptr.next
            slow = slow.next
        return ptr


class SolutionHashSet:
    """Alternative: track visited nodes by identity. O(n) space, O(1) per step."""

    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        seen: set[int] = set()
        node = head
        while node:
            if id(node) in seen:
                return node
            seen.add(id(node))
            node = node.next
        return None


# ----------------------------- Test helpers ----------------------------------
def build_list_with_cycle(values: List[int], pos: int) -> Optional[ListNode]:
    """Build a linked list; if pos >= 0 connect tail.next to node at index pos."""
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


def entrance_index(head: Optional[ListNode], values: List[int], pos: int):
    """Return the expected entrance node object for verification."""
    if pos < 0 or not values:
        return None
    # Rebuild mapping by walking; find node at index pos following from head.
    node = head
    for _ in range(pos):
        node = node.next
    return node


if __name__ == "__main__":
    for SolClass in (Solution, SolutionHashSet):
        sol = SolClass()

        # Example 1: cycle enters at index 1 (value 2)
        vals1, pos1 = [3, 2, 0, -4], 1
        head1 = build_list_with_cycle(vals1, pos1)
        result1 = sol.detectCycle(head1)
        assert result1 is entrance_index(head1, vals1, pos1), SolClass.__name__
        assert result1 is not None and result1.val == 2, SolClass.__name__

        # Example 2: cycle enters at index 0 (value 1)
        vals2, pos2 = [1, 2], 0
        head2 = build_list_with_cycle(vals2, pos2)
        result2 = sol.detectCycle(head2)
        assert result2 is head2, SolClass.__name__
        assert result2.val == 1, SolClass.__name__

        # Example 3: single node, no cycle
        head3 = build_list_with_cycle([1], -1)
        assert sol.detectCycle(head3) is None, SolClass.__name__

        # Empty list
        assert sol.detectCycle(build_list_with_cycle([], -1)) is None, SolClass.__name__

        # No cycle, multiple nodes
        head5 = build_list_with_cycle([1, 2, 3, 4, 5], -1)
        assert sol.detectCycle(head5) is None, SolClass.__name__

        # Self-loop: single node pointing to itself
        head6 = build_list_with_cycle([7], 0)
        r6 = sol.detectCycle(head6)
        assert r6 is head6 and r6.val == 7, SolClass.__name__

        # Cycle entrance at the last node
        vals7, pos7 = [1, 2, 3, 4], 3
        head7 = build_list_with_cycle(vals7, pos7)
        r7 = sol.detectCycle(head7)
        assert r7 is entrance_index(head7, vals7, pos7) and r7.val == 4, SolClass.__name__

    print("All tests passed for 142. Linked List Cycle II")
