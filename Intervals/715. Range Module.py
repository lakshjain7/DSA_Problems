"""
715. Range Module
Difficulty: Hard
Topics: Design, Segment Tree, Ordered Set, Binary Search

Problem:
A Range Module tracks ranges of numbers as half-open intervals [left, right).
Implement the RangeModule class:
  RangeModule()                   Initializes the data structure.
  void addRange(left, right)      Adds the half-open interval [left, right),
                                  tracking every real number in it. Numbers
                                  already tracked are not added twice.
  boolean queryRange(left, right) True iff every real number in [left, right)
                                  is currently tracked.
  void removeRange(left, right)   Stops tracking every real number in [left, right).

Example:
  rm = RangeModule()
  rm.addRange(10, 20); rm.removeRange(14, 16)
  rm.queryRange(10, 14) -> True
  rm.queryRange(13, 15) -> False
  rm.queryRange(16, 17) -> True

Constraints:
  1 <= left < right <= 10^9
  At most 10^4 calls to addRange, queryRange, removeRange.

Approach:
Maintain a sorted list of disjoint, non-adjacent intervals as two parallel
lists: starts L and ends R. Binary search (bisect) finds the affected slice:
  add:    intervals overlapping or touching [left,right) are those with
          R[i] >= left and L[j-1] <= right; merge them into one and replace
          the slice.
  remove: intervals with R > left and L < right are affected; keep the left
          remnant [L, left) and right remnant [right, R) if non-empty.
  query:  the only candidate is the last interval with start <= left; it must
          reach right.

Complexity:
  Time:  O(log n) to locate + O(n) worst-case slice replacement (fast memmove
         in practice); query is O(log n).
  Space: O(n) intervals.

Alternative: a dynamic segment tree with lazy assign (O(log M) per op) or a
TreeMap/SortedDict of intervals; here a bisect list is simplest and fast enough.
"""
from bisect import bisect_left, bisect_right


class RangeModule:
    def __init__(self) -> None:
        self.L: list = []
        self.R: list = []

    def addRange(self, left: int, right: int) -> None:
        i = bisect_left(self.R, left)      # first interval with end >= left
        j = bisect_right(self.L, right)    # intervals [i, j) start <= right
        if i < j:
            left = min(left, self.L[i])
            right = max(right, self.R[j - 1])
        self.L[i:j] = [left]
        self.R[i:j] = [right]

    def queryRange(self, left: int, right: int) -> bool:
        i = bisect_right(self.L, left) - 1
        return i >= 0 and self.R[i] >= right

    def removeRange(self, left: int, right: int) -> None:
        i = bisect_right(self.R, left)     # first interval with end > left
        j = bisect_left(self.L, right)     # intervals [i, j) start < right
        if i >= j:
            return
        newL, newR = [], []
        if self.L[i] < left:
            newL.append(self.L[i]); newR.append(left)
        if self.R[j - 1] > right:
            newL.append(right); newR.append(self.R[j - 1])
        self.L[i:j] = newL
        self.R[i:j] = newR


if __name__ == "__main__":
    import random
    rm = RangeModule()
    rm.addRange(10, 20)
    rm.removeRange(14, 16)
    assert rm.queryRange(10, 14) is True
    assert rm.queryRange(13, 15) is False
    assert rm.queryRange(16, 17) is True

    rm = RangeModule()                      # touching intervals merge
    rm.addRange(1, 5); rm.addRange(5, 9)
    assert rm.queryRange(1, 9) and rm.L == [1] and rm.R == [9]
    rm.addRange(2, 3)                       # contained add is a no-op
    assert rm.L == [1] and rm.R == [9]
    rm.removeRange(1, 9)
    assert not rm.queryRange(1, 2) and rm.L == []
    rm.removeRange(3, 4)                    # remove on empty
    rm.addRange(1, 3); rm.addRange(7, 9); rm.addRange(2, 8)
    assert rm.queryRange(1, 9) and len(rm.L) == 1
    rm.removeRange(1, 2)
    assert not rm.queryRange(1, 2) and rm.queryRange(2, 9)
    rm.removeRange(9, 10)                   # touching but no overlap
    assert rm.queryRange(2, 9)

    # randomized cross-check against integer-unit brute force (half-open unit cells)
    for _ in range(300):
        rm, cells = RangeModule(), set()
        for _ in range(40):
            op = random.choice("arq")
            l = random.randint(1, 20); r = random.randint(l + 1, 22)
            rng = set(range(l, r))
            if op == "a":
                rm.addRange(l, r); cells |= rng
            elif op == "r":
                rm.removeRange(l, r); cells -= rng
            else:
                assert rm.queryRange(l, r) == rng.issubset(cells)
            assert all(a < b for a, b in zip(rm.L, rm.R))
            assert all(rm.R[k] < rm.L[k + 1] for k in range(len(rm.L) - 1))
    print("All tests passed.")
