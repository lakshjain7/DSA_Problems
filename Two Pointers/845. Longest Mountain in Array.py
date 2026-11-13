"""
845. Longest Mountain in Array
Difficulty: Medium
Topics: Array, Two Pointers, Dynamic Programming, Enumeration

Problem:
You may recall that an array arr is a mountain array if and only if:
  - arr.length >= 3
  - There exists some index i (0-indexed) with 0 < i < arr.length - 1 such that:
      arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
      arr[i] > arr[i + 1] > ... > arr[arr.length - 1]

Given an integer array arr, return the length of the longest subarray, which is a
mountain. Return 0 if there is no mountain subarray.

Example 1:
  Input: arr = [2,1,4,7,3,2,5]
  Output: 5
  Explanation: The largest mountain is [1,4,7,3,2] which has length 5.

Example 2:
  Input: arr = [2,2,2]
  Output: 0
  Explanation: There is no mountain.

Constraints:
  1 <= arr.length <= 10^4
  0 <= arr[i] <= 10^4

Follow up: Can you solve it using only one pass and O(1) space?

Approach (Two Pointers, single pass):
  Let `base` be the left end of a candidate mountain. From `base`:
    1. Walk `end` up while arr[end] < arr[end + 1]   (strictly ascending side).
    2. If we actually climbed (end > base), walk `end` down while
       arr[end] > arr[end + 1]                       (strictly descending side).
    3. If we also descended, arr[base..end] is a mountain → update the answer.
    4. The next mountain cannot start before `end` (any element inside the
       current ascent/descent belongs to this slope), so set base = max(end, base + 1).
  Every index is visited by `end` at most a constant number of times, so the
  whole scan is linear. Plateaus (equal neighbours) stop both walks, which
  correctly breaks mountains since they must be strictly monotone.

Complexity:
  Time:  O(n) — each pointer only moves forward.
  Space: O(1).

Alternative (Up/Down DP arrays):
  up[i]   = length of strictly increasing run ending at i (excluding i).
  down[i] = length of strictly decreasing run starting at i (excluding i).
  For every peak with up[i] > 0 and down[i] > 0, the mountain length is
  up[i] + down[i] + 1. O(n) time, O(n) space.
"""
from typing import List


class Solution:
    def longestMountain(self, arr: List[int]) -> int:
        n = len(arr)
        best = 0
        base = 0
        while base < n:
            end = base
            # climb the ascending side
            if end + 1 < n and arr[end] < arr[end + 1]:
                while end + 1 < n and arr[end] < arr[end + 1]:
                    end += 1
                # descend the other side
                if end + 1 < n and arr[end] > arr[end + 1]:
                    while end + 1 < n and arr[end] > arr[end + 1]:
                        end += 1
                    best = max(best, end - base + 1)
            base = max(end, base + 1)
        return best

    def longestMountain_dp(self, arr: List[int]) -> int:
        n = len(arr)
        up = [0] * n
        down = [0] * n
        for i in range(1, n):
            if arr[i] > arr[i - 1]:
                up[i] = up[i - 1] + 1
        for i in range(n - 2, -1, -1):
            if arr[i] > arr[i + 1]:
                down[i] = down[i + 1] + 1
        best = 0
        for i in range(n):
            if up[i] and down[i]:
                best = max(best, up[i] + down[i] + 1)
        return best


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([2, 1, 4, 7, 3, 2, 5], 5),
        ([2, 2, 2], 0),
        ([1], 0),
        ([1, 2], 0),
        ([1, 2, 3], 0),            # only ascending
        ([3, 2, 1], 0),            # only descending
        ([1, 3, 2], 3),
        ([0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0], 11),
        ([1, 2, 2, 1], 0),         # plateau at peak
        ([0, 2, 0, 2, 0], 3),      # shared valley
        ([875, 884, 239, 731, 723, 685], 4),
        ([1, 1, 0, 0, 1, 0], 3),
    ]
    for arr, exp in cases:
        assert s.longestMountain(arr) == exp, (arr, s.longestMountain(arr), exp)
        assert s.longestMountain_dp(arr) == exp, (arr, exp)

    # randomized cross-check against brute force
    def brute(a):
        best = 0
        for i in range(len(a)):
            for j in range(i + 2, len(a)):
                sub = a[i:j + 1]
                p = sub.index(max(sub))
                if 0 < p < len(sub) - 1 and all(sub[k] < sub[k + 1] for k in range(p)) \
                        and all(sub[k] > sub[k + 1] for k in range(p, len(sub) - 1)):
                    best = max(best, len(sub))
        return best

    for _ in range(500):
        a = [random.randint(0, 4) for _ in range(random.randint(1, 12))]
        assert s.longestMountain(a) == s.longestMountain_dp(a) == brute(a), a

    print("All tests passed for 845. Longest Mountain in Array")
