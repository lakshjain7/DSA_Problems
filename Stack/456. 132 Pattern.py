"""
456. 132 Pattern
Difficulty: Medium
Topics: Array, Binary Search, Stack, Monotonic Stack, Ordered Set

Problem:
Given an array of n integers nums, a 132 pattern is a subsequence of three
integers nums[i], nums[j] and nums[k] such that i < j < k and
nums[i] < nums[k] < nums[j].
Return true if there is a 132 pattern in nums, otherwise, return false.

Example 1:
    Input: nums = [1,2,3,4]
    Output: false
Example 2:
    Input: nums = [3,1,4,2]
    Output: true   (1, 4, 2)
Example 3:
    Input: nums = [-1,3,2,0]
    Output: true   (-1,3,2), (-1,3,0), (-1,2,0)

Constraints:
    n == nums.length
    1 <= n <= 2 * 10^5
    -10^9 <= nums[i] <= 10^9

Approach (monotonic decreasing stack, scan right to left):
    Treat nums[k] as the "2" and keep `third` = the largest candidate "2" seen
    so far that has a bigger "3" to its left (within the scanned suffix).
    Scan from the right. If nums[i] < third, then nums[i] is the "1" and we
    have a pattern. Otherwise pop every stack element smaller than nums[i];
    each popped value has nums[i] as a larger element before it, so it is a
    valid "2" - keep the maximum popped as `third`. Then push nums[i].
    Maximizing "2" is optimal because a larger `third` makes nums[i] < third
    easier to satisfy, and the stack stays decreasing so each element is
    popped at most once.

Complexity:
    Time:  O(n) - each element pushed/popped once.
    Space: O(n) for the stack.
"""
from typing import List


class Solution:
    def find132pattern(self, nums: List[int]) -> bool:
        stack: List[int] = []
        third = float("-inf")
        for x in reversed(nums):
            if x < third:
                return True
            while stack and stack[-1] < x:
                third = stack.pop()
            stack.append(x)
        return False

    # Alternative: prefix minimum as "1" + stack of (value) candidates, scanning left to right.
    def find132patternPrefixMin(self, nums: List[int]) -> bool:
        stack: List[tuple] = []  # (value, min_before_it) with decreasing values
        cur_min = nums[0]
        for x in nums[1:]:
            while stack and x >= stack[-1][0]:
                stack.pop()
            if stack and x > stack[-1][1]:
                return True
            stack.append((x, cur_min))
            cur_min = min(cur_min, x)
        return False

    # Brute force O(n^2) with prefix minimum, useful for cross-checking.
    def find132patternBrute(self, nums: List[int]) -> bool:
        n = len(nums)
        mn = float("inf")
        for j in range(n):
            for k in range(j + 1, n):
                if mn < nums[k] < nums[j]:
                    return True
            mn = min(mn, nums[j])
        return False


if __name__ == "__main__":
    import random
    s = Solution()
    cases = [
        ([1, 2, 3, 4], False),
        ([3, 1, 4, 2], True),
        ([-1, 3, 2, 0], True),
        ([1], False),
        ([1, 2], False),
        ([1, 0, 1, -4, -3], False),
        ([3, 5, 0, 3, 4], True),
        ([2, 2, 2, 2], False),
        ([4, 3, 2, 1], False),
        ([1, 3, 2], True),
    ]
    for nums, exp in cases:
        assert s.find132pattern(nums) == exp, nums
        assert s.find132patternPrefixMin(nums) == exp, nums
        assert s.find132patternBrute(nums) == exp, nums
    random.seed(1)
    for _ in range(2000):
        a = [random.randint(-6, 6) for _ in range(random.randint(1, 9))]
        b = s.find132patternBrute(a)
        assert s.find132pattern(a) == b, a
        assert s.find132patternPrefixMin(a) == b, a
    print("All tests passed")
