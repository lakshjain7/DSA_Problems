"""
148. Sort List
Difficulty: Medium
Topics: Linked List, Two Pointers, Divide and Conquer, Sorting, Merge Sort

Problem Statement:
    Given the head of a linked list, return the list after sorting it in
    ascending order.

    Follow up: Can you sort the linked list in O(n log n) time and O(1) memory
    (i.e. constant space)?

Examples:
    Example 1:
        Input:  head = [4, 2, 1, 3]
        Output: [1, 2, 3, 4]

    Example 2:
        Input:  head = [-1, 5, 3, 4, 0]
        Output: [-1, 0, 3, 4, 5]

    Example 3:
        Input:  head = []
        Output: []

Constraints:
    - The number of nodes in the list is in the range [0, 5 * 10^4].
    - -10^5 <= Node.val <= 10^5


Approach (Top-Down Merge Sort):
    Merge sort is the natural fit for linked lists because, unlike arrays, we do
    not need random access — we only ever walk forward, and splicing nodes is
    O(1).

    1. Base case: a list with 0 or 1 node is already sorted.
    2. Split: use the slow/fast (tortoise/hare) pointer technique to find the
       middle. Cut the list into two halves. To guarantee the halves shrink
       (and avoid infinite recursion on a 2-node list), we track `prev` and sever
       the link right before slow's final position so neither half is ever empty.
    3. Recurse on both halves.
    4. Merge the two sorted halves with a standard two-pointer merge.

    Why it works: merge sort's correctness does not depend on random access. Each
    split halves the problem; merging two sorted lists yields a sorted list, so
    by induction the whole list is sorted.

Complexity:
    Time:  O(n log n) — log n levels of splitting, O(n) merge work per level.
    Space: O(log n) — recursion stack depth (top-down). The bottom-up variant
           below achieves O(1) auxiliary space to satisfy the follow-up.


Alternative Approach (Bottom-Up Merge Sort, O(1) space):
    Iteratively merge sublists of size 1, 2, 4, 8, ... In each pass we walk the
    list, cut off two runs of the current size, merge them, and stitch the result
    onto the growing output. No recursion, so only O(1) extra pointers are used.
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Top-down merge sort. Time O(n log n), space O(log n)."""
        if head is None or head.next is None:
            return head

        # Split into two halves using slow/fast pointers.
        prev, slow, fast = None, head, head
        while fast is not None and fast.next is not None:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        # prev is guaranteed not None here (list has >= 2 nodes), so cut safely.
        prev.next = None  # type: ignore[union-attr]

        left = self.sortList(head)
        right = self.sortList(slow)
        return self._merge(left, right)

    def _merge(
        self, a: Optional[ListNode], b: Optional[ListNode]
    ) -> Optional[ListNode]:
        dummy = tail = ListNode()
        while a is not None and b is not None:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a if a is not None else b
        return dummy.next

    def sortListBottomUp(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Iterative bottom-up merge sort. Time O(n log n), space O(1)."""
        if head is None or head.next is None:
            return head

        # Count nodes.
        length = 0
        node = head
        while node is not None:
            length += 1
            node = node.next

        dummy = ListNode(0, head)
        size = 1
        while size < length:
            prev, curr = dummy, dummy.next
            while curr is not None:
                left = curr
                right = self._split(left, size)
                curr = self._split(right, size)
                prev = self._merge_into(prev, left, right)
            size *= 2
        return dummy.next

    def _split(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """Advance n-1 nodes, sever, and return the head of the remainder."""
        for _ in range(n - 1):
            if head is None:
                break
            head = head.next
        if head is None:
            return None
        rest = head.next
        head.next = None
        return rest

    def _merge_into(
        self, prev: ListNode, a: Optional[ListNode], b: Optional[ListNode]
    ) -> ListNode:
        """Merge a and b, attach after prev, return the new tail."""
        tail = prev
        while a is not None and b is not None:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a if a is not None else b
        while tail.next is not None:
            tail = tail.next
        return tail


# ---------------------------------------------------------------------------
# Helpers for testing
# ---------------------------------------------------------------------------
def build(vals):
    dummy = tail = ListNode()
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    sol = Solution()

    for method in (sol.sortList, sol.sortListBottomUp):
        # Example cases
        assert to_list(method(build([4, 2, 1, 3]))) == [1, 2, 3, 4]
        assert to_list(method(build([-1, 5, 3, 4, 0]))) == [-1, 0, 3, 4, 5]
        # Edge: empty list
        assert to_list(method(build([]))) == []
        # Edge: single node
        assert to_list(method(build([7]))) == [7]
        # Edge: two nodes needing swap
        assert to_list(method(build([2, 1]))) == [1, 2]
        # Duplicates and negatives
        assert to_list(method(build([3, 1, 2, 3, 1]))) == [1, 1, 2, 3, 3]
        # Already sorted
        assert to_list(method(build([1, 2, 3, 4, 5]))) == [1, 2, 3, 4, 5]
        # Reverse sorted
        assert to_list(method(build([5, 4, 3, 2, 1]))) == [1, 2, 3, 4, 5]
        # Larger stress test
        import random

        arr = [random.randint(-50, 50) for _ in range(200)]
        assert to_list(method(build(arr))) == sorted(arr)

    print("All tests passed for 148. Sort List")
