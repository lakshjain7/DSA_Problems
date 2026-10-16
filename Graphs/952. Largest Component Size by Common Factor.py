"""
Problem 952: Largest Component Size by Common Factor
Difficulty: Hard
Topics: Array, Hash Table, Math, Union Find, Number Theory

You are given an integer array of unique positive integers nums. Consider the
graph where:
- there are nums.length nodes labeled nums[0] .. nums[n-1];
- there is an edge between nums[i] and nums[j] if they share a common factor
  greater than 1.
Return the size of the largest connected component in the graph.

Examples:
    [4,6,15,35] -> 4
    [20,50,9,63] -> 2
    [2,3,6,7,4,12,21,39] -> 8

Constraints:
- 1 <= nums.length <= 2 * 10^4
- 1 <= nums[i] <= 10^5
- All values of nums are unique.

Approach:
    Union-Find over prime factors. For each number, factor it (trial division
    up to sqrt) and union the number's index with each prime factor. Numbers
    sharing a prime end up in one set. Then count how many numbers land in
    each root and return the max.

Complexity:
    Time O(n * sqrt(M) * alpha), M = max(nums). Space O(n + M).

Alternative: sieve smallest-prime-factor table up to max(nums) for O(log M)
    factorization per number (same union-find afterwards).
"""
from collections import Counter
from typing import List


class DSU:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def largestComponentSize(nums: List[int]) -> int:
    m = max(nums)
    dsu = DSU(m + 1)
    for x in nums:
        d = 2
        y = x
        while d * d <= y:
            if y % d == 0:
                dsu.union(x, d)
                while y % d == 0:
                    y //= d
            d += 1
        if y > 1:
            dsu.union(x, y)
    cnt = Counter(dsu.find(x) for x in nums)
    return max(cnt.values())


def largestComponentSize_spf(nums: List[int]) -> int:
    m = max(nums)
    spf = list(range(m + 1))
    i = 2
    while i * i <= m:
        if spf[i] == i:
            for j in range(i * i, m + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    dsu = DSU(m + 1)
    for x in nums:
        y = x
        while y > 1:
            p = spf[y]
            dsu.union(x, p)
            while y % p == 0:
                y //= p
    cnt = Counter(dsu.find(x) for x in nums)
    return max(cnt.values())


if __name__ == "__main__":
    cases = [
        ([4, 6, 15, 35], 4),
        ([20, 50, 9, 63], 2),
        ([2, 3, 6, 7, 4, 12, 21, 39], 8),
        ([1], 1),
        ([1, 2], 1),
        ([2, 3, 5, 7, 11], 1),
        ([99999, 100000], 1),
        ([7], 1),
    ]
    for nums, exp in cases:
        assert largestComponentSize(nums) == exp, (nums, largestComponentSize(nums))
        assert largestComponentSize_spf(nums) == exp, nums
    big = list(range(2, 2002, 2))
    assert largestComponentSize(big) == len(big)
    print("All tests passed.")
