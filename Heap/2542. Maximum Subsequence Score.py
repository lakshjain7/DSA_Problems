"""
2542. Maximum Subsequence Score
Difficulty: Medium
Topics: Array, Greedy, Sorting, Heap (Priority Queue)

Problem:
You are given two 0-indexed integer arrays `nums1` and `nums2` of equal
length n and a positive integer k. You must choose a subsequence of indices
from nums1 of length k.

For chosen indices i0, i1, ..., i(k-1), your score is defined as:
    (nums1[i0] + nums1[i1] + ... + nums1[i(k-1)]) * min(nums2[i0], ..., nums2[i(k-1)])

Return the maximum possible score.

A subsequence of indices of an array is a set that can be derived from the
set {0, 1, ..., n-1} by deleting some or no elements.

Example 1:
    Input: nums1 = [1,3,3,2], nums2 = [2,1,3,4], k = 3
    Output: 12
    Explanation: The four possible subsequence scores are:
    - indices 0,1,2 -> (1+3+3) * min(2,1,3) = 7
    - indices 0,1,3 -> (1+3+2) * min(2,1,4) = 6
    - indices 0,2,3 -> (1+3+2) * min(2,3,4) = 12
    - indices 1,2,3 -> (3+3+2) * min(1,3,4) = 8
    Therefore, we return the max score, which is 12.

Example 2:
    Input: nums1 = [4,2,3,1,1], nums2 = [7,5,10,9,6], k = 1
    Output: 30
    Explanation: Choosing index 2 is optimal: nums1[2] * nums2[2] = 3 * 10 = 30.

Constraints:
    n == nums1.length == nums2.length
    1 <= n <= 10^5
    0 <= nums1[i], nums2[j] <= 10^5
    1 <= k <= n

Approach (Sort by multiplier desc + Min-Heap of top-k sums):
    Fix which index supplies the minimum of nums2. If we process pairs in
    descending order of nums2, then when we reach pair i, every pair seen so
    far has nums2 >= nums2[i], so nums2[i] is the minimum of any group drawn
    from the processed prefix that includes i. To maximise the sum part, we
    want the k largest nums1 values among the prefix (including i).

    Maintain a min-heap of the k largest nums1 values seen so far plus their
    running sum. After pushing nums1[i], if the heap exceeds k, pop the
    smallest. Whenever the heap holds exactly k items, candidate score is
    heap_sum * nums2[i].

    Subtlety: if nums1[i] itself was popped, the group's real minimum is
    larger than nums2[i], so the candidate underestimates a score we already
    counted earlier — it never overestimates, so the max is still correct.

Complexity:
    Time:  O(n log n) — sort plus n heap operations of O(log k).
    Space: O(n) for the sorted pairs, O(k) for the heap.

Alternative (Brute force over combinations):
    Enumerate all C(n, k) subsets — exponential, only useful as a test oracle.
"""

import heapq
from itertools import combinations
from typing import List


def max_score(nums1: List[int], nums2: List[int], k: int) -> int:
    pairs = sorted(zip(nums2, nums1), reverse=True)
    heap: List[int] = []
    running = 0
    best = 0
    for mult, val in pairs:
        heapq.heappush(heap, val)
        running += val
        if len(heap) > k:
            running -= heapq.heappop(heap)
        if len(heap) == k:
            best = max(best, running * mult)
    return best


def max_score_brute(nums1: List[int], nums2: List[int], k: int) -> int:
    best = 0
    for idx in combinations(range(len(nums1)), k):
        best = max(best, sum(nums1[i] for i in idx) * min(nums2[i] for i in idx))
    return best


if __name__ == "__main__":
    import random

    assert max_score([1, 3, 3, 2], [2, 1, 3, 4], 3) == 12
    assert max_score([4, 2, 3, 1, 1], [7, 5, 10, 9, 6], 1) == 30
    assert max_score([5], [3], 1) == 15                       # single element
    assert max_score([0, 0, 0], [5, 5, 5], 2) == 0            # all-zero sums
    assert max_score([1, 2, 3], [0, 0, 0], 3) == 0            # zero multipliers
    assert max_score([2, 1, 14, 12], [11, 7, 13, 6], 3) == 168
    assert max_score([1, 1, 1, 1], [1, 2, 3, 4], 4) == 4      # k == n

    for _ in range(400):
        n = random.randint(1, 8)
        a = [random.randint(0, 10) for _ in range(n)]
        b = [random.randint(0, 10) for _ in range(n)]
        kk = random.randint(1, n)
        assert max_score(a, b, kk) == max_score_brute(a, b, kk), (a, b, kk)

    print("All tests passed for 2542. Maximum Subsequence Score")
