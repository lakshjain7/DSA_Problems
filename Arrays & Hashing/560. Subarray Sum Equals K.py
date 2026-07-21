"""
560. Subarray Sum Equals K
Difficulty: Medium
Topics: Array, Hash Table, Prefix Sum

Problem Statement
-----------------
Given an array of integers `nums` and an integer `k`, return the total number
of subarrays whose sum equals to `k`.

A subarray is a contiguous non-empty sequence of elements within an array.

Examples
--------
Example 1:
    Input:  nums = [1, 1, 1], k = 2
    Output: 2
    Explanation: The subarrays [1,1] (indices 0-1) and [1,1] (indices 1-2)
                 both sum to 2.

Example 2:
    Input:  nums = [1, 2, 3], k = 3
    Output: 2
    Explanation: [1,2] and [3].

Constraints
-----------
    1 <= nums.length <= 2 * 10^4
    -1000 <= nums[i] <= 1000
    -10^7 <= k <= 10^7

Approach: Prefix Sum + Hash Map
-------------------------------
Let prefix[i] be the sum of nums[0..i-1] (prefix sum up to but not including i).
A subarray nums[j..i-1] has sum == k  iff  prefix[i] - prefix[j] == k, i.e.
prefix[j] == prefix[i] - k.

So while scanning left to right and maintaining the running prefix sum, the
number of valid subarrays ending at the current position equals the number of
earlier prefix sums equal to (running_sum - k). We keep those counts in a hash
map.

Why it works: every contiguous subarray is uniquely identified by a pair of
prefix-sum boundaries (j, i) with j < i. Fixing the right boundary i and asking
"how many left boundaries j give sum k" reduces to a single hash-map lookup,
turning an O(n^2) enumeration into O(n).

We seed the map with {0: 1} to account for subarrays that start at index 0
(prefix sum of the empty prefix is 0).

Complexity
----------
Time:  O(n) - one pass, O(1) hash-map work per element.
Space: O(n) - up to n distinct prefix sums stored.

Note: the brute-force O(n^2) alternative is included below for contrast.
"""

from collections import defaultdict
from typing import List


def subarray_sum(nums: List[int], k: int) -> int:
    """Count subarrays summing to k using prefix sums and a hash map. O(n)."""
    count = 0
    running = 0
    seen = defaultdict(int)
    seen[0] = 1  # empty prefix
    for x in nums:
        running += x
        count += seen[running - k]
        seen[running] += 1
    return count


def subarray_sum_bruteforce(nums: List[int], k: int) -> int:
    """O(n^2) reference: extend each start index and count sums equal to k."""
    n = len(nums)
    count = 0
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += nums[j]
            if total == k:
                count += 1
    return count


if __name__ == "__main__":
    tests = [
        ([1, 1, 1], 2, 2),
        ([1, 2, 3], 3, 2),
        ([1], 0, 0),
        ([1], 1, 1),
        ([-1, -1, 1], 0, 1),
        ([0, 0, 0, 0], 0, 10),          # C(5,2) pairs of boundaries = 10
        ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
        ([1, -1, 0], 0, 3),             # [1,-1], [1,-1,0], [0]
        ([100, -100, 100], 0, 2),
    ]
    for nums, k, expected in tests:
        got = subarray_sum(nums, k)
        assert got == expected, f"subarray_sum({nums}, {k}) = {got}, expected {expected}"
        # cross-check the two implementations agree
        brute = subarray_sum_bruteforce(nums, k)
        assert brute == expected, f"bruteforce({nums}, {k}) = {brute}, expected {expected}"

    print("All tests passed for 560. Subarray Sum Equals K")
