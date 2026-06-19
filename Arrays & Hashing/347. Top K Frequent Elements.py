"""
347. Top K Frequent Elements
Difficulty: Medium
Topics: Array, Hash Table, Heap (Priority Queue), Bucket Sort, Counting

Problem Statement:
Given an integer array `nums` and an integer `k`, return the k most frequent
elements. You may return the answer in any order.

Examples:
    Input:  nums = [1,1,1,2,2,3], k = 2
    Output: [1,2]

    Input:  nums = [1], k = 1
    Output: [1]

Constraints:
    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4
    k is in the range [1, number of unique elements]
    The answer is guaranteed to be unique.

Approach (Bucket Sort):
Count frequencies with a hash map. A value's frequency can be at most n, so
create n+1 buckets where bucket[f] holds all values appearing exactly f times.
Walk the buckets from highest frequency to lowest, collecting values until we
have k. This avoids any comparison sorting — frequency itself is the index —
giving guaranteed linear time.

Complexity:
    Time:  O(n) — one counting pass + one bucket pass.
    Space: O(n) — counter and buckets.

Alternative (Min-Heap of size k):
Count frequencies, then push (freq, value) pairs into a min-heap capped at
size k; pop the smallest whenever the heap exceeds k. Whatever remains are the
k most frequent. O(n log k) time, O(n + k) space.
"""

from collections import Counter
import heapq
from typing import List


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """Bucket sort solution — O(n)."""
    counts = Counter(nums)
    buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]
    for value, freq in counts.items():
        buckets[freq].append(value)

    result: List[int] = []
    for freq in range(len(buckets) - 1, 0, -1):
        for value in buckets[freq]:
            result.append(value)
            if len(result) == k:
                return result
    return result


def top_k_frequent_heap(nums: List[int], k: int) -> List[int]:
    """Alternative: min-heap of size k — O(n log k)."""
    counts = Counter(nums)
    heap: List[tuple] = []
    for value, freq in counts.items():
        heapq.heappush(heap, (freq, value))
        if len(heap) > k:
            heapq.heappop(heap)
    return [value for _, value in heap]


if __name__ == "__main__":
    for solve in (top_k_frequent, top_k_frequent_heap):
        assert sorted(solve([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
        assert solve([1], 1) == [1]
        assert sorted(solve([5, 5, 5, 5], 1)) == [5]
        assert sorted(solve([1, 2, 3, 4], 4)) == [1, 2, 3, 4]
        assert sorted(solve([-1, -1, -2, -2, -2, 3], 2)) == [-2, -1]
        assert sorted(solve([0, 0, 0, 7, 7, 9], 2)) == [0, 7]
        big = [10] * 100 + [20] * 50 + [30] * 25 + [40]
        assert sorted(solve(big, 3)) == [10, 20, 30]
    print("All tests passed for 347. Top K Frequent Elements")
