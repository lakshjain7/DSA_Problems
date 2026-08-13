"""
480. Sliding Window Median
Difficulty: Hard
Topics: Array, Hash Table, Sliding Window, Heap (Priority Queue)

Problem Statement
-----------------
The median is the middle value in an ordered integer list. If the size of the
list is even, there is no middle value, so the median is the mean of the two
middle values.

    For arr = [2, 3, 4], the median is 3.
    For arr = [1, 2, 3, 4], the median is (2 + 3) / 2 = 2.5.

You are given an integer array `nums` and an integer `k`. There is a sliding
window of size `k` which is moving from the very left of the array to the very
right. You can only see the `k` numbers in the window. Each time the sliding
window moves right by one position.

Return the median array for each window in the original array. Answers within
10^-5 of the actual value will be accepted.

Examples
--------
Example 1:
    Input:  nums = [1,3,-1,-3,5,3,6,7], k = 3
    Output: [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
    Windows:
        [1  3  -1] -3  5  3  6  7   ->  median  1
         1 [3  -1  -3] 5  3  6  7   ->  median -1
         1  3 [-1  -3  5] 3  6  7   ->  median -1
         1  3  -1 [-3  5  3] 6  7   ->  median  3
         1  3  -1  -3 [5  3  6] 7   ->  median  5
         1  3  -1  -3  5 [3  6  7]  ->  median  6

Example 2:
    Input:  nums = [1,2,3,4,2,3,1,4,2], k = 3
    Output: [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]

Constraints
-----------
    1 <= k <= nums.length <= 10^5
    -2^31 <= nums[i] <= 2^31 - 1

Approach: Two heaps + lazy deletion
-----------------------------------
To read the median of a window in O(1) we maintain two heaps:
    - `small`: a max-heap (stored as negatives) holding the smaller half.
    - `large`: a min-heap holding the larger half.
We keep the invariant (over live elements) that small holds the smaller
ceil(k/2) values and large holds the larger floor(k/2) values. Then the median
is small's top (odd k) or the average of the two tops (even k).

The challenge with a sliding window is removing the element that leaves the
window - heaps don't support arbitrary deletion in O(log n). We use *lazy
deletion*: a hash map `to_remove` counts elements scheduled for deletion. We
only physically pop an element from a heap top when it is actually the top
(otherwise it stays buried until it surfaces). A per-step `balance` counter
tracks the net change to small's live size as one element leaves and one enters,
so a single corrective move restores the size invariant.

Algorithm per slide:
    1. Schedule the outgoing value nums[i-k] for removal; note which heap it
       lived in (balance -= 1 if it was in small, else += 1).
    2. Insert the incoming value nums[i] into small or large by comparing with
       small's top (balance += 1 / -= 1 accordingly).
    3. Apply exactly one rebalancing move if balance != 0.
    4. Clean deleted values off both heap tops, then read the median.

Why it works: `balance` counts only live elements, so after the single
corrective move the live sizes are back to ceil(k/2) and floor(k/2); pruning the
tops guarantees the values read for the median are actually in the window.

Complexity
----------
Time:  O(n log n) - each element pushed/popped a constant number of times.
Space: O(k)       - heaps and the deletion map hold O(k) live/pending items.

Alternative (below): a simpler O(n * k) sorted-list approach using bisect,
which is clean and fast enough for moderate inputs and easy to verify against.
"""

import heapq
from bisect import insort, bisect_left
from collections import defaultdict
from typing import List


def median_sliding_window(nums: List[int], k: int) -> List[float]:
    """Two-heap solution with lazy deletion. O(n log n) time.

    Invariant (in terms of *live* elements): small holds the smaller
    ceil(k/2) values, large holds the larger floor(k/2) values.
    """
    small: List[int] = []   # max-heap via negation (smaller half)
    large: List[int] = []   # min-heap (larger half)
    to_remove = defaultdict(int)

    def clean_tops() -> None:
        """Pop any top elements that are scheduled for deletion."""
        while small and to_remove[-small[0]] > 0:
            to_remove[-small[0]] -= 1
            heapq.heappop(small)
        while large and to_remove[large[0]] > 0:
            to_remove[large[0]] -= 1
            heapq.heappop(large)

    def median() -> float:
        if k % 2 == 1:
            return float(-small[0])
        return (-small[0] + large[0]) / 2.0

    # Build the first window: small = ceil(k/2), large = floor(k/2).
    for x in nums[:k]:
        heapq.heappush(small, -x)
    for _ in range(k // 2):
        heapq.heappush(large, -heapq.heappop(small))

    result: List[float] = [median()]

    for i in range(k, len(nums)):
        out = nums[i - k]
        inc = nums[i]
        to_remove[out] += 1

        # balance = (net change to small's live count) as we swap out/in.
        balance = -1 if (small and out <= -small[0]) else 1

        # Insert the incoming value.
        if small and inc <= -small[0]:
            heapq.heappush(small, -inc)
            balance += 1
        else:
            heapq.heappush(large, inc)
            balance -= 1

        # Exactly one corrective move restores the size invariant.
        if balance > 0:      # small has one too many live elements
            heapq.heappush(large, -heapq.heappop(small))
        elif balance < 0:    # small has one too few
            heapq.heappush(small, -heapq.heappop(large))

        clean_tops()
        result.append(median())

    return result


# ---------------------------------------------------------------------------
# Alternative approach: maintain a sorted window with bisect. O(n * k) because
# each insert/delete into the list is O(k), but very simple and a great oracle
# to test the heap version against.
# ---------------------------------------------------------------------------
def median_sliding_window_bisect(nums: List[int], k: int) -> List[float]:
    window = sorted(nums[:k])
    medians: List[float] = []

    def median() -> float:
        if k % 2 == 1:
            return float(window[k // 2])
        return (window[k // 2 - 1] + window[k // 2]) / 2.0

    medians.append(median())
    for i in range(k, len(nums)):
        # remove nums[i-k]
        window.pop(bisect_left(window, nums[i - k]))
        # insert nums[i]
        insort(window, nums[i])
        medians.append(median())
    return medians


if __name__ == "__main__":
    def approx_equal(a: List[float], b: List[float]) -> bool:
        return len(a) == len(b) and all(abs(x - y) < 1e-5 for x, y in zip(a, b))

    for fn in (median_sliding_window, median_sliding_window_bisect):
        assert approx_equal(
            fn([1, 3, -1, -3, 5, 3, 6, 7], 3),
            [1.0, -1.0, -1.0, 3.0, 5.0, 6.0],
        ), fn.__name__
        assert approx_equal(
            fn([1, 2, 3, 4, 2, 3, 1, 4, 2], 3),
            [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0],
        ), fn.__name__
        assert approx_equal(fn([1, 2, 3, 4], 1), [1.0, 2.0, 3.0, 4.0]), fn.__name__
        assert approx_equal(fn([1, 2, 3, 4], 4), [2.5]), fn.__name__
        assert approx_equal(fn([5], 1), [5.0]), fn.__name__
        assert approx_equal(fn([1, 4, 2, 3], 2), [2.5, 3.0, 2.5]), fn.__name__
        # duplicates should be handled correctly by lazy deletion
        assert approx_equal(fn([2, 2, 2, 2, 2], 3), [2.0, 2.0, 2.0]), fn.__name__

    # Randomized cross-check: heap solution vs. bisect oracle.
    import random
    random.seed(42)
    for _ in range(300):
        n = random.randint(1, 40)
        arr = [random.randint(-20, 20) for _ in range(n)]
        kk = random.randint(1, n)
        assert approx_equal(
            median_sliding_window(arr, kk),
            median_sliding_window_bisect(arr, kk),
        ), (arr, kk)

    print("All tests passed.")
