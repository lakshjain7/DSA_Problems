"""
442. Find All Duplicates in an Array
Difficulty: Medium
Topics: Array, Hash Table

Given an integer array nums of length n where all the integers of nums are in
the range [1, n] and each integer appears at most twice, return an array of
all the integers that appear twice.
You must write an algorithm that runs in O(n) time and uses only constant
auxiliary space, excluding the space needed to store the output.

Example 1:
    Input: nums = [4,3,2,7,8,2,3,1]   Output: [2,3]
Example 2:
    Input: nums = [1,1,2]             Output: [1]
Example 3:
    Input: nums = [1]                 Output: []

Constraints:
    n == nums.length
    1 <= n <= 10^5
    1 <= nums[i] <= n
    Each element appears once or twice.

Approach (index as hash / sign marking):
    Values are in [1, n], so value v maps to index v-1. For each value v, flip
    the sign of nums[v-1]. If that cell is already negative, v was seen before,
    so it is a duplicate. Restore the array afterwards.

Complexity:
    Time:  O(n)
    Space: O(1) extra (output excluded)

Alternative: a hash set of seen values (O(n) extra space).
"""
from typing import List


class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        res = []
        for x in nums:
            v = abs(x)
            if nums[v - 1] < 0:
                res.append(v)
            else:
                nums[v - 1] = -nums[v - 1]
        for i in range(len(nums)):  # restore input
            nums[i] = abs(nums[i])
        return res

    def findDuplicatesSet(self, nums: List[int]) -> List[int]:
        seen, res = set(), []
        for x in nums:
            if x in seen:
                res.append(x)
            seen.add(x)
        return res


if __name__ == "__main__":
    sol = Solution()
    cases = [([4, 3, 2, 7, 8, 2, 3, 1], [2, 3]), ([1, 1, 2], [1]), ([1], []),
             ([1, 2, 3], []), ([2, 2], [2]), ([1, 1], [1]),
             ([3, 3, 1, 1, 2], [1, 3])]
    for nums, exp in cases:
        orig = nums[:]
        assert sorted(sol.findDuplicates(nums)) == sorted(exp), (orig, exp)
        assert nums == orig  # input restored
        assert sorted(sol.findDuplicatesSet(orig[:])) == sorted(exp)
    print("All tests passed.")
