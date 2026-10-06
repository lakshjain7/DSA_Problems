"""
719. Find K-th Smallest Pair Distance
Difficulty: Hard
Topics: Array, Two Pointers, Binary Search, Sorting

The distance of a pair of integers a and b is defined as the absolute
difference between a and b. Given an integer array nums and an integer k,
return the k-th smallest distance among all the pairs nums[i] and nums[j]
where 0 <= i < j < nums.length.

Example 1:
    Input: nums = [1,3,1], k = 1
    Output: 0
Example 2:
    Input: nums = [1,1,1], k = 2
    Output: 0
Example 3:
    Input: nums = [1,6,1], k = 3
    Output: 5

Constraints:
    n == nums.length
    2 <= n <= 10^4
    0 <= nums[i] <= 10^6
    1 <= k <= n * (n - 1) / 2

Approach (binary search on the answer + two pointers):
    Sort nums. For a candidate distance d, the number of pairs with distance
    <= d is monotonic in d and can be counted in O(n) with a sliding window:
    for each right index j, advance left until nums[j]-nums[left] <= d and add
    j-left. Binary search the smallest d whose count >= k.

Complexity:
    Time: O(n log n + n log M), M = max - min   Space: O(1) extra
"""
from typing import List


def smallestDistancePair(nums: List[int], k: int) -> int:
    nums = sorted(nums)
    n = len(nums)

    def count_le(d: int) -> int:
        cnt = left = 0
        for right in range(n):
            while nums[right] - nums[left] > d:
                left += 1
            cnt += right - left
        return cnt

    lo, hi = 0, nums[-1] - nums[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


# Alternative: brute force, collect all distances and sort (O(n^2 log n)).
def smallestDistancePairBrute(nums: List[int], k: int) -> int:
    d = sorted(abs(nums[i] - nums[j])
               for i in range(len(nums)) for j in range(i + 1, len(nums)))
    return d[k - 1]


if __name__ == "__main__":
    import random
    for f in (smallestDistancePair, smallestDistancePairBrute):
        assert f([1, 3, 1], 1) == 0
        assert f([1, 1, 1], 2) == 0
        assert f([1, 6, 1], 3) == 5
        assert f([0, 10], 1) == 10
        assert f([62, 100, 4], 2) == 58
    random.seed(1)
    for _ in range(300):
        n = random.randint(2, 12)
        a = [random.randint(0, 30) for _ in range(n)]
        k = random.randint(1, n * (n - 1) // 2)
        assert smallestDistancePair(a, k) == smallestDistancePairBrute(a, k)
    print("All tests passed.")
