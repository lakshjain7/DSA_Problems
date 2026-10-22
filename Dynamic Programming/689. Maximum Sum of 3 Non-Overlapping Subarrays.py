"""
689. Maximum Sum of 3 Non-Overlapping Subarrays
Difficulty: Hard
Topics: Array, Dynamic Programming, Sliding Window

Problem:
Given an integer array nums and an integer k, find three non-overlapping
subarrays of length k with maximum sum and return them. Return the result as a
list of indices representing the starting position of each interval
(0-indexed). If there are multiple answers, return the lexicographically
smallest one.

Example 1:
    Input: nums = [1,2,1,2,6,7,5,1], k = 2
    Output: [0,3,5]
    Explanation: Subarrays [1,2], [2,6], [7,5] starting at 0, 3, 5.

Example 2:
    Input: nums = [1,2,1,2,1,2,1,2,1], k = 2
    Output: [0,2,4]

Constraints:
  * 1 <= nums.length <= 2 * 10^4
  * 1 <= nums[i] < 2^16
  * 1 <= k <= floor(nums.length / 3)

Approach (prefix windows + best-left / best-right, middle enumeration):
Compute w[i] = sum of the window nums[i:i+k]. Fix the middle window start m
(k <= m <= n-2k). We need the best window entirely to the left (start <= m-k)
and the best entirely to the right (start >= m+k).
  * left[i]  = start of the best window in w[0..i] (earliest on ties)
  * right[i] = start of the best window in w[i..] (earliest on ties)
Then the answer maximises w[left[m-k]] + w[m] + w[right[m+k]]. Using strict
'>' for updates and earliest-tie choices yields the lexicographically
smallest answer.

Complexity:
  Time:  O(n)
  Space: O(n)
"""
from typing import List


class Solution:
    def maxSumOfThreeSubarrays(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        m = n - k + 1
        w = [0] * m
        cur = sum(nums[:k])
        w[0] = cur
        for i in range(1, m):
            cur += nums[i + k - 1] - nums[i - 1]
            w[i] = cur

        left = [0] * m
        best = 0
        for i in range(m):
            if w[i] > w[best]:
                best = i
            left[i] = best

        right = [0] * m
        best = m - 1
        for i in range(m - 1, -1, -1):
            if w[i] >= w[best]:  # >= keeps the earliest start on ties
                best = i
            right[i] = best

        ans, best_sum = [], -1
        for mid in range(k, m - k):
            l, r = left[mid - k], right[mid + k]
            total = w[l] + w[mid] + w[r]
            if total > best_sum:
                best_sum = total
                ans = [l, mid, r]
        return ans

    # Alternative: DP over (count of subarrays used, position) - brute-force
    # reference used for cross-checking in the tests (O(n^3) enumeration).
    def bruteForce(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        pre = [0]
        for x in nums:
            pre.append(pre[-1] + x)
        w = [pre[i + k] - pre[i] for i in range(n - k + 1)]
        best, ans = -1, []
        for a in range(len(w)):
            for b in range(a + k, len(w)):
                for c in range(b + k, len(w)):
                    t = w[a] + w[b] + w[c]
                    if t > best:
                        best, ans = t, [a, b, c]
        return ans


if __name__ == "__main__":
    import random

    s = Solution()
    assert s.maxSumOfThreeSubarrays([1, 2, 1, 2, 6, 7, 5, 1], 2) == [0, 3, 5]
    assert s.maxSumOfThreeSubarrays([1, 2, 1, 2, 1, 2, 1, 2, 1], 2) == [0, 2, 4]
    assert s.maxSumOfThreeSubarrays([1, 1, 1], 1) == [0, 1, 2]
    assert s.maxSumOfThreeSubarrays([4, 3, 2, 1], 1) == [0, 1, 2]
    assert s.maxSumOfThreeSubarrays([7, 7, 7, 7, 7, 7], 2) == [0, 2, 4]
    random.seed(1)
    for _ in range(300):
        n = random.randint(3, 14)
        k = random.randint(1, n // 3)
        nums = [random.randint(1, 5) for _ in range(n)]
        assert s.maxSumOfThreeSubarrays(nums, k) == s.bruteForce(nums, k), (nums, k)
    print("All tests passed.")
