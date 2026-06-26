"""
Problem Number: 167
Title: Two Sum II - Input Array Is Sorted
Difficulty: Medium
Topics: Array, Two Pointers, Binary Search

Problem Statement:
Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order,
find two numbers such that they add up to a specific target number. Let these two numbers be
numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers, index1 and index2, added by one as an integer array
[index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You may not use the same
element twice.

Your solution must use only constant extra space.

Examples:
    Input: numbers = [2,7,11,15], target = 9
    Output: [1,2]
    Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2.

    Input: numbers = [2,3,4], target = 6
    Output: [1,3]

    Input: numbers = [-1,0], target = -1
    Output: [1,2]

Constraints:
    2 <= numbers.length <= 3 * 10^4
    -1000 <= numbers[i] <= 1000
    numbers is sorted in non-decreasing order.
    -1000 <= target <= 1000
    The tests are generated such that there is exactly one solution.

Approach:
    Use two pointers starting at both ends of the array. Since the array is sorted:
    - If numbers[left] + numbers[right] == target, we found our answer.
    - If the sum is too small, move left pointer right to increase the sum.
    - If the sum is too large, move right pointer left to decrease the sum.

    This works because sorting guarantees that moving left right can only increase the sum
    and moving right left can only decrease it, so we converge to the answer in O(n).

Complexity:
    Time:  O(n) — single pass with two pointers
    Space: O(1) — only two pointer variables
"""

from typing import List


def twoSum(numbers: List[int], target: int) -> List[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]  # 1-indexed
        elif s < target:
            left += 1
        else:
            right -= 1
    return []  # guaranteed to find solution


# Alternative approach: Binary Search
# For each element numbers[i], binary search for (target - numbers[i]) in the
# remaining right portion. O(n log n) time, O(1) space — slower than two pointers.
def twoSumBinarySearch(numbers: List[int], target: int) -> List[int]:
    import bisect
    for i, num in enumerate(numbers):
        complement = target - num
        j = bisect.bisect_left(numbers, complement, i + 1)
        if j < len(numbers) and numbers[j] == complement:
            return [i + 1, j + 1]
    return []


if __name__ == "__main__":
    # Basic cases
    assert twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert twoSum([2, 3, 4], 6) == [1, 3]
    assert twoSum([-1, 0], -1) == [1, 2]

    # Negative numbers
    assert twoSum([-3, -2, -1, 0], -5) == [1, 2]

    # Target at the ends
    assert twoSum([1, 2, 3, 4, 5], 9) == [4, 5]
    assert twoSum([1, 2, 3, 4, 5], 3) == [1, 2]

    # Binary search alternative
    assert twoSumBinarySearch([2, 7, 11, 15], 9) == [1, 2]
    assert twoSumBinarySearch([2, 3, 4], 6) == [1, 3]

    print("All tests passed!")
