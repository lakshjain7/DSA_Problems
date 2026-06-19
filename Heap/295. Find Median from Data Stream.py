"""
Problem Number: 295
Title: Find Median from Data Stream
Difficulty: Hard
Topics: Two Pointers, Design, Sorting, Heap (Priority Queue), Data Stream

Implement MedianFinder:
  - addNum(num): adds integer from stream
  - findMedian(): returns median of all elements so far

Approach (Two Heaps):
  lo (max-heap via negation): smaller half
  hi (min-heap): larger half
  Invariants: all lo <= all hi; |len(lo) - len(hi)| <= 1

Complexity: O(log n) addNum, O(1) findMedian
"""

import heapq


class MedianFinder:
    def __init__(self) -> None:
        self.lo: list = []  # max-heap (negated)
        self.hi: list = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        lo_max = -heapq.heappop(self.lo)
        heapq.heappush(self.hi, lo_max)
        if len(self.hi) > len(self.lo):
            hi_min = heapq.heappop(self.hi)
            heapq.heappush(self.lo, -hi_min)

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0


if __name__ == "__main__":
    mf = MedianFinder()
    mf.addNum(1); mf.addNum(2)
    assert mf.findMedian() == 1.5
    mf.addNum(3)
    assert mf.findMedian() == 2.0
    mf2 = MedianFinder()
    mf2.addNum(5)
    assert mf2.findMedian() == 5.0
    mf3 = MedianFinder()
    for x in [5, 3, 8, 1, 4]: mf3.addNum(x)
    assert mf3.findMedian() == 4.0
    print("All tests passed for 295. Find Median from Data Stream!")
