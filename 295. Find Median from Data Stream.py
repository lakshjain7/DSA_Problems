"""
Problem Number: 295
Title: Find Median from Data Stream
Difficulty: Hard
Topics: Two Pointers, Design, Sorting, Heap (Priority Queue), Data Stream

Problem Statement:
    The median is the middle value in an ordered integer list. If the size of the
    list is even, there is no middle value, and the median is the mean of the two
    middle values.

    For example, for arr = [2,3,4], the median is 3.
    For arr = [2,3], the median is (2 + 3) / 2 = 2.5.

    Implement the MedianFinder class:
    - MedianFinder()    Initializes the MedianFinder object.
    - void addNum(int num)  Adds the integer num from the data stream to the data structure.
    - double findMedian()   Returns the median of all elements so far. Answers within
                            10^-5 of the actual answer will be accepted.

Examples:
    Input:  ["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]
            [[],[1],[2],[],[3],[]]
    Output: [null,null,null,1.5,null,2.0]
    Explanation:
        MedianFinder medianFinder = new MedianFinder();
        medianFinder.addNum(1);   // arr = [1]
        medianFinder.addNum(2);   // arr = [1, 2]
        medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
        medianFinder.addNum(3);   // arr = [1, 2, 3]
        medianFinder.findMedian(); // return 2.0

Constraints:
    - -10^5 <= num <= 10^5
    - There will be at least one element in the data structure before calling findMedian.
    - At most 5 * 10^4 calls will be made to addNum and findMedian.

Follow-up:
    - If all integer numbers from the stream are in the range [0, 100], how would
      you optimize your solution? (Use a counting array / bucket sort.)
    - If 99% of all integer numbers from the stream are in the range [0, 100], how
      would you handle this? (Track outliers separately.)

Approach (Two Heaps):
    Maintain two heaps that partition the stream into two halves:
    - max_heap (lo): stores the SMALLER half. Python's heapq is a min-heap, so we
      negate values to simulate a max-heap.
    - min_heap (hi): stores the LARGER half as a standard min-heap.

    Invariants maintained after every addNum:
    1. Every element in lo <= every element in hi.
    2. |len(lo) - len(hi)| <= 1  (lo is allowed to have at most 1 extra element).

    To find the median:
    - If sizes are equal -> median = (lo_max + hi_min) / 2.0
    - If lo is larger   -> median = lo_max  (the single middle element).

    Insertion procedure:
    1. Push num into lo (max-heap). Pop the max from lo.
    2. Push that max into hi (min-heap). This ensures lo <= hi.
    3. If hi is now larger than lo, pop min from hi and push back to lo.
       This re-balances so lo can have at most 1 extra element.

Complexity:
    Time:  O(log n) per addNum, O(1) per findMedian
    Space: O(n) -- all elements stored across the two heaps

Alternative Approach (Sorted List via SortedList from sortedcontainers):
    Maintain a sorted list and track the median index. Insertion is O(log n) with
    binary search + O(n) shift. findMedian is O(1). This is simpler to code but
    has O(n) insertion in Python without sortedcontainers library.
"""

import heapq


class MedianFinder:
    """
    Online median finder using two heaps.

    lo: max-heap (stored as negated values in a min-heap)
        contains the smaller half of elements.
    hi: min-heap
        contains the larger half of elements.
    """

    def __init__(self) -> None:
        self.lo: list[int] = []  # max-heap (negated)
        self.hi: list[int] = []  # min-heap

    def addNum(self, num: int) -> None:
        """
        Add a number to the data structure in O(log n).

        Args:
            num: Integer to add from the stream.
        """
        # Step 1: push to lo (max-heap via negation), then pop the max
        heapq.heappush(self.lo, -num)
        lo_max = -heapq.heappop(self.lo)

        # Step 2: push that max to hi (ensures lo_max <= hi elements)
        heapq.heappush(self.hi, lo_max)

        # Step 3: re-balance if hi has more elements than lo
        if len(self.hi) > len(self.lo):
            hi_min = heapq.heappop(self.hi)
            heapq.heappush(self.lo, -hi_min)

    def findMedian(self) -> float:
        """
        Return the median of all numbers added so far in O(1).

        Returns:
            The median as a float.
        """
        if len(self.lo) > len(self.hi):
            # lo has the extra middle element
            return float(-self.lo[0])
        # Equal sizes: average the two middle values
        return (-self.lo[0] + self.hi[0]) / 2.0


# ---------------------------------------------------------------------------
# Alternative: expose the same interface but use a simple sorted list
# (useful for understanding / correctness checking in tests)
# ---------------------------------------------------------------------------

class MedianFinderNaive:
    """O(n log n) naive version using sorted insertion -- for verification only."""

    def __init__(self) -> None:
        self.data: list[int] = []

    def addNum(self, num: int) -> None:
        # Binary search insertion to keep sorted
        lo, hi = 0, len(self.data)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.data[mid] < num:
                lo = mid + 1
            else:
                hi = mid
        self.data.insert(lo, num)

    def findMedian(self) -> float:
        n = len(self.data)
        if n % 2 == 1:
            return float(self.data[n // 2])
        return (self.data[n // 2 - 1] + self.data[n // 2]) / 2.0


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example from problem statement
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    assert mf.findMedian() == 1.5, f"Expected 1.5, got {mf.findMedian()}"
    mf.addNum(3)
    assert mf.findMedian() == 2.0, f"Expected 2.0, got {mf.findMedian()}"

    # Single element
    mf2 = MedianFinder()
    mf2.addNum(5)
    assert mf2.findMedian() == 5.0, "Expected 5.0"

    # Two elements
    mf3 = MedianFinder()
    mf3.addNum(3)
    mf3.addNum(7)
    assert mf3.findMedian() == 5.0, "Expected 5.0"

    # Odd count
    mf4 = MedianFinder()
    for x in [5, 3, 8, 1, 4]:
        mf4.addNum(x)
    # Sorted: [1, 3, 4, 5, 8] -> median = 4
    assert mf4.findMedian() == 4.0, f"Expected 4.0, got {mf4.findMedian()}"

    # Even count
    mf5 = MedianFinder()
    for x in [6, 2, 4, 8]:
        mf5.addNum(x)
    # Sorted: [2, 4, 6, 8] -> median = (4+6)/2 = 5.0
    assert mf5.findMedian() == 5.0, f"Expected 5.0, got {mf5.findMedian()}"

    # Negative numbers
    mf6 = MedianFinder()
    for x in [-5, -3, -1]:
        mf6.addNum(x)
    assert mf6.findMedian() == -3.0, f"Expected -3.0, got {mf6.findMedian()}"

    # Verify heap solution matches naive solution on a longer stream
    import random
    random.seed(42)
    heap_mf = MedianFinder()
    naive_mf = MedianFinderNaive()

    for _ in range(200):
        val = random.randint(-1000, 1000)
        heap_mf.addNum(val)
        naive_mf.addNum(val)
        heap_result = heap_mf.findMedian()
        naive_result = naive_mf.findMedian()
        assert abs(heap_result - naive_result) < 1e-9, \
            f"Mismatch: heap={heap_result}, naive={naive_result}"

    print("All tests passed for 295. Find Median from Data Stream!")
