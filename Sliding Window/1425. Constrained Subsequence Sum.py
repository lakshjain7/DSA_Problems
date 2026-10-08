"""
Problem: 1425. Constrained Subsequence Sum
Difficulty: Hard
Topics: Array, Dynamic Programming, Queue, Sliding Window, Heap, Monotonic Queue

Given an integer array nums and an integer k, return the maximum sum of a
non-empty subsequence of that array such that for every two consecutive
integers in the subsequence, nums[i] and nums[j], where i < j, the condition
j - i <= k is satisfied.

A subsequence is obtained by deleting some number of elements (possibly zero)
from the array, leaving the remaining elements in their original order.

Example 1:
    Input: nums = [10,2,-10,5,20], k = 2
    Output: 37
    Explanation: The subsequence is [10, 2, 5, 20].

Example 2:
    Input: nums = [-1,-2,-3], k = 1
    Output: -1

Example 3:
    Input: nums = [10,-2,-10,-5,20], k = 2
    Output: 23

Constraints:
    1 <= k <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4
"""
from collections import deque
from typing import List
import heapq

# Approach (DP + monotonic deque):
#   dp[i] = best sum of a valid subsequence ending at i
#         = nums[i] + max(0, max(dp[i-k..i-1])).
#   The window maximum over the last k dp values is kept by a deque whose dp
#   values are strictly decreasing from front to back. Pop the front when it
#   leaves the window, pop the back while it is <= the new dp.
#
# Complexity: Time O(n) (each index pushed/popped once), Space O(n) for dp
# (O(k) for the deque).


class Solution:
    def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dp = [0] * n
        dq = deque()  # indices, dp values decreasing
        best = float("-inf")
        for i in range(n):
            if dq and dq[0] < i - k:
                dq.popleft()
            dp[i] = nums[i] + (dp[dq[0]] if dq and dp[dq[0]] > 0 else 0)
            while dq and dp[dq[-1]] <= dp[i]:
                dq.pop()
            dq.append(i)
            best = max(best, dp[i])
        return best

    # Alternative: max-heap with lazy deletion. O(n log n) time, O(n) space.
    def constrainedSubsetSumHeap(self, nums: List[int], k: int) -> int:
        heap = []  # (-dp, index)
        best = float("-inf")
        for i, x in enumerate(nums):
            while heap and heap[0][1] < i - k:
                heapq.heappop(heap)
            cur = x + (max(0, -heap[0][0]) if heap else 0)
            heapq.heappush(heap, (-cur, i))
            best = max(best, cur)
        return best


def brute(nums, k):
    n = len(nums)
    dp = [0] * n
    for i in range(n):
        dp[i] = nums[i] + max([0] + [dp[j] for j in range(max(0, i - k), i)])
    return max(dp)


if __name__ == "__main__":
    import random
    s = Solution()
    for f in (s.constrainedSubsetSum, s.constrainedSubsetSumHeap):
        assert f([10, 2, -10, 5, 20], 2) == 37
        assert f([-1, -2, -3], 1) == -1
        assert f([10, -2, -10, -5, 20], 2) == 23
        assert f([5], 1) == 5
        assert f([-5], 1) == -5
        assert f([1, 2, 3, 4], 1) == 10
        assert f([-1, 5, -1, -1, 5], 1) == 8
        random.seed(1)
        for _ in range(300):
            n = random.randint(1, 12)
            nums = [random.randint(-10, 10) for _ in range(n)]
            k = random.randint(1, n)
            assert f(nums, k) == brute(nums, k), (nums, k)
    print("All tests passed.")
