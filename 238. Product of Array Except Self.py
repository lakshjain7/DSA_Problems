"""
Problem 238: Product of Array Except Self
Difficulty: Medium
Topics: Arrays, Prefix Products

Problem Statement:
Given an integer array nums, return an array answer such that answer[i] is equal to
the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
You must write an algorithm that runs in O(n) time and without using the division operation.

Follow-up: Can you solve it in O(1) extra space (output array doesn't count)?

Examples:
    Input: nums = [1,2,3,4]
    Output: [24,12,8,6]

    Input: nums = [−1,1,0,−3,3]
    Output: [0,0,9,0,0]

Constraints:
    - 2 <= nums.length <= 10^5
    - -30 <= nums[i] <= 30
    - The product of any prefix or suffix fits in a 32-bit integer.
    - Follow up: O(1) extra space

Approach (O(n) time, O(1) extra space):
    answer[i] = (product of all elements to the LEFT of i)
              * (product of all elements to the RIGHT of i)

    Pass 1 (left to right): Fill answer[i] with prefix product up to (not including) i.
    Pass 2 (right to left): Multiply answer[i] by a running suffix product,
                             updating the suffix as we go.

    No division needed, no extra array beyond the output.

Complexity:
    Time:  O(n) — two linear passes
    Space: O(1) extra — output array not counted per problem statement
"""

from typing import List


def product_except_self(nums: List[int]) -> List[int]:
    """O(n) time, O(1) extra space using prefix/suffix accumulation."""
    n = len(nums)
    answer = [1] * n

    # Pass 1: answer[i] = product of nums[0..i-1]
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    # Pass 2: multiply answer[i] by product of nums[i+1..n-1]
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer


# Alternative Approach (O(n) space, clearer):
# Build explicit prefix[] and suffix[] arrays, then answer[i] = prefix[i] * suffix[i].
# Same time complexity but uses O(n) extra space — useful for clarity.

def product_except_self_explicit(nums: List[int]) -> List[int]:
    """O(n) time and space — explicit prefix/suffix arrays."""
    n = len(nums)
    prefix = [1] * n
    suffix = [1] * n

    for i in range(1, n):
        prefix[i] = prefix[i - 1] * nums[i - 1]
    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i + 1] * nums[i + 1]

    return [prefix[i] * suffix[i] for i in range(n)]


if __name__ == "__main__":
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

    # Edge cases
    assert product_except_self([2, 3]) == [3, 2]
    assert product_except_self([1, 1, 1, 1]) == [1, 1, 1, 1]
    assert product_except_self([0, 0]) == [0, 0]
    assert product_except_self([1, 0]) == [0, 1]
    assert product_except_self([-1, -1, -1]) == [1, 1, 1]

    # Both approaches should agree
    test_cases = [
        [1, 2, 3, 4],
        [-1, 1, 0, -3, 3],
        [2, 3],
        [0, 0, 0],
        [5, 2, 3, 1, 4],
    ]
    for tc in test_cases:
        assert product_except_self(tc) == product_except_self_explicit(tc), f"Mismatch on {tc}"

    print("All tests passed for 238. Product of Array Except Self")
