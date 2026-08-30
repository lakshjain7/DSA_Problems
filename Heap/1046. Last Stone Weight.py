"""
1046. Last Stone Weight
Difficulty: Easy/Medium (NeetCode 150 - Heap / Priority Queue)
Topics: Array, Heap (Priority Queue)

PROBLEM STATEMENT
-----------------
You are given an array of integers `stones` where `stones[i]` is the weight of
the i-th stone.

We are playing a game with the stones. On each turn, we choose the two heaviest
stones and smash them together. Suppose the heaviest two stones have weights x
and y with x <= y. The result of this smash is:
  - If x == y, both stones are destroyed, and
  - If x != y, the stone of weight x is destroyed, and the stone of weight y has
    new weight y - x.

At the end of the game, there is at most one stone left. Return the weight of
the last remaining stone. If there are no stones left, return 0.

EXAMPLES
--------
Example 1:
  Input:  stones = [2,7,4,1,8,1]
  Output: 1
  Explanation:
    We combine 7 and 8 to get 1, so the array converts to [2,4,1,1,1].
    We combine 2 and 4 to get 2, so the array converts to [2,1,1,1].
    We combine 2 and 1 to get 1, so the array converts to [1,1,1].
    We combine 1 and 1 to get 0, so the array converts to [1], the last stone.

Example 2:
  Input:  stones = [1]
  Output: 1

CONSTRAINTS
-----------
  - 1 <= stones.length <= 30
  - 1 <= stones[i] <= 1000

APPROACH (Max-Heap)
-------------------
On every turn we need the two largest stones. A max-heap gives us O(log n)
access to the largest element. Python's `heapq` is a MIN-heap, so we negate the
weights when pushing and negate again when popping to simulate a max-heap.

Algorithm:
  1. Build a max-heap of all negated stone weights.
  2. While more than one stone remains:
       - Pop the two heaviest stones (y >= x).
       - If they differ, push back (y - x) as the new stone.
  3. Return the remaining stone's weight, or 0 if the heap is empty.

Why it works: smashing only ever depends on the current two heaviest stones, and
the residual (y - x) is itself just another stone that re-enters the pool. The
heap keeps the "two heaviest" query correct after every mutation.

COMPLEXITY
----------
  Time:  O(n log n) - each of up to n-1 smashes does a constant number of
         heap pops/pushes, each O(log n). Building the heap is O(n).
  Space: O(n) for the heap.
"""

from typing import List
import heapq


def last_stone_weight(stones: List[int]) -> int:
    """Return the weight of the last remaining stone (0 if none) using a max-heap."""
    max_heap = [-s for s in stones]
    heapq.heapify(max_heap)

    while len(max_heap) > 1:
        y = -heapq.heappop(max_heap)  # heaviest
        x = -heapq.heappop(max_heap)  # second heaviest
        if y != x:
            heapq.heappush(max_heap, -(y - x))

    return -max_heap[0] if max_heap else 0


def last_stone_weight_sorted(stones: List[int]) -> int:
    """
    Alternative: keep the list sorted and re-insert the residual with binary
    insertion. Simpler to reason about but slower per step because insertion is
    O(n). Time O(n^2), Space O(1) extra. Useful as a cross-check for tests.
    """
    import bisect

    arr = sorted(stones)
    while len(arr) > 1:
        y = arr.pop()
        x = arr.pop()
        if y != x:
            bisect.insort(arr, y - x)
    return arr[0] if arr else 0


if __name__ == "__main__":
    # Example cases
    assert last_stone_weight([2, 7, 4, 1, 8, 1]) == 1
    assert last_stone_weight([1]) == 1

    # All stones cancel out -> 0
    assert last_stone_weight([2, 2]) == 0
    assert last_stone_weight([3, 3, 3, 3]) == 0

    # Two distinct stones
    assert last_stone_weight([10, 4]) == 6

    # Larger / random cross-check against the sorted implementation
    import random
    for _ in range(500):
        n = random.randint(1, 30)
        stones = [random.randint(1, 1000) for _ in range(n)]
        assert last_stone_weight(stones) == last_stone_weight_sorted(stones)

    # Edge: maximum values
    assert last_stone_weight([1000, 1000]) == 0
    assert last_stone_weight([1000]) == 1000

    print("All tests passed for 1046. Last Stone Weight")
