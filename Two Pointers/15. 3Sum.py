"""
15. 3Sum
Difficulty: Medium
Topics: Array, Two Pointers, Sorting

Problem Statement:
Given an integer array nums, return all triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, j != k, and nums[i] + nums[j] + nums[k] == 0.
The solution set must not contain duplicate triplets.

Example 1:
    Input:  nums = [-1, 0, 1, 2, -1, -4]
    Output: [[-1, -1, 2], [-1, 0, 1]]

Example 2:
    Input:  nums = [0, 1, 1]
    Output: []

Example 3:
    Input:  nums = [0, 0, 0]
    Output: [[0, 0, 0]]

Constraints:
    3 <= nums.length <= 3000
    -10^5 <= nums[i] <= 10^5

Approach: Sort + Two Pointers — O(n^2)
"""

from typing import List


def three_sum(nums: List[int]) -> List[List[int]]:
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break

        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result


if __name__ == "__main__":
    assert sorted(three_sum([-1, 0, 1, 2, -1, -4])) == sorted([[-1, -1, 2], [-1, 0, 1]])
    assert three_sum([0, 1, 1]) == []
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
    assert three_sum([]) == []
    assert three_sum([1, 1, 1]) == []
    print("All tests passed!")
