"""
995. Minimum Number of K Consecutive Bit Flips
Difficulty: Hard
Topics: Array, Bit Manipulation, Queue, Sliding Window, Prefix Sum

Problem:
You are given a binary array nums and an integer k.
A k-bit flip is choosing a subarray of length k from nums and simultaneously
changing every 0 in the subarray to 1, and every 1 in the subarray to 0.
Return the minimum number of k-bit flips required so that there is no 0 in the
array. If it is not possible, return -1.
A subarray is a contiguous part of an array.

Example 1:
  Input: nums = [0,1,0], k = 1
  Output: 2
  Explanation: Flip nums[0], then flip nums[2].

Example 2:
  Input: nums = [1,1,0], k = 2
  Output: -1
  Explanation: No matter how we flip subarrays of size 2, we cannot make the
  array become [1,1,1].

Example 3:
  Input: nums = [0,0,0,1,0,1,1,0], k = 3
  Output: 3
  Explanation:
    Flip nums[0],nums[1],nums[2]: nums becomes [1,1,1,1,0,1,1,0]
    Flip nums[4],nums[5],nums[6]: nums becomes [1,1,1,1,1,0,0,0]
    Flip nums[5],nums[6],nums[7]: nums becomes [1,1,1,1,1,1,1,1]

Constraints:
  1 <= nums.length <= 10^5
  1 <= k <= nums.length

Approach (Greedy + sliding window of active flips):
  Scan left to right. The leftmost 0 can only be fixed by a flip that STARTS
  at it (any flip starting earlier would disturb already-fixed positions, and
  flipping the same window twice is useless), so the greedy choice is forced
  → the greedy answer is optimal and unique.
  Simulating each flip naively costs O(k). Instead keep `active` = parity of
  flips currently covering index i (flips started in (i-k, i]). The effective
  bit is nums[i] ^ active. When a flip window slides out (i >= k and a flip
  started at i-k), toggle `active` back. We mark a started flip by setting
  nums[start] = 2 (in-place marker), so no extra memory is needed.
  If a 0 needs flipping but i + k > n, the window doesn't fit → return -1.

Complexity:
  Time:  O(n) — one pass, O(1) work per index.
  Space: O(1) extra (marks are written into nums; a copy is made here to keep
         the caller's list untouched — use the in-place version for true O(1)).

Alternative (Difference array / queue):
  Keep a deque of start indices of active flips (or a diff array where
  diff[i+k] cancels a flip started at i). len(deque) % 2 is the current
  parity. O(n) time, O(k) / O(n) space; often easier to reason about.
"""
from collections import deque
from typing import List


class Solution:
    def minKBitFlips(self, nums: List[int], k: int) -> int:
        a = nums[:]  # avoid mutating caller input
        n = len(a)
        active = 0
        flips = 0
        for i in range(n):
            if i >= k and a[i - k] == 2:
                active ^= 1  # flip started at i-k no longer covers i
            if a[i] ^ active == 0:  # effective bit is 0 → must flip here
                if i + k > n:
                    return -1
                a[i] = 2
                active ^= 1
                flips += 1
        return flips

    def minKBitFlips_queue(self, nums: List[int], k: int) -> int:
        q: deque = deque()  # start indices of flips covering current index
        flips = 0
        for i, x in enumerate(nums):
            if q and q[0] + k <= i:
                q.popleft()
            if (x + len(q)) % 2 == 0:
                if i + k > len(nums):
                    return -1
                q.append(i)
                flips += 1
        return flips


if __name__ == "__main__":
    import itertools

    s = Solution()
    cases = [
        ([0, 1, 0], 1, 2),
        ([1, 1, 0], 2, -1),
        ([0, 0, 0, 1, 0, 1, 1, 0], 3, 3),
        ([1], 1, 0),
        ([0], 1, 1),
        ([1, 1, 1], 3, 0),
        ([0, 0, 0], 3, 1),
        ([0, 0], 2, 1),
        ([0, 1], 2, -1),
        ([0, 1, 1], 3, -1),
        ([1, 0, 0, 1], 2, 1),
    ]
    for nums, k, exp in cases:
        orig = nums[:]
        assert s.minKBitFlips(nums, k) == exp, (nums, k, exp)
        assert nums == orig, "input must not be mutated"
        assert s.minKBitFlips_queue(nums, k) == exp, (nums, k, exp)

    # exhaustive brute force on small arrays (each window flipped 0/1 times)
    def brute(nums, k):
        n = len(nums)
        best = -1
        starts = range(n - k + 1)
        for mask in range(1 << len(starts)):
            a = nums[:]
            for st in starts:
                if mask >> st & 1:
                    for j in range(st, st + k):
                        a[j] ^= 1
            if all(a):
                c = bin(mask).count("1")
                best = c if best == -1 else min(best, c)
        return best

    for n in range(1, 9):
        for bits in itertools.product([0, 1], repeat=n):
            for k in range(1, n + 1):
                arr = list(bits)
                b = brute(arr, k)
                assert s.minKBitFlips(arr, k) == b == s.minKBitFlips_queue(arr, k), (arr, k)

    print("All tests passed for 995. Minimum Number of K Consecutive Bit Flips")
