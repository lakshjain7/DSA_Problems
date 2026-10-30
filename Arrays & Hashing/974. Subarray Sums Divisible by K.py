"""
974. Subarray Sums Divisible by K
Difficulty: Medium
Topics: Array, Hash Table, Prefix Sum

Problem:
    Given an integer array nums and an integer k, return the number of
    non-empty subarrays that have a sum divisible by k.
    A subarray is a contiguous part of an array.

Examples:
    Input: nums = [4,5,0,-2,-3,1], k = 5
    Output: 7
    Input: nums = [5], k = 9
    Output: 0

Constraints:
    1 <= nums.length <= 3 * 10^4
    -10^4 <= nums[i] <= 10^4
    2 <= k <= 10^4

Approach:
    Let P[i] be the prefix sum of the first i elements. The subarray
    (j, i] has sum P[i] - P[j], divisible by k iff P[i] % k == P[j] % k.
    So count, for each prefix, how many earlier prefixes share its remainder.
    Python's % already yields a non-negative remainder for negative sums.
    Seed the count with remainder 0 -> 1 (the empty prefix).

Complexity:
    Time O(n), Space O(min(n, k)).
"""
from collections import defaultdict
from typing import List


def subarraysDivByK(nums: List[int], k: int) -> int:
    counts = defaultdict(int)
    counts[0] = 1
    prefix = 0
    result = 0
    for x in nums:
        prefix = (prefix + x) % k
        result += counts[prefix]
        counts[prefix] += 1
    return result


def subarraysDivByK_array(nums: List[int], k: int) -> int:
    """Alternative: fixed-size array of remainder counts (size k)."""
    counts = [0] * k
    counts[0] = 1
    prefix = 0
    result = 0
    for x in nums:
        prefix = (prefix + x) % k
        result += counts[prefix]
        counts[prefix] += 1
    return result


def _brute(nums: List[int], k: int) -> int:
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i, n) if sum(nums[i:j + 1]) % k == 0)


if __name__ == "__main__":
    import random
    for f in (subarraysDivByK, subarraysDivByK_array):
        assert f([4, 5, 0, -2, -3, 1], 5) == 7
        assert f([5], 9) == 0
        assert f([5], 5) == 1
        assert f([0, 0, 0], 2) == 6
        assert f([-1, 2, 9], 2) == 2
        assert f([-5], 5) == 1
    random.seed(1)
    for _ in range(300):
        arr = [random.randint(-20, 20) for _ in range(random.randint(1, 15))]
        k = random.randint(2, 9)
        assert subarraysDivByK(arr, k) == subarraysDivByK_array(arr, k) == _brute(arr, k)
    print("All tests passed.")
