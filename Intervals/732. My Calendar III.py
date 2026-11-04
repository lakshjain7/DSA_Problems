"""
732. My Calendar III
Difficulty: Hard
Topics: Binary Search, Design, Segment Tree, Prefix Sum, Ordered Set

Problem:
A k-booking happens when k events have some non-empty intersection (there is
some time that is common to all k events). Implement MyCalendarThree:
    MyCalendarThree()        initializes the object.
    int book(int startTime, int endTime)
        Books the half-open event [startTime, endTime) and returns the largest
        integer k such that a k-booking exists in the calendar.

Example:
    book(10, 20) -> 1
    book(50, 60) -> 1
    book(10, 40) -> 2
    book(5, 15)  -> 3
    book(5, 10)  -> 3
    book(25, 55) -> 3

Constraints:
    0 <= startTime < endTime <= 10^9
    At most 400 calls to book.

Approach (sweep line over a difference map):
    Keep a map delta[time] with +1 at each start and -1 at each end. The number
    of overlapping events at any moment is the running prefix sum of delta in
    time order, so the answer is the maximum prefix sum. With at most 400
    calls, re-sorting the keys per call is cheap and simple. Ends are
    exclusive, so an event ending at t and another starting at t do not
    overlap; both deltas live at key t and net out correctly.

Complexity:
    book: O(m log m) where m = number of distinct boundary points (<= 800).
    Space: O(m).

Alternative: a dynamic segment tree with lazy range-add / max (below) gives
O(log C) per call over coordinate range C = 10^9.
"""
from collections import defaultdict


class MyCalendarThree:
    def __init__(self):
        self.delta = defaultdict(int)

    def book(self, startTime: int, endTime: int) -> int:
        self.delta[startTime] += 1
        self.delta[endTime] -= 1
        best = cur = 0
        for t in sorted(self.delta):
            cur += self.delta[t]
            best = max(best, cur)
        return best


class MyCalendarThreeSegTree:
    """Dynamic segment tree: range add +1, global max (no push-down needed)."""

    def __init__(self):
        self.mx = defaultdict(int)    # max in node's subtree incl. own add
        self.add = defaultdict(int)   # pending add applied to whole node range

    def _update(self, l: int, r: int, lo: int, hi: int, node: int) -> None:
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            self.mx[node] += 1
            self.add[node] += 1
            return
        mid = (lo + hi) // 2
        self._update(l, r, lo, mid, 2 * node)
        self._update(l, r, mid + 1, hi, 2 * node + 1)
        self.mx[node] = self.add[node] + max(self.mx[2 * node], self.mx[2 * node + 1])

    def book(self, startTime: int, endTime: int) -> int:
        self._update(startTime, endTime - 1, 0, 10 ** 9, 1)
        return self.mx[1]


if __name__ == "__main__":
    import random
    for cls in (MyCalendarThree, MyCalendarThreeSegTree):
        c = cls()
        out = [c.book(*e) for e in
               [(10, 20), (50, 60), (10, 40), (5, 15), (5, 10), (25, 55)]]
        assert out == [1, 1, 2, 3, 3, 3], out
        c = cls()
        assert c.book(1, 2) == 1
        assert c.book(2, 3) == 1      # touching, not overlapping
        assert c.book(1, 3) == 2
        assert c.book(0, 10 ** 9) == 3
    a, b = MyCalendarThree(), MyCalendarThreeSegTree()
    for _ in range(150):
        s = random.randint(0, 60)
        e = random.randint(s + 1, 70)
        assert a.book(s, e) == b.book(s, e)
    print("All tests passed.")
