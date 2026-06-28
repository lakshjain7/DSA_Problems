"""
Problem: 41. First Missing Positive
Difficulty: Hard
Topics: Arrays, Hash Map

Problem Statement:
    Given an unsorted integer array nums, return the smallest missing positive integer.
    You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.

Examples:
    Input: nums = [1, 2, 0]
    Output: 3

    Input: nums = [3, 4, -1, 1]
    Output: 2

    Input: nums = [7, 8, 9, 11, 12]
    Output: 1

Constraints:
    - 1 <= nums.length <= 10^5
    - -2^31 <= nums[i] <= 2^31 - 1

Approach (Index as Hash Map):
    Key insight: for an array of length n, the answer must be in [1, n+1].
      - If 1..n are all present, answer is n+1.
      - Otherwise some value in 1..n is missing.

    We use the array itself as a hash map:
      - For each value v in [1, n], place it at index v-1 (i.e. nums[v-1] = v).
      - After rearranging, scan for the first index i where nums[i] != i+1.
        That i+1 is our answer.

    Step 1: Rearrange — while nums[i] is in [1,n] and not already in correct spot,
            swap nums[i] with nums[nums[i]-1].
    Step 2: Scan for first mismatch.

Complexity:
    Time:  O(n) — each element is swapped at most once into its final position
    Space: O(1) auxiliary (in-place)

Alternative Approach (O(n) time, O(n) space):
    Use a set. Add all nums to a set, then scan 1, 2, 3... until a miss.
    Simpler but uses O(n) extra space.
"""

from typing import List


def firstMissingPositive(nums: List[int]) -> int:
    n = len(nums)

    # Place each number v in [1, n] at index v-1
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            # Swap nums[i] to its correct position
            correct = nums[i] - 1
            nums[i], nums[correct] = nums[correct], nums[i]

    # First index where value doesn't match → that's the missing positive
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1

    return n + 1


def firstMissingPositive_set(nums: List[int]) -> int:
    """Alternative O(n) space solution using a set."""
    num_set = set(nums)
    i = 1
    while i in num_set:
        i += 1
    return i


if __name__ == "__main__":
    # Basic examples
    assert firstMissingPositive([1, 2, 0]) == 3
    assert firstMissingPositive([3, 4, -1, 1]) == 2
    assert firstMissingPositive([7, 8, 9, 11, 12]) == 1

    # Edge cases
    assert firstMissingPositive([1]) == 2
    assert firstMissingPositive([2]) == 1
    assert firstMissingPositive([1, 2, 3]) == 4
    assert firstMissingPositive([-1, -2, -3]) == 1
    assert firstMissingPositive([0]) == 1
    assert firstMissingPositive([1, 1]) == 2

    # Larger input
    assert firstMissingPositive(list(range(1, 101))) == 101
    assert firstMissingPositive(list(range(2, 101))) == 1

    # Alt solution
    assert firstMissingPositive_set([1, 2, 0]) == 3
    assert firstMissingPositive_set([3, 4, -1, 1]) == 2
    assert firstMissingPositive_set([7, 8, 9, 11, 12]) == 1

    print("All tests passed!")
