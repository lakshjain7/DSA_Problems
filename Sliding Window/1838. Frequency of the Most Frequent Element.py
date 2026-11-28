"""
1838. Frequency of the Most Frequent Element
Difficulty: Medium
Topics: Array, Binary Search, Greedy, Sliding Window, Sorting, Prefix Sum

Problem:
The frequency of an element is the number of times it occurs in an array.

You are given an integer array `nums` and an integer `k`. In one operation,
you can choose an index of `nums` and increment the element at that index by 1.

Return the maximum possible frequency of an element after performing at most
`k` operations.

Example 1:
    Input: nums = [1,2,4], k = 5
    Output: 3
    Explanation: Increment the first element three times and the second element
    two times to make nums = [4,4,4]. 4 has a frequency of 3.

Example 2:
    Input: nums = [1,4,8,13], k = 5
    Output: 2
    Explanation: There are multiple optimal solutions:
    - Increment the first element three times to make nums = [4,4,8,13]. 4 has a frequency of 2.
    - Increment the second element four times to make nums = [1,8,8,13]. 8 has a frequency of 2.
    - Increment the third element five times to make nums = [1,4,13,13]. 13 has a frequency of 2.

Example 3:
    Input: nums = [3,9,6], k = 2
    Output: 1

Constraints:
    1 <= nums.length <= 10^5
    1 <= nums[i] <= 10^5
    1 <= k <= 10^5

Approach (Sort + Variable Sliding Window):
    We can only increment, so the target value must be some existing element,
    and it is cheapest to raise the elements just below it. After sorting, any
    optimal group is therefore a contiguous window nums[l..r] whose target is
    nums[r]. The cost to raise every element of the window to nums[r] is

        cost = nums[r] * (r - l + 1) - sum(nums[l..r])

    As r moves right, cost only grows, so we shrink from the left while
    cost > k. The largest valid window size is the answer. Each index enters
    and leaves the window at most once.

Complexity:
    Time:  O(n log n) for sorting; the window pass is O(n).
    Space: O(1) extra (ignoring the sort's internal space).

Alternative (Prefix Sum + Binary Search):
    For each right end r, binary-search the smallest l such that the cost
    computed from prefix sums is <= k. O(n log n) time, O(n) space.
"""

from typing import List


def max_frequency(nums: List[int], k: int) -> int:
    nums = sorted(nums)
    left = 0
    window_sum = 0
    best = 0
    for right, val in enumerate(nums):
        window_sum += val
        # Shrink while raising the whole window to `val` costs more than k
        while val * (right - left + 1) - window_sum > k:
            window_sum -= nums[left]
            left += 1
        best = max(best, right - left + 1)
    return best


def max_frequency_binary_search(nums: List[int], k: int) -> int:
    nums = sorted(nums)
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, v in enumerate(nums):
        prefix[i + 1] = prefix[i] + v

    best = 1
    for r in range(n):
        lo, hi = 0, r
        while lo < hi:
            mid = (lo + hi) // 2
            cost = nums[r] * (r - mid + 1) - (prefix[r + 1] - prefix[mid])
            if cost <= k:
                hi = mid
            else:
                lo = mid + 1
        best = max(best, r - lo + 1)
    return best


if __name__ == "__main__":
    import random

    for fn in (max_frequency, max_frequency_binary_search):
        assert fn([1, 2, 4], 5) == 3
        assert fn([1, 4, 8, 13], 5) == 2
        assert fn([3, 9, 6], 2) == 1
        assert fn([5], 1) == 1                      # single element
        assert fn([7, 7, 7, 7], 1) == 4             # already all equal
        assert fn([1, 1, 1, 100], 1) == 3           # outlier far away
        assert fn([1, 2, 3, 4, 5], 100) == 5        # k large enough for all
        assert fn([9930, 9923, 9983, 9997, 9934, 9952, 9945, 9914, 9985, 9982, 9970,
                   9932, 9985, 9902, 9975, 9990, 9922, 9990, 9994, 9937, 9996, 9964,
                   9943, 9963, 9911, 9925, 9935, 9945, 9933, 9916, 9930, 9938, 10000,
                   9916, 9911, 9959, 9957, 9907, 9913, 9916, 9993, 9930, 9975, 9924,
                   9988, 9923, 9910, 9925, 9977, 9981, 9927, 9930, 9927, 9925, 9923,
                   9904, 9928, 9928, 9986, 9903, 9985, 9954, 9938, 9911, 9952, 9974,
                   9926, 9920, 9972, 9983, 9973, 9917, 9995, 9973, 9977, 9947, 9936,
                   9975, 9954, 9932, 9964, 9972, 9935, 9946, 9966], 3056) == 73

    # Randomised cross-check against brute force
    def brute(nums, k):
        best = 0
        for target in set(nums):
            costs = sorted(target - x for x in nums if x <= target)
            used = cnt = 0
            for c in costs:
                if used + c <= k:
                    used += c
                    cnt += 1
            best = max(best, cnt)
        return best

    for _ in range(300):
        arr = [random.randint(1, 20) for _ in range(random.randint(1, 12))]
        kk = random.randint(1, 30)
        exp = brute(arr, kk)
        assert max_frequency(arr, kk) == exp
        assert max_frequency_binary_search(arr, kk) == exp

    print("All tests passed for 1838. Frequency of the Most Frequent Element")
