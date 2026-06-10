"""
23. Merge k Sorted Lists
Difficulty: Hard
Topics: Linked List, Heap (Priority Queue), Divide and Conquer, Merge Sort

Problem Statement:
You are given an array of k linked-lists `lists`, each linked-list is sorted
in ascending order. Merge all the linked-lists into one sorted linked-list and
return it.

Examples:
    Input:  lists = [[1,4,5],[1,3,4],[2,6]]
    Output: [1,1,2,3,4,4,5,6]
    Explanation: merging [1->4->5, 1->3->4, 2->6] gives 1->1->2->3->4->4->5->6

    Input:  lists = []
    Output: []

    Input:  lists = [[]]
    Output: []

Constraints:
    k == lists.length
    0 <= k <= 10^4
    0 <= lists[i].length <= 500
    -10^4 <= lists[i][j] <= 10^4
    lists[i] is sorted in ascending order.
    The sum of lists[i].length will not exceed 10^4.

Approach (Min-Heap of k heads):
Push the head of every non-empty list into a min-heap keyed by node value
(with a tie-breaking counter, since ListNode is not comparable). Repeatedly
pop the smallest node, append it to the result, and push that node's
successor. The heap always holds at most one node per list, so every pop is
guaranteed to be the global minimum of all remaining elements — which is
exactly why the output is sorted. With N total nodes, each node enters and
leaves the heap once at log k cost.

Complexity:
    Time:  O(N log k) — N total nodes, heap of size <= k.
    Space: O(k) for the heap (output reuses existing nodes).

Alternative (Divide and Conquer / pairwise merge):
Repeatedly merge lists in pairs — merge lists[i] and lists[i + step] like the
merge step of merge sort — halving the number of lists each round. log k
rounds, each touching all N nodes: O(N log k) time, O(1) extra space
iteratively. Same asymptotics as the heap, but no heap bookkeeping.
"""

import heapq
from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """Min-heap solution — O(N log k)."""
    heap: List[tuple] = []
    counter = 0  # tie-breaker so ListNodes are never compared directly
    for node in lists:
        if node:
            heapq.heappush(heap, (node.val, counter, node))
            counter += 1

    dummy = ListNode()
    tail = dummy
    while heap:
        _, _, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, counter, node.next))
            counter += 1
    tail.next = None
    return dummy.next


def _merge_two(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
    """Standard two-list merge used by the divide-and-conquer variant."""
    dummy = ListNode()
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def merge_k_lists_divide_conquer(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """Alternative: pairwise merging, log k rounds — O(N log k)."""
    if not lists:
        return None
    step = 1
    while step < len(lists):
        for i in range(0, len(lists) - step, step * 2):
            lists[i] = _merge_two(lists[i], lists[i + step])
        step *= 2
    return lists[0]


# ---- helpers for tests ----
def build(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    out: List[int] = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    for solve in (merge_k_lists, merge_k_lists_divide_conquer):
        # Provided examples
        assert to_list(solve([build([1, 4, 5]), build([1, 3, 4]), build([2, 6])])) == [1, 1, 2, 3, 4, 4, 5, 6]
        assert to_list(solve([])) == []                       # k == 0
        assert to_list(solve([build([])])) == []              # one empty list
        # Edge cases
        assert to_list(solve([build([]), build([])])) == []   # all empty
        assert to_list(solve([build([7])])) == [7]            # single list
        assert to_list(solve([build([]), build([1]), build([])])) == [1]   # empties mixed in
        assert to_list(solve([build([-3, -1]), build([-2, 0, 4])])) == [-3, -2, -1, 0, 4]  # negatives
        assert to_list(solve([build([1, 1, 1]), build([1, 1])])) == [1, 1, 1, 1, 1]        # duplicates
        assert to_list(solve([build([5]), build([3]), build([4]), build([1]), build([2])])) == [1, 2, 3, 4, 5]
    print("All tests passed for 23. Merge k Sorted Lists")
