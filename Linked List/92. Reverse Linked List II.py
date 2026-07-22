"""
92. Reverse Linked List II
Difficulty: Medium
Topics: Linked List, Pointers

PROBLEM STATEMENT
-----------------
Given the head of a singly linked list and two integers left and right where
left <= right, reverse the nodes of the list from position left to position
right, and return the reversed list.

Positions are 1-indexed.

Examples
--------
Example 1:
    Input:  head = [1,2,3,4,5], left = 2, right = 4
    Output: [1,4,3,2,5]

Example 2:
    Input:  head = [5], left = 1, right = 1
    Output: [5]

Constraints
-----------
- The number of nodes in the list is n.
- 1 <= n <= 500
- -500 <= Node.val <= 500
- 1 <= left <= right <= n

Follow up: Could you do it in one pass?


APPROACH  (One pass, in-place, head-insertion / "kick-back")
------------------------------------------------------------
We use a dummy node in front of head so the case left == 1 (reversing from the
very first node) needs no special handling.

1. Walk `prev` to the node just before position `left`. This node stays fixed;
   everything reversed will be re-attached after it.

2. Let `curr` be the first node of the sublist to reverse (position `left`).
   Repeatedly take the node right after `curr` (call it `nxt`) and move it to
   the front of the reversed section, immediately after `prev`. We do this
   (right - left) times. This is the classic "head insertion" technique: each
   iteration pulls one node out and splices it just behind `prev`, which
   incrementally reverses the segment in a single pass.

Pointer surgery per iteration:
    curr.next = nxt.next      # unlink nxt from its spot
    nxt.next  = prev.next     # nxt points to current front of reversed part
    prev.next = nxt           # prev now points to nxt (new front)

COMPLEXITY
----------
Time:  O(n) -- single traversal.
Space: O(1) -- only a constant number of pointers.
"""

from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


def reverseBetween(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    """Reverse nodes from position `left` to `right` (1-indexed), one pass."""
    if head is None or left == right:
        return head

    dummy = ListNode(0, head)
    prev = dummy

    # Move prev to the node just before position `left`.
    for _ in range(left - 1):
        prev = prev.next  # type: ignore[assignment]

    # curr is the first node of the section to reverse.
    curr = prev.next
    for _ in range(right - left):
        nxt = curr.next            # node to move to the front
        curr.next = nxt.next       # detach nxt
        nxt.next = prev.next       # nxt jumps to the front of the segment
        prev.next = nxt            # prev links to the new front

    return dummy.next


# ---------------------------------------------------------------------------
# Alternative approach: collect the sublist, reverse the values in place, and
# write them back. Simpler to reason about but uses O(right-left) extra space
# and still O(n) time. Kept as a second reference / cross-check.
# ---------------------------------------------------------------------------
def reverseBetween_values(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    if head is None or left == right:
        return head
    # Gather references to the affected nodes.
    nodes: List[ListNode] = []
    node, idx = head, 1
    while node:
        if left <= idx <= right:
            nodes.append(node)
        node = node.next
        idx += 1
    # Two-pointer swap of values.
    i, j = 0, len(nodes) - 1
    while i < j:
        nodes[i].val, nodes[j].val = nodes[j].val, nodes[i].val
        i += 1
        j -= 1
    return head


# ---------- test helpers ----------
def build(vals: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    # Provided examples
    assert to_list(reverseBetween(build([1, 2, 3, 4, 5]), 2, 4)) == [1, 4, 3, 2, 5]
    assert to_list(reverseBetween(build([5]), 1, 1)) == [5]

    # Edge cases
    assert to_list(reverseBetween(build([1, 2]), 1, 2)) == [2, 1]          # whole list
    assert to_list(reverseBetween(build([1, 2, 3, 4, 5]), 1, 5)) == [5, 4, 3, 2, 1]
    assert to_list(reverseBetween(build([1, 2, 3, 4, 5]), 3, 3)) == [1, 2, 3, 4, 5]  # no-op
    assert to_list(reverseBetween(build([1, 2, 3]), 1, 2)) == [2, 1, 3]    # reverse head part
    assert to_list(reverseBetween(build([7, 9, 2, 10, 1, 8, 6]), 3, 6)) == [7, 9, 8, 1, 10, 2, 6]

    # Cross-check the two implementations on random inputs.
    import random
    for _ in range(3000):
        n = random.randint(1, 12)
        vals = [random.randint(-500, 500) for _ in range(n)]
        l = random.randint(1, n)
        r = random.randint(l, n)
        a = to_list(reverseBetween(build(vals), l, r))
        b = to_list(reverseBetween_values(build(vals), l, r))
        assert a == b, (vals, l, r, a, b)

    print("All tests passed for 92. Reverse Linked List II")
