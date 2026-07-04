'''
410. Split Array Largest Sum
Difficulty: Hard
Topics: Binary Search, Dynamic Programming, Greedy, Array

Problem Statement:
Given an integer array nums and an integer k, split nums into k
non-empty contiguous subarrays such that the largest sum of any subarray
is minimized.

Return the minimized largest sum of the split.

A subarray is a contiguous part of the array.

Examples:
Input: nums = [7,2,5,10,8], k = 2
Output: 18
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [7,2,5] and [10,8], where the largest
sum among the two subarrays is only 18.

Input: nums = [1,2,3,4,5], k = 2
Output: 9
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5], where the largest
sum among the two subarrays is only 9.

Constraints:
- 1 <= nums.length <= 1000
- 0 <= nums[i] <= 10^6
- 1 <= k <= min(50, nums.length)

Approach: Binary search on the answer.
The final answer (the minimized largest subarray sum) lies somewhere in
the range [max(nums), sum(nums)]:
- max(nums) is a lower bound: any single element must fit inside some
  subarray, so the largest sum can never be smaller than the largest
  single element.
- sum(nums) is an upper bound: putting everything into one subarray
  (k = 1) trivially achieves this.

Binary search this range for the smallest "capacity" C such that nums
can be split into at most k subarrays where every subarray's sum is
<= C. This feasibility check is monotonic: if a capacity C works, any
capacity greater than C also works (you can only merge subarrays
together, never need more of them), which is what makes binary search
valid here.

Feasibility check (greedy): scan the array, greedily accumulate elements
into the current subarray as long as adding the next element does not
exceed C. When it would exceed C, close the current subarray, start a
new one, and increment the subarray count. If the number of subarrays
needed stays <= k, capacity C is feasible.

Binary search shrinks the search range: if C is feasible, try a smaller
capacity (move the upper bound down); if not feasible, increase the
lower bound. This converges to the minimum feasible capacity.

Why it works:
Minimizing a maximum subject to a monotonic feasibility predicate is the
classic "binary search on the answer" pattern. The greedy feasibility
check is optimal for a fixed capacity: packing as much as possible into
each subarray before starting a new one never uses more subarrays than
necessary for that capacity (any other valid split with capacity C uses
at least as many subarrays as the greedy pack).

Complexity:
- Time: O(n log(sum(nums) - max(nums))), where each binary search step
  does an O(n) feasibility scan and there are O(log(range)) steps.
- Space: O(1) extra space (O(k) or O(n) if using the DP alternative).

Alternative approach:
Dynamic programming: let dp[i][j] be the minimum possible largest sum
when splitting the first i elements into j subarrays. Using prefix sums
to get range sums in O(1):
    dp[i][j] = min over m < i of max(dp[m][j-1], prefixSum(m, i))
This is correct but runs in O(n^2 * k) time (with prefix sums), which is
significantly slower than binary search for large inputs but is a useful
way to double-check correctness on small cases.
'''

from typing import List


def splitArray(nums: List[int], k: int) -> int:
    def feasible(capacity: int) -> bool:
        subarrays_needed = 1
        current_sum = 0
        for num in nums:
            if current_sum + num > capacity:
                subarrays_needed += 1
                current_sum = num
                if subarrays_needed > k:
                    return False
            else:
                current_sum += num
        return True

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def splitArray_dp(nums: List[int], k: int) -> int:
    """Alternative: O(n^2 * k) DP using prefix sums."""
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, num in enumerate(nums):
        prefix[i + 1] = prefix[i] + num

    INF = float("inf")
    # dp[j][i] = min largest sum splitting first i elements into j parts
    dp = [[INF] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0

    for j in range(1, k + 1):
        for i in range(1, n + 1):
            for m in range(j - 1, i):
                candidate = max(dp[j - 1][m], prefix[i] - prefix[m])
                if candidate < dp[j][i]:
                    dp[j][i] = candidate

    return dp[k][n]


if __name__ == "__main__":
    for fn in (splitArray, splitArray_dp):
        assert fn([7, 2, 5, 10, 8], 2) == 18
        assert fn([1, 2, 3, 4, 5], 2) == 9
        # k equals array length: each element is its own subarray.
        assert fn([1, 4, 4], 3) == 4
        # k = 1: entire array is one subarray.
        assert fn([1, 2, 3, 4, 5], 1) == 15
        # Single element array.
        assert fn([5], 1) == 5
        # All identical elements.
        assert fn([2, 2, 2, 2], 2) == 4
        # Zeros present in the array.
        assert fn([0, 0, 0, 10], 2) == 10

    print("All Split Array Largest Sum tests passed.")
