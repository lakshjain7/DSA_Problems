"""
327. Count of Range Sum
Difficulty: Hard
Topics: Array, Binary Search, Divide and Conquer, Binary Indexed Tree, Segment Tree,
        Merge Sort, Ordered Set

Problem:
Given an integer array nums and two integers lower and upper, return the number of
range sums that lie in [lower, upper] inclusive. Range sum S(i, j) is the sum of the
elements of nums between indices i and j (i <= j), inclusive.

Examples:
    Input: nums = [-2,5,-1], lower = -2, upper = 2
    Output: 3   (ranges [0,0], [2,2], [0,2] with sums -2, -1, 2)

    Input: nums = [0], lower = 0, upper = 0
    Output: 1

Constraints:
    1 <= nums.length <= 10^5
    -2^31 <= nums[i] <= 2^31 - 1
    -10^5 <= lower <= upper <= 10^5
    The answer is guaranteed to fit in a 32-bit integer.

Approach (merge sort on prefix sums):
    Let prefix[0]=0, prefix[i]=nums[0]+...+nums[i-1]. S(i,j) = prefix[j+1]-prefix[i].
    So we count pairs a<b with lower <= prefix[b]-prefix[a] <= upper.
    Merge sort the prefix array. Before merging sorted halves L and R, for every x in L
    (ascending) the valid y in R form a contiguous window [lo, hi) where
    y - x >= lower and y - x <= upper. Because x ascends, both pointers only move
    forward, so counting is linear per level. Then merge normally.

Complexity:
    Time:  O(n log n)
    Space: O(n)

Alternative: brute force over all pairs of prefix sums, O(n^2) (used to cross-check).
"""
from typing import List
import random


def countRangeSum(nums: List[int], lower: int, upper: int) -> int:
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)

    def sort_count(lo: int, hi: int) -> int:  # sorts prefix[lo:hi]
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        count = sort_count(lo, mid) + sort_count(mid, hi)
        left, right = mid, mid
        for i in range(lo, mid):
            while left < hi and prefix[left] - prefix[i] < lower:
                left += 1
            while right < hi and prefix[right] - prefix[i] <= upper:
                right += 1
            count += right - left
        prefix[lo:hi] = sorted(prefix[lo:mid] + prefix[mid:hi])  # merge of two sorted runs (timsort is linear here)
        return count

    return sort_count(0, len(prefix))


def countRangeSumBrute(nums: List[int], lower: int, upper: int) -> int:
    n, count = len(nums), 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if lower <= s <= upper:
                count += 1
    return count


if __name__ == "__main__":
    assert countRangeSum([-2, 5, -1], -2, 2) == 3
    assert countRangeSum([0], 0, 0) == 1
    assert countRangeSum([1], 2, 3) == 0
    assert countRangeSum([0, 0, 0], 0, 0) == 6
    assert countRangeSum([-2147483647, 0, -2147483647, 2147483647], -564, 3864) == 3
    random.seed(1)
    for _ in range(300):
        a = [random.randint(-10, 10) for _ in range(random.randint(1, 15))]
        lo = random.randint(-15, 5)
        hi = random.randint(lo, 20)
        assert countRangeSum(a, lo, hi) == countRangeSumBrute(a, lo, hi), (a, lo, hi)
    print("All tests passed!")
