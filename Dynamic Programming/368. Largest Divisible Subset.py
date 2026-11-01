"""
368. Largest Divisible Subset
Difficulty: Medium
Topics: Array, Math, Dynamic Programming, Sorting

Problem:
Given a set of distinct positive integers nums, return the largest subset
answer such that every pair (answer[i], answer[j]) of elements satisfies:
    answer[i] % answer[j] == 0, or
    answer[j] % answer[i] == 0
If there are multiple solutions, return any of them.

Example 1:
    Input: nums = [1,2,3]
    Output: [1,2]   ([1,3] is also accepted)
Example 2:
    Input: nums = [1,2,4,8]
    Output: [1,2,4,8]

Constraints:
    1 <= nums.length <= 1000
    1 <= nums[i] <= 2 * 10^9
    All the integers in nums are unique.

Approach (DP, LIS-style):
Sort ascending. Divisibility is transitive: if a | b and b | c then a | c.
So a subset is valid iff consecutive elements (in sorted order) divide each
other. Let dp[i] = size of the largest valid chain ending at nums[i]; then
dp[i] = 1 + max(dp[j]) over j < i with nums[i] % nums[j] == 0. Keep a parent
pointer to reconstruct the chain.

Complexity:
    Time:  O(n^2) (plus O(n log n) sort)
    Space: O(n)
"""
from typing import List


class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        nums = sorted(nums)
        n = len(nums)
        dp = [1] * n
        parent = [-1] * n
        best = 0
        for i in range(n):
            for j in range(i):
                if nums[i] % nums[j] == 0 and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j
            if dp[i] > dp[best]:
                best = i
        res = []
        while best != -1:
            res.append(nums[best])
            best = parent[best]
        return res[::-1]

    # Alternative: top-down memoization over index of the last chosen element.
    def largestDivisibleSubsetMemo(self, nums: List[int]) -> List[int]:
        from functools import lru_cache
        nums = sorted(nums)
        n = len(nums)

        @lru_cache(maxsize=None)
        def longest(i: int) -> tuple:
            # best chain starting at i going upward
            best = (nums[i],)
            for j in range(i + 1, n):
                if nums[j] % nums[i] == 0:
                    cand = (nums[i],) + longest(j)
                    if len(cand) > len(best):
                        best = cand
            return best

        res: tuple = ()
        for i in range(n):
            c = longest(i)
            if len(c) > len(res):
                res = c
        return list(res)


if __name__ == "__main__":
    from itertools import combinations

    def valid(s):
        return all(a % b == 0 or b % a == 0 for a, b in combinations(s, 2))

    def brute(nums):
        for k in range(len(nums), 0, -1):
            for c in combinations(nums, k):
                if valid(c):
                    return k
        return 0

    sol = Solution()
    for f in (sol.largestDivisibleSubset, sol.largestDivisibleSubsetMemo):
        assert sorted(f([1, 2, 3])) in ([1, 2], [1, 3])
        assert f([1, 2, 4, 8]) == [1, 2, 4, 8]
        assert f([7]) == [7]
        assert len(f([2, 3, 5, 7])) == 1
        assert f([8, 4, 2, 1]) == [1, 2, 4, 8]
        for nums in ([4, 8, 10, 240], [3, 4, 16, 8], [5, 9, 18, 54, 108, 540, 90, 180, 360, 720],
                     [1, 2, 3, 6, 12, 24, 5, 10]):
            r = f(nums)
            assert valid(r) and set(r) <= set(nums) and len(r) == brute(nums), (nums, r)
    print("All tests passed")
