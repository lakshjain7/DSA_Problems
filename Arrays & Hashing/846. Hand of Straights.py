"""
846. Hand of Straights
Difficulty: Medium
Topics: Array, Hash Table, Greedy, Sorting

Problem:
Alice has some number of cards and she wants to rearrange the cards into groups
so that each group is of size groupSize, and consists of groupSize consecutive
cards.

Given an integer array hand where hand[i] is the value written on the ith card
and an integer groupSize, return true if she can rearrange the cards, or false
otherwise.

Example 1:
    Input: hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
    Output: true
    Explanation: Alice's hand can be rearranged as [1,2,3],[2,3,4],[6,7,8]

Example 2:
    Input: hand = [1,2,3,4,5], groupSize = 4
    Output: false
    Explanation: Alice's hand can not be rearranged into groups of 4.

Constraints:
    1 <= hand.length <= 10^4
    0 <= hand[i] <= 10^9
    1 <= groupSize <= hand.length

(Same problem as 1296. Divide Array in Sets of K Consecutive Numbers.)

Approach (Greedy with counting, smallest-first):
    The smallest remaining card x can only ever be the *start* of a group —
    nothing smaller exists to precede it. So every copy of x must open a group
    x, x+1, ..., x+groupSize-1. Process distinct values in sorted order; when
    value x still has count c > 0, consume c copies of each of the next
    groupSize-1 consecutive values. If any of them has fewer than c copies,
    the hand is impossible.

    Consuming c groups at once (instead of one at a time) keeps the work
    proportional to the number of distinct values times groupSize.

Complexity:
    Time:  O(n log n) for sorting distinct keys + O(d * groupSize) for the sweep
           (d = distinct values; bounded by O(n * groupSize), typically far less).
    Space: O(n) for the counter.
"""
from collections import Counter, deque
from typing import List


def is_n_straight_hand(hand: List[int], group_size: int) -> bool:
    if len(hand) % group_size:
        return False
    count = Counter(hand)
    for x in sorted(count):
        c = count[x]
        if c == 0:
            continue
        for v in range(x, x + group_size):
            if count[v] < c:
                return False
            count[v] -= c
    return True


def is_n_straight_hand_open_groups(hand: List[int], group_size: int) -> bool:
    """
    Alternative: single sorted sweep tracking how many groups are still "open".

    Walk distinct values in order. `opened` is a queue of how many groups
    started at each of the last groupSize values. Groups that need value x
    = total currently open. If count[x] < open groups -> fail. Also, if x is
    not exactly prev+1 while groups are open -> fail. Extra copies of x start
    new groups; groups started groupSize values ago close now.

    Time O(n log n), Space O(n). Never decrements beyond each distinct key once.
    """
    if len(hand) % group_size:
        return False
    count = Counter(hand)
    opened: deque = deque()
    open_groups = 0
    prev = None
    for x in sorted(count):
        if open_groups > 0 and x != prev + 1:
            return False
        if count[x] < open_groups:
            return False
        new = count[x] - open_groups
        opened.append(new)
        open_groups += new
        if len(opened) == group_size:
            open_groups -= opened.popleft()
        prev = x
    return open_groups == 0


if __name__ == "__main__":
    for fn in (is_n_straight_hand, is_n_straight_hand_open_groups):
        assert fn([1, 2, 3, 6, 2, 3, 4, 7, 8], 3) is True
        assert fn([1, 2, 3, 4, 5], 4) is False
        assert fn([1], 1) is True
        assert fn([5, 1], 1) is True
        assert fn([1, 2, 3], 3) is True
        assert fn([1, 3, 4], 3) is False            # gap
        assert fn([1, 1, 2, 2, 3, 3], 3) is True    # duplicate groups
        assert fn([1, 1, 2, 3], 2) is False
        assert fn([1, 2, 3, 4, 5, 6], 2) is True
        assert fn([8, 10, 12], 3) is False
        assert fn([0, 0, 1, 1, 2, 2, 3, 3], 4) is True
        assert fn([1000000000, 999999999], 2) is True

    # randomized cross-check between both approaches
    import random
    random.seed(846)
    for _ in range(2000):
        h = [random.randint(0, 8) for _ in range(random.randint(1, 12))]
        k = random.randint(1, len(h))
        assert is_n_straight_hand(h, k) == is_n_straight_hand_open_groups(h, k), (h, k)
    print("All tests passed for 846. Hand of Straights")
