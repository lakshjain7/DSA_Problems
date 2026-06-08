"""
15. 3Sum
Difficulty: Medium
Topics: Array, Two Pointers, Sorting

=== PROBLEM ===
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

=== APPROACH: Sort + Two Pointers ===

Key Insight:
    Fix one element (nums[i]) and reduce the problem to finding two numbers
    in the remainder of the array that sum to -nums[i]. Since the array is
    sorted, this two-sum sub-problem is solvable in O(n) with two pointers.

Algorithm:
    1. Sort nums.
    2. For i in range(len(nums) - 2):
         - Skip duplicates: if i > 0 and nums[i] == nums[i-1], continue
         - If nums[i] > 0: break (no three positives can sum to 0)
         - Set left = i+1, right = len(nums)-1
         - While left < right:
             total = nums[i] + nums[left] + nums[right]
             if total == 0:
                 record triplet, advance left & right, skip duplicates
             elif total < 0: left++
             else: right--
    3. Return results

Duplicate handling:
    - Outer loop: skip if nums[i] == nums[i-1] (same fixed element)
    - Inner loop: after recording a triplet, skip while nums[left] == nums[left-1]
      and while nums[right] == nums[right+1]

Complexity:
    Time:  O(n log n) for sort + O(n²) for two-pointer scan → O(n²)
    Space: O(1) extra (output list not counted)
"""

from typing import List


def three_sum(nums: List[int]) -> List[List[int]]:
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        # Skip duplicate values for the fixed element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        # Optimisation: all remaining triples will be positive
        if nums[i] > 0:
            break

        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates on both pointers
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


# ─── Tests ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    assert sorted(three_sum([-1, 0, 1, 2, -1, -4])) == sorted([[-1, -1, 2], [-1, 0, 1]])
    assert three_sum([0, 1, 1]) == []
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
    assert three_sum([]) == []
    # All same, non-zero → no solution
    assert three_sum([1, 1, 1]) == []
    print("All tests passed!")
