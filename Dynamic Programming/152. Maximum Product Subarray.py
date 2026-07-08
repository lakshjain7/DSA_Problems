"""
152. Maximum Product Subarray
Difficulty: Medium
Topics: Array, Dynamic Programming

Problem Statement
-----------------
Given an integer array nums, find a subarray that has the largest product,
and return the product.

The test cases are generated so that the answer will fit in a 32-bit
integer.

Example 1:
    Input:  nums = [2,3,-2,4]
    Output: 6
    Explanation: [2,3] has the largest product 6.

Example 2:
    Input:  nums = [-2,0,-1]
    Output: 0
    Explanation: The result cannot be 2, because [-2,-1] is not a subarray.

Constraints:
    1 <= nums.length <= 2 * 10^4
    -10 <= nums[i] <= 10
    The product of any subarray of nums is guaranteed to fit in a 32-bit
    integer.


Approach: Track both the running max AND min product (DP)
---------------------------------------------------------
For a sum-based "maximum subarray" (Kadane), we only need the best sum
ending at each index. Products are trickier because a negative number
flips large/small: the smallest (most negative) product so far can become
the largest after multiplying by another negative. Zeros reset everything.

So at each index i we maintain two quantities for subarrays ending at i:
    cur_max = largest product of a subarray ending at i
    cur_min = smallest product of a subarray ending at i

Transition for value v = nums[i]:
    candidates = {v, cur_max * v, cur_min * v}
    new_max = max(candidates)
    new_min = min(candidates)

Including v alone handles the reset after a zero (and the start). Taking
the max/min over the three candidates handles the sign flip caused by a
negative v. We keep a global answer = max over all cur_max.

Why it works: any subarray ending at i either is just [v], or extends the
best (or worst) subarray ending at i-1. Because a negative v turns the
worst into the best, we must carry both extremes forward.

Complexity
----------
Time:  O(n) - single pass.
Space: O(1) - only a constant number of running variables.
"""

from typing import List


def maxProduct(nums: List[int]) -> int:
    result = nums[0]
    cur_max = cur_min = nums[0]

    for v in nums[1:]:
        # v can flip the roles of max and min, so compute all candidates.
        candidates = (v, cur_max * v, cur_min * v)
        cur_max = max(candidates)
        cur_min = min(candidates)
        result = max(result, cur_max)

    return result


# -----------------------------------------------------------------------------
# Alternative approach: prefix / suffix product sweep.
# The max product subarray always sits at one end of a run between zeros,
# so scanning products left->right and right->left (resetting on zero)
# and taking the best value seen covers every case, including odd counts
# of negatives.
# -----------------------------------------------------------------------------
def maxProductPrefixSuffix(nums: List[int]) -> int:
    n = len(nums)
    result = nums[0]

    prefix = suffix = 0
    for i in range(n):
        prefix = (prefix or 1) * nums[i]
        suffix = (suffix or 1) * nums[n - 1 - i]
        result = max(result, prefix, suffix)

    return result


if __name__ == "__main__":
    # Provided examples.
    assert maxProduct([2, 3, -2, 4]) == 6
    assert maxProduct([-2, 0, -1]) == 0

    # Single element (including negative).
    assert maxProduct([3]) == 3
    assert maxProduct([-5]) == -5

    # All negatives: even count -> whole array; odd count -> drop one end.
    assert maxProduct([-2, -3, -4]) == 12          # -3 * -4
    assert maxProduct([-1, -2, -3, -4]) == 24       # whole array

    # Zeros split the array into independent segments.
    assert maxProduct([0, 2]) == 2
    assert maxProduct([-2, 0, -1, -3]) == 3         # -1 * -3
    assert maxProduct([2, -5, -2, -4, 3]) == 24     # -2 * -4 * 3

    # A single negative surrounded by positives.
    assert maxProduct([1, 2, -1, 4, 5]) == 20       # 4 * 5

    # Cross-check both approaches against a brute-force oracle.
    import random

    def brute(nums: List[int]) -> int:
        best = nums[0]
        for i in range(len(nums)):
            prod = 1
            for j in range(i, len(nums)):
                prod *= nums[j]
                best = max(best, prod)
        return best

    random.seed(1)
    for _ in range(2000):
        arr = [random.randint(-5, 5) for _ in range(random.randint(1, 8))]
        expected = brute(arr)
        assert maxProduct(arr) == expected, (arr, maxProduct(arr), expected)
        assert maxProductPrefixSuffix(arr) == expected, arr

    print("All tests passed for 152. Maximum Product Subarray")
