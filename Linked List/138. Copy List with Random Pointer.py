"""
138. Copy List with Random Pointer
Difficulty: Medium
Topics: Hash Table, Linked List

Problem Statement:
A linked list of length n is given such that each node contains an additional
random pointer, which could point to any node in the list, or null.

Construct a deep copy of the list. The deep copy should consist of exactly n
brand new nodes, where each new node has its value set to the value of its
corresponding original node. Both the `next` and `random` pointer of the new
nodes should point to new nodes in the copied list such that the pointers in
the original list and copied list represent the same list state. None of the
pointers in the new list should point to nodes in the original list.

The linked list is represented in the input/output as a list of n nodes.
Each node is represented as a pair of [val, random_index] where random_index
is the index of the node (0-indexed) that the random pointer points to, or
null if it does not point to any node.

Return the head of the copied linked list.

Examples:
    Input: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
    Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]

    Input: head = [[1,1],[2,1]]
    Output: [[1,1],[2,1]]

    Input: head = [[3,null],[3,0],[3,null]]
    Output: [[3,null],[3,0],[3,null]]

Constraints:
    0 <= n <= 1000
    -10^4 <= Node.val <= 10^4
    Node.random is null or is pointing to some node in the linked list.

Approach 1 (Hash Map, two passes):
Use a hash map from original node -> cloned node.
Pass 1: walk the original list, create a cloned node for every original node
(value copied, next/random left as None for now), and store the mapping.
Pass 2: walk the original list again; for each original node, set
    clone.next   = mapping.get(original.next)
    clone.random = mapping.get(original.random)
Since every original node already has a corresponding entry in the map by
the time pass 2 runs, every next/random link resolves correctly (map.get on
None returns None, which is exactly what we want for null pointers).

Complexity:
    Time:  O(n)  - two linear passes over the list
    Space: O(n)  - hash map storing n original->clone pairs

Approach 2 (Interweaving, O(1) extra space - the classic follow-up):
1. For each original node `orig`, insert a cloned node directly after it in
   the same list: orig -> clone -> orig.next -> ...
2. Now `orig.next` is `clone`, so `orig.random.next` is the clone of
   `orig.random` (when random is not None). Walk the interwoven list and set
   clone.random = orig.random.next if orig.random else None.
3. Finally, unweave the two lists: restore the original list's `next`
   pointers and extract the cloned nodes into their own list.

This achieves O(1) auxiliary space (no hash map) at the cost of three passes
and trickier pointer bookkeeping. Both approaches are O(n) time.
"""

from typing import Dict, Optional


class Node:
    def __init__(self, x: int, next: "Optional[Node]" = None, random: "Optional[Node]" = None):
        self.val = int(x)
        self.next = next
        self.random = random


def copy_random_list(head: Optional[Node]) -> Optional[Node]:
    """Hash map approach: O(n) time, O(n) space."""
    if head is None:
        return None

    mapping: Dict[Node, Node] = {}

    # Pass 1: create all clones (value only).
    current = head
    while current:
        mapping[current] = Node(current.val)
        current = current.next

    # Pass 2: wire up next and random pointers using the map.
    current = head
    while current:
        clone = mapping[current]
        clone.next = mapping.get(current.next) if current.next else None
        clone.random = mapping.get(current.random) if current.random else None
        current = current.next

    return mapping[head]


def copy_random_list_o1_space(head: Optional[Node]) -> Optional[Node]:
    """Interweaving approach: O(n) time, O(1) extra space (excluding output)."""
    if head is None:
        return None

    # Step 1: interweave clones into the original list.
    current = head
    while current:
        clone = Node(current.val)
        clone.next = current.next
        current.next = clone
        current = clone.next

    # Step 2: assign random pointers for the clones.
    current = head
    while current:
        clone = current.next
        clone.random = current.random.next if current.random else None
        current = clone.next

    # Step 3: unweave the two lists.
    original_ptr = head
    clone_head = head.next
    clone_ptr = clone_head
    while original_ptr:
        original_ptr.next = original_ptr.next.next
        clone_ptr.next = clone_ptr.next.next if clone_ptr.next else None
        original_ptr = original_ptr.next
        clone_ptr = clone_ptr.next

    return clone_head


# --- Test helpers -----------------------------------------------------

def build_list(pairs):
    """pairs: list of [val, random_index_or_None] -> returns head Node."""
    if not pairs:
        return None
    nodes = [Node(v) for v, _ in pairs]
    for i, (_, r) in enumerate(pairs):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        nodes[i].random = nodes[r] if r is not None else None
    return nodes[0]


def to_pairs(head):
    """Convert a linked list back to [[val, random_index], ...] for comparison."""
    nodes = []
    current = head
    while current:
        nodes.append(current)
        current = current.next
    index_of = {id(n): i for i, n in enumerate(nodes)}
    return [
        [n.val, index_of[id(n.random)] if n.random else None]
        for n in nodes
    ]


def assert_deep_copy_correct(original_pairs, copied_head, original_head):
    """Verify copied list matches structurally but shares no node objects."""
    assert to_pairs(copied_head) == original_pairs

    orig_nodes = set()
    current = original_head
    while current:
        orig_nodes.add(id(current))
        current = current.next

    current = copied_head
    while current:
        assert id(current) not in orig_nodes, "Copy must not reuse original nodes"
        current = current.next


if __name__ == "__main__":
    test_cases = [
        [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
        [[1, 1], [2, 1]],
        [[3, None], [3, 0], [3, None]],
        [],  # empty list
        [[1, None]],  # single node, no random
        [[1, 0]],  # single node, random points to itself
    ]

    for pairs in test_cases:
        head = build_list(pairs)
        copied = copy_random_list(head)
        if not pairs:
            assert copied is None
        else:
            assert_deep_copy_correct(pairs, copied, head)

        # Re-build fresh list for the O(1) space approach (first approach may
        # not mutate original, but rebuilding keeps tests independent).
        head2 = build_list(pairs)
        copied2 = copy_random_list_o1_space(head2)
        if not pairs:
            assert copied2 is None
        else:
            assert_deep_copy_correct(pairs, copied2, head2)
            # Ensure original list structure is restored after interweaving.
            assert to_pairs(head2) == pairs

    print("All test cases passed!")
