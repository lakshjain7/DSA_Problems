"""
540. Single Element in a Sorted Array
Difficulty: Medium
Topics: Array, Binary Search

Problem:
You are given a sorted array consisting of only integers where every element
appears exactly twice, except for one element which appears exactly once.
Return the single element that appears only once.
Your solution must run in O(log n) time and O(1) space.

Example 1:
    Input: nums = [1,1,2,3,3,4,4,8,8]
    Output: 2

Example 2:
    Input: nums = [3,3,7,7,10,11,11]
    Output: 10

Constraints:
  * 1 <= nums.length <= 10^5
  * 0 <= nums[i] <= 10^5

Approach (binary search on pair alignment):
Before the single element, pairs start at even indices (nums[2k] == nums[2k+1]).
After it, the alignment flips: pairs start at odd indices. So for a mid index
(normalised to even by mid -= mid & 1), if nums[mid] == nums[mid+1] the pairing
is still intact on the left, so the answer lies to the right (lo = mid + 2);
otherwise the single element is at mid or to its left (hi = mid).

Complexity:
  Time:  O(log n)
  Space: O(1)
"""
from typing import List


class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            mid -= mid & 1  # make mid even
            if nums[mid] == nums[mid + 1]:
                lo = mid + 2
            else:
                hi = mid
        return nums[lo]

    # Alternative: XOR of all elements (O(n) time, O(1) space).
    def singleNonDuplicateXor(self, nums: List[int]) -> int:
        res = 0
        for x in nums:
            res ^= x
        return res


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 1, 2, 3, 3, 4, 4, 8, 8], 2),
        ([3, 3, 7, 7, 10, 11, 11], 10),
        ([1], 1),
        ([1, 2, 2], 1),
        ([1, 1, 2], 2),
        ([0, 0, 1, 1, 2], 2),
        ([5, 6, 6, 7, 7], 5),
        ([1, 1, 2, 2, 3, 3, 4, 5, 5], 4),
    ]
    for nums, expected in cases:
        assert s.singleNonDuplicate(nums) == expected, nums
        assert s.singleNonDuplicateXor(nums) == expected, nums
    big = [i // 2 for i in range(200000)]
    big.pop()  # last value now appears once
    assert s.singleNonDuplicate(big) == big[-1]
    print("All tests passed.")
