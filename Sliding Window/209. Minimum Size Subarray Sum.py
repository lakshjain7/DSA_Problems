"""
209. Minimum Size Subarray Sum
Difficulty: Medium
Topics: Array, Sliding Window, Prefix Sum, Binary Search

Problem Statement:
Given an array of positive integers `nums` and a positive integer `target`,
return the minimal length of a contiguous subarray of which the sum is
greater than or equal to `target`. If there is no such subarray, return 0
instead.

Examples:
    Input: target = 7, nums = [2,3,1,2,4,3]
    Output: 2
    Explanation: The subarray [4,3] has the minimal length under the
    problem constraint.

    Input: target = 4, nums = [1,4,4]
    Output: 1

    Input: target = 11, nums = [1,1,1,1,1,1,1,1]
    Output: 0

Constraints:
    1 <= target <= 10^9
    1 <= nums.length <= 10^5
    1 <= nums[i] <= 10^4

Approach (Variable-size sliding window):
Since all numbers are positive, the running window sum is monotonically
increasing as the right pointer advances and monotonically decreasing as
the left pointer advances. This monotonicity is exactly what makes a
sliding window valid here: we grow the window by moving `right` forward,
adding nums[right] to `window_sum`. Whenever `window_sum >= target`, the
current window is a valid candidate, so we record its length and then
greedily shrink the window from the left (moving `left` forward and
subtracting nums[left] from window_sum) for as long as the window remains
valid. This greedy shrinking is safe because we only care about the
*minimum* length, and shrinking never has to be "undone" -- once a window
starting further left stops being valid we simply keep growing to the
right again. Every element is added to the window exactly once and removed
at most once, giving linear time.

Complexity Analysis:
    Time:  O(n) -- each pointer (left, right) traverses the array once.
    Space: O(1) -- only a few scalar variables are used.

Alternative Approach (Binary Search on prefix sums):
Build a prefix-sum array `prefix` where prefix[i] = sum(nums[0..i-1]).
Because all nums[i] > 0, `prefix` is strictly increasing, so for every
right endpoint i we can binary search for the smallest index j such that
prefix[i] - prefix[j] >= target, i.e. prefix[j] <= prefix[i] - target.
This gives an O(n log n) solution -- asymptotically worse than the sliding
window, but useful to know because it generalizes to variants where a
two-pointer approach doesn't directly apply (e.g. when combined with other
constraints), and it's a nice illustration of "binary search on a
monotonic derived structure".
    Time:  O(n log n)
    Space: O(n) for the prefix array.
"""

from bisect import bisect_left
from typing import List


def min_sub_array_len(target: int, nums: List[int]) -> int:
    """Return the minimal length of a contiguous subarray with sum >= target.

    Sliding window approach, O(n) time, O(1) space.
    """
    n = len(nums)
    left = 0
    window_sum = 0
    best = n + 1  # sentinel larger than any possible valid length

    for right in range(n):
        window_sum += nums[right]

        while window_sum >= target:
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1

    return best if best <= n else 0


def min_sub_array_len_binary_search(target: int, nums: List[int]) -> int:
    """Alternative O(n log n) solution using prefix sums + binary search."""
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, num in enumerate(nums):
        prefix[i + 1] = prefix[i] + num

    best = n + 1
    for i in range(1, n + 1):
        needed = prefix[i] - target
        # Find leftmost j such that prefix[j] <= needed
        j = bisect_left(prefix, needed + 1) - 1
        # j is the largest index with prefix[j] <= needed (since prefix is
        # strictly increasing because all nums are positive).
        if j >= 0:
            best = min(best, i - j)

    return best if best <= n else 0


if __name__ == "__main__":
    for solve in (min_sub_array_len, min_sub_array_len_binary_search):
        # Example 1
        assert solve(7, [2, 3, 1, 2, 4, 3]) == 2
        # Example 2
        assert solve(4, [1, 4, 4]) == 1
        # Example 3: no subarray reaches target
        assert solve(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
        # Single element exactly equal to target
        assert solve(5, [5]) == 1
        # Single element smaller than target
        assert solve(10, [5]) == 0
        # Entire array required
        assert solve(15, [1, 2, 3, 4, 5]) == 5
        # Large target unreachable
        assert solve(100, [1, 2, 3]) == 0
        # Target satisfied by the very first element
        assert solve(1, [1, 2, 3]) == 1
        # Repeated large values, shortest window is length 1
        assert solve(9, [9, 9, 9]) == 1

    print("All tests passed.")
