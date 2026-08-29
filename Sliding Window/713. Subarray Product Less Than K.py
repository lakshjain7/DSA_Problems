"""
713. Subarray Product Less Than K
Difficulty: Medium
Topics: Array, Sliding Window, Two Pointers, Binary Search

Problem Statement:
Given an array of integers nums and an integer k, return the number of contiguous
subarrays where the product of all the elements in the subarray is strictly less
than k.

Example 1:
    Input:  nums = [10,5,2,6], k = 100
    Output: 8
    Explanation: The 8 subarrays that have product less than 100 are:
    [10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6]
    Note that [10,5,2] is not included because 10 * 5 * 2 = 100 is not < 100.

Example 2:
    Input:  nums = [1,2,3], k = 0
    Output: 0

Constraints:
    - 1 <= nums.length <= 3 * 10^4
    - 1 <= nums[i] <= 1000
    - 0 <= k <= 10^6

--------------------------------------------------------------------------------
Approach (Sliding Window):
Since every element is >= 1, extending a window to the right never decreases the
product, and shrinking from the left never increases it. That monotonic behavior
is exactly what a variable-size sliding window needs.

Maintain a window [left, right] with running `product`. For each `right`:
    1. Multiply `product` by nums[right].
    2. While `product >= k` and `left <= right`, divide out nums[left] and move
       `left` forward. (This restores the window to a valid state.)
    3. Every subarray that ends at `right` and starts anywhere in
       [left, right] now has product < k. There are (right - left + 1) such
       subarrays, so add that count to the answer.

Edge case: if k <= 1, no subarray can have a product strictly less than k
(products are >= 1), so the answer is 0. The while-loop handles this naturally
because the window collapses (left moves past right), contributing 0 each step.

Why counting (right - left + 1) is correct:
When the window is valid, the subarrays ending exactly at `right` are:
[left..right], [left+1..right], ..., [right..right]. Each has product <= the
window product < k (products only shrink as the start moves right). Summing this
per `right` counts every qualifying subarray exactly once, keyed by its right end.

Complexity:
    Time:  O(n) - left and right each advance at most n times total.
    Space: O(1) - constant extra space.

--------------------------------------------------------------------------------
Alternative Approach (Binary search on prefix log-sums):
Take logs so products become sums, build a prefix-sum array, and for each right
binary-search the smallest left with sum in (right] below log(k). Runs in
O(n log n) time and O(n) space, and is more susceptible to floating-point
precision issues, so the sliding window is preferred here.
"""

from typing import List
import math
from bisect import bisect_left


class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k <= 1:
            return 0

        left = 0
        product = 1
        count = 0

        for right, val in enumerate(nums):
            product *= val
            while product >= k:
                product //= nums[left]
                left += 1
            count += right - left + 1

        return count

    def numSubarrayProductLessThanK_binary(self, nums: List[int], k: int) -> int:
        if k <= 1:
            return 0
        # prefix[i] = sum of logs of first i elements
        logk = math.log(k)
        prefix = [0.0]
        for v in nums:
            prefix.append(prefix[-1] + math.log(v))

        count = 0
        # Use a tiny epsilon to counter floating point error for strict "<".
        for right in range(1, len(prefix)):
            target = prefix[right] - logk + 1e-9
            # Smallest index lo such that prefix[lo] > target
            lo = bisect_left(prefix, target, 0, right)
            count += right - lo
        return count


if __name__ == "__main__":
    sol = Solution()

    for method in (
        sol.numSubarrayProductLessThanK,
        sol.numSubarrayProductLessThanK_binary,
    ):
        # Example 1
        assert method([10, 5, 2, 6], 100) == 8
        # Example 2: k = 0 -> nothing qualifies
        assert method([1, 2, 3], 0) == 0
        # k = 1 -> nothing qualifies (products >= 1)
        assert method([1, 1, 1], 1) == 0
        # Single element less than k
        assert method([5], 6) == 1
        # Single element equal to k (not strictly less)
        assert method([5], 5) == 0
        # All ones with k=2: every subarray qualifies -> n*(n+1)/2
        assert method([1, 1, 1, 1], 2) == 10
        # Larger mixed case
        assert method([10, 9, 10, 4, 3, 8, 3, 3, 6, 2, 10, 10, 9, 3], 19) == 18

    print("All tests passed for 713. Subarray Product Less Than K")
