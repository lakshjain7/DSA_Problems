"""
1696. Jump Game VI
Difficulty: Medium
Topics: Array, Dynamic Programming, Queue, Sliding Window, Monotonic Queue, Heap

Problem:
You are given a 0-indexed integer array nums and an integer k.

You are initially standing at index 0. In one move, you can jump at most k steps
forward without going outside the boundaries of the array. That is, you can jump
from index i to any index in the range [i + 1, min(n - 1, i + k)] inclusive.

You want to reach the last index of the array (index n - 1). Your score is the sum
of all nums[j] for each index j you visited in the array.

Return the maximum score you can get.

Example 1:
    Input: nums = [1,-1,-2,4,-7,3], k = 2
    Output: 7
    Explanation: Choose the subsequence [1,-1,4,3]. The sum is 7.

Example 2:
    Input: nums = [10,-5,-2,4,0,3], k = 3
    Output: 17
    Explanation: Choose the subsequence [10,4,3]. The sum is 17.

Example 3:
    Input: nums = [1,-5,-20,4,-1,3,-6,-3], k = 2
    Output: 0

Constraints:
    1 <= nums.length, k <= 10^5
    -10^4 <= nums[i] <= 10^4

Approach (DP + monotonic deque):
    dp[i] = nums[i] + max(dp[i-k .. i-1]) is the best score of any path ending at i.
    Computing that max naively costs O(k) per index. Instead keep a deque of indices
    whose dp values are strictly decreasing from front to back:
      * pop the front if it has slid out of the window (index < i - k),
      * the front is then the window maximum, so dp[i] = nums[i] + dp[front],
      * pop from the back every index whose dp <= dp[i] (it can never again be a
        better predecessor than i, which is both newer and at least as large),
      * push i.
    Each index enters and leaves the deque once, so the whole pass is linear.

Complexity:
    Time:  O(n) - every index is pushed and popped at most once.
    Space: O(n) for dp (O(k) for the deque).

Alternative:
    Max-heap of (-dp[j], j), lazily discarding entries with j < i - k.
    O(n log n) time, O(n) space.
"""

from collections import deque
import heapq
from typing import List


class Solution:
    def maxResult(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dp = [0] * n
        dp[0] = nums[0]
        dq = deque([0])  # indices, dp values strictly decreasing
        for i in range(1, n):
            while dq[0] < i - k:
                dq.popleft()
            dp[i] = nums[i] + dp[dq[0]]
            while dq and dp[dq[-1]] <= dp[i]:
                dq.pop()
            dq.append(i)
        return dp[-1]

    def maxResultHeap(self, nums: List[int], k: int) -> int:
        heap = [(-nums[0], 0)]
        best = nums[0]
        for i in range(1, len(nums)):
            while heap[0][1] < i - k:
                heapq.heappop(heap)
            best = nums[i] - heap[0][0]
            heapq.heappush(heap, (-best, i))
        return best


def _brute(nums: List[int], k: int) -> int:
    n = len(nums)
    dp = [float("-inf")] * n
    dp[0] = nums[0]
    for i in range(1, n):
        dp[i] = nums[i] + max(dp[max(0, i - k):i])
    return dp[-1]


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([1, -1, -2, 4, -7, 3], 2, 7),
        ([10, -5, -2, 4, 0, 3], 3, 17),
        ([1, -5, -20, 4, -1, 3, -6, -3], 2, 0),
        ([5], 1, 5),                 # single element
        ([-3], 4, -3),               # single negative
        ([-1, -2, -3, -4], 1, -10),  # forced to visit every index
        ([-1, -2, -3, -4], 3, -5),   # jump straight to the end
        ([1, 2, 3], 10, 6),          # k larger than n, take all positives
    ]
    for nums, k, exp in cases:
        assert s.maxResult(nums, k) == exp, (nums, k)
        assert s.maxResultHeap(nums, k) == exp, (nums, k)

    random.seed(0)
    for _ in range(300):
        n = random.randint(1, 25)
        nums = [random.randint(-20, 20) for _ in range(n)]
        k = random.randint(1, 8)
        e = _brute(nums, k)
        assert s.maxResult(nums, k) == e
        assert s.maxResultHeap(nums, k) == e

    big = [random.randint(-10**4, 10**4) for _ in range(10**5)]
    assert s.maxResult(big, 500) == s.maxResultHeap(big, 500)
    print("All tests passed!")
