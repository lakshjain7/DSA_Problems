"""
53. Maximum Subarray
Difficulty: Medium
Topics: Array, Divide and Conquer, Dynamic Programming

Problem:
Given an integer array nums, find the subarray with the largest sum, and
return its sum.

Examples:
    Input: nums = [-2,1,-3,4,-1,2,1,-5,4]  Output: 6   ([4,-1,2,1])
    Input: nums = [1]                      Output: 1
    Input: nums = [5,4,-1,7,8]             Output: 23

Constraints:
    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4

Approach (Kadane's algorithm / DP):
    Let best_ending_here[i] be the max sum of a subarray ending at i. Then
    best_ending_here[i] = max(nums[i], best_ending_here[i-1] + nums[i]):
    either extend the previous subarray or start fresh. The answer is the
    maximum over all i. Only the previous value is needed -> O(1) space.

Complexity: Time O(n), Space O(1).
"""
from typing import List


def maxSubArray(nums: List[int]) -> int:
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


# Alternative: divide and conquer. O(n log n) time, O(log n) space.
def maxSubArrayDC(nums: List[int]) -> int:
    def solve(lo: int, hi: int) -> int:
        if lo == hi:
            return nums[lo]
        mid = (lo + hi) // 2
        left_best = float("-inf")
        s = 0
        for i in range(mid, lo - 1, -1):
            s += nums[i]
            left_best = max(left_best, s)
        right_best = float("-inf")
        s = 0
        for i in range(mid + 1, hi + 1):
            s += nums[i]
            right_best = max(right_best, s)
        return max(solve(lo, mid), solve(mid + 1, hi), left_best + right_best)

    return solve(0, len(nums) - 1)


if __name__ == "__main__":
    import random

    for f in (maxSubArray, maxSubArrayDC):
        assert f([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
        assert f([1]) == 1
        assert f([5, 4, -1, 7, 8]) == 23
        assert f([-3]) == -3
        assert f([-3, -1, -2]) == -1
        assert f([0, 0, 0]) == 0
    for _ in range(300):
        a = [random.randint(-10, 10) for _ in range(random.randint(1, 12))]
        brute = max(sum(a[i:j]) for i in range(len(a)) for j in range(i + 1, len(a) + 1))
        assert maxSubArray(a) == brute == maxSubArrayDC(a)
    print("All tests passed")
