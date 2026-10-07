"""
61. Rotate List
Difficulty: Medium
Topics: Linked List, Two Pointers

Problem:
Given the head of a linked list, rotate the list to the right by k places.

Examples:
    Input: head = [1,2,3,4,5], k = 2
    Output: [4,5,1,2,3]

    Input: head = [0,1,2], k = 4
    Output: [2,0,1]

Constraints:
    The number of nodes in the list is in the range [0, 500].
    -100 <= Node.val <= 100
    0 <= k <= 2 * 10^9

Approach (make a ring, then cut):
    1. Walk to the tail while counting length n; link tail -> head (a ring).
    2. Rotating right by k equals moving the new head to position n - (k % n).
       The new tail is the node just before it, at n - k%n - 1 steps from head.
    3. Cut the ring after the new tail and return the new head.
    k % n handles k much larger than n.

Complexity:
    Time:  O(n)
    Space: O(1)

Alternative (two pointers):
    Advance a fast pointer k%n nodes, then move fast and slow together until fast
    reaches the tail; slow is then the new tail.
"""
from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


def rotateRight(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or not head.next or k == 0:
        return head
    n, tail = 1, head
    while tail.next:
        tail = tail.next
        n += 1
    k %= n
    if k == 0:
        return head
    tail.next = head
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head


def rotateRightTwoPointers(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or not head.next:
        return head
    n, cur = 0, head
    while cur:
        n += 1
        cur = cur.next
    k %= n
    if k == 0:
        return head
    fast = slow = head
    for _ in range(k):
        fast = fast.next
    while fast.next:
        fast, slow = fast.next, slow.next
    new_head = slow.next
    slow.next = None
    fast.next = head
    return new_head


def build(a: List[int]) -> Optional[ListNode]:
    dummy = cur = ListNode()
    for x in a:
        cur.next = ListNode(x)
        cur = cur.next
    return dummy.next


def to_list(h: Optional[ListNode]) -> List[int]:
    out = []
    while h:
        out.append(h.val)
        h = h.next
    return out


if __name__ == "__main__":
    for f in (rotateRight, rotateRightTwoPointers):
        assert to_list(f(build([1, 2, 3, 4, 5]), 2)) == [4, 5, 1, 2, 3]
        assert to_list(f(build([0, 1, 2]), 4)) == [2, 0, 1]
        assert to_list(f(build([]), 3)) == []
        assert to_list(f(build([1]), 99)) == [1]
        assert to_list(f(build([1, 2]), 0)) == [1, 2]
        assert to_list(f(build([1, 2]), 2)) == [1, 2]
        assert to_list(f(build([1, 2]), 1)) == [2, 1]
        assert to_list(f(build([1, 2, 3]), 2000000000)) == [2, 3, 1]
    print("All tests passed!")
