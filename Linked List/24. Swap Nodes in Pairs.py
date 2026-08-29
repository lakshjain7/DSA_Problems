"""
24. Swap Nodes in Pairs
Difficulty: Medium
Topics: Linked List, Recursion

Problem Statement:
Given a linked list, swap every two adjacent nodes and return its head. You must
solve the problem without modifying the values in the list's nodes (i.e., only
nodes themselves may be changed.)

Example 1:
    Input:  head = [1,2,3,4]
    Output: [2,1,4,3]

Example 2:
    Input:  head = []
    Output: []

Example 3:
    Input:  head = [1]
    Output: [1]

Example 4:
    Input:  head = [1,2,3]
    Output: [2,1,3]

Constraints:
    - The number of nodes in the list is in the range [0, 100].
    - 0 <= Node.val <= 100

--------------------------------------------------------------------------------
Approach (Iterative with a dummy node):
The core difficulty is re-wiring pointers correctly for each adjacent pair while
keeping a handle on the node that precedes the pair (so it can point at the new
first node after the swap).

We use a sentinel `dummy` whose `next` is the head. We keep a `prev` pointer,
starting at `dummy`. As long as there are at least two nodes ahead of `prev`
(call them `first` and `second`), we perform the swap:

    prev -> first -> second -> rest
becomes
    prev -> second -> first -> rest

Concretely:
    first.next  = second.next   # first now points past the pair
    second.next = first         # second becomes the leading node
    prev.next   = second        # previous segment links to new leader
    prev        = first         # advance prev to the tail of the swapped pair

Because we only relink node references and never touch `.val`, this satisfies the
"no value modification" constraint.

Why it works:
Each iteration fully resolves one pair and leaves `prev` pointing at the last
node of that resolved pair, which is exactly the predecessor for the next pair.
The invariant "everything before and including prev is finalized and correctly
ordered" is preserved every step, so the whole list ends up correct.

Complexity:
    Time:  O(n) - each node is visited a constant number of times.
    Space: O(1) - only a fixed number of pointers are used.

--------------------------------------------------------------------------------
Alternative Approach (Recursion):
Swap the first two nodes, then recursively swap the rest and attach it. This is
clean but uses O(n) stack space due to recursion depth.
"""

from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy

        while prev.next and prev.next.next:
            first = prev.next
            second = first.next

            # Swap
            first.next = second.next
            second.next = first
            prev.next = second

            # Advance prev to the end of the swapped pair
            prev = first

        return dummy.next

    def swapPairsRecursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        first = head
        second = head.next
        first.next = self.swapPairsRecursive(second.next)
        second.next = first
        return second


# ------------------------------ Test Helpers ------------------------------ #
def build_list(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    for v in values:
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
    sol = Solution()

    for method in (sol.swapPairs, sol.swapPairsRecursive):
        # Example 1
        assert to_list(method(build_list([1, 2, 3, 4]))) == [2, 1, 4, 3]
        # Example 2: empty
        assert to_list(method(build_list([]))) == []
        # Example 3: single node
        assert to_list(method(build_list([1]))) == [1]
        # Example 4: odd length
        assert to_list(method(build_list([1, 2, 3]))) == [2, 1, 3]
        # Longer even list
        assert to_list(method(build_list([1, 2, 3, 4, 5, 6]))) == [2, 1, 4, 3, 6, 5]
        # Longer odd list
        assert to_list(method(build_list([1, 2, 3, 4, 5]))) == [2, 1, 4, 3, 5]
        # Two nodes
        assert to_list(method(build_list([7, 8]))) == [8, 7]

    print("All tests passed for 24. Swap Nodes in Pairs")
