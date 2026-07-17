"""
503. Next Greater Element II
Difficulty: Medium
Topics: Array, Stack, Monotonic Stack, Circular Array

Problem Statement
-----------------
Given a circular integer array nums (i.e., the next element of nums[nums.length
- 1] is nums[0]), return the next greater number for every element in nums.

The next greater number of a number x is the first greater number to its
traversing order next in the array, which means you could search circularly to
find its next greater number. If it doesn't exist, return -1 for this number.

Examples
--------
Example 1:
    Input: nums = [1,2,1]
    Output: [2,-1,2]
    Explanation: The first 1's next greater number is 2; the number 2 can't find
    a next greater number; the second 1's next greater number needs to search
    circularly, which is also 2.

Example 2:
    Input: nums = [1,2,3,4,3]
    Output: [2,3,4,-1,4]

Constraints
-----------
    * 1 <= nums.length <= 10^4
    * -10^9 <= nums[i] <= 10^9

Approach 1: Monotonic Decreasing Stack over a Doubled Array (optimal)
--------------------------------------------------------------------
This is the classic "next greater element" pattern, complicated only by the
array being circular. A circular scan is equivalent to walking a linear array of
length 2n, using index i % n to refer back into nums.

Keep a stack of indices whose next greater element has not been found yet; the
values at those indices are non-increasing from bottom to top. Iterate i from 0
to 2n - 1:
    * Let cur = nums[i % n].
    * While the stack is non-empty and nums[stack[-1]] < cur, cur is the next
      greater element for that index -> pop it and set result[index] = cur.
    * Only push real indices during the first pass (i < n); on the second pass we
      just resolve leftovers and never add new indices, which prevents any index
      from being answered twice or looping forever.

Any index still on the stack after both passes has no greater element anywhere
in the circle, so its answer stays -1.

Why it works: doubling the traversal lets every element "see" all other elements
once in circular order. The monotonic stack guarantees that the *first* larger
value encountered (in traversal order) is the one recorded.

Complexity
----------
Time:  O(n) - each index is pushed once and popped at most once across 2n steps.
Space: O(n) - the result array and the stack.

Approach 2: Brute Force
-----------------------
For each index i, walk up to n - 1 steps forward using modular indexing and
return the first strictly greater value, else -1. O(n^2) time, O(1) extra space.
Used below as a reference oracle to validate the optimal solution.
"""

from typing import List


def next_greater_elements(nums: List[int]) -> List[int]:
    """Monotonic stack over a doubled circular scan. O(n) time, O(n) space."""
    n = len(nums)
    result = [-1] * n
    stack: List[int] = []  # holds indices with unresolved next greater element

    for i in range(2 * n):
        cur = nums[i % n]
        while stack and nums[stack[-1]] < cur:
            result[stack.pop()] = cur
        if i < n:
            stack.append(i)

    return result


def next_greater_elements_brute(nums: List[int]) -> List[int]:
    """Brute-force reference. O(n^2) time, O(1) extra space."""
    n = len(nums)
    result = [-1] * n
    for i in range(n):
        for step in range(1, n):
            candidate = nums[(i + step) % n]
            if candidate > nums[i]:
                result[i] = candidate
                break
    return result


if __name__ == "__main__":
    # Example 1
    assert next_greater_elements([1, 2, 1]) == [2, -1, 2]

    # Example 2
    assert next_greater_elements([1, 2, 3, 4, 3]) == [2, 3, 4, -1, 4]

    # Single element - nothing greater
    assert next_greater_elements([5]) == [-1]

    # All equal - no strictly greater element exists
    assert next_greater_elements([7, 7, 7]) == [-1, -1, -1]

    # Strictly increasing then wrap-around resolves the last few
    assert next_greater_elements([1, 2, 3, 4]) == [2, 3, 4, -1]

    # Strictly decreasing - only wrap-around helps earlier elements
    assert next_greater_elements([4, 3, 2, 1]) == [-1, 4, 4, 4]

    # Negative values
    assert next_greater_elements([-1, -2, -3]) == [-1, -1, -1]

    # Cross-check optimal vs brute force
    cases = [
        [1, 2, 1],
        [1, 2, 3, 4, 3],
        [5],
        [7, 7, 7],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [5, 4, 3, 2, 1, 6],
        [100, 1, 11, 1, 120, 111, 123, 1, -1, -100],
    ]
    for case in cases:
        assert next_greater_elements(case) == next_greater_elements_brute(case)

    print("All test cases passed for 503. Next Greater Element II")
