"""
421. Maximum XOR of Two Numbers in an Array
Difficulty: Medium
Topics: Array, Hash Table, Bit Manipulation, Trie

Problem:
Given an integer array nums, return the maximum result of nums[i] XOR nums[j],
where 0 <= i <= j < n.

Example 1:
    Input: nums = [3,10,5,25,2,8]
    Output: 28   (5 XOR 25 = 28)
Example 2:
    Input: nums = [14,70,53,83,49,91,36,80,92,51,66,70]
    Output: 127

Constraints:
    1 <= nums.length <= 2 * 10^5
    0 <= nums[i] <= 2^31 - 1

Approach (binary trie, greedy):
Insert every number into a trie of its 31 bits (MSB first). For each number,
walk the trie preferring the child with the OPPOSITE bit at every level: a
differing high bit contributes more than any combination of lower bits, so
greedy choice is optimal. Track the max XOR.

Complexity:
    Time:  O(31 * n)
    Space: O(31 * n)
"""
from typing import List


class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        BITS = 31
        trie = [[0, 0]]  # node -> [child0, child1]
        for x in nums:
            node = 0
            for b in range(BITS - 1, -1, -1):
                bit = (x >> b) & 1
                if not trie[node][bit]:
                    trie.append([0, 0])
                    trie[node][bit] = len(trie) - 1
                node = trie[node][bit]
        best = 0
        for x in nums:
            node, cur = 0, 0
            for b in range(BITS - 1, -1, -1):
                bit = (x >> b) & 1
                want = bit ^ 1
                if trie[node][want]:
                    cur |= 1 << b
                    node = trie[node][want]
                else:
                    node = trie[node][bit]
            best = max(best, cur)
        return best

    # Alternative: build the answer bit by bit using prefix sets.
    # If prefixes p1, p2 exist with p1 ^ p2 == candidate, candidate is reachable.
    def findMaximumXORPrefixSet(self, nums: List[int]) -> int:
        ans = 0
        for b in range(30, -1, -1):
            ans <<= 1
            prefixes = {x >> b for x in nums}
            cand = ans | 1
            if any((cand ^ p) in prefixes for p in prefixes):
                ans = cand
        return ans


if __name__ == "__main__":
    import random

    sol = Solution()
    for f in (sol.findMaximumXOR, sol.findMaximumXORPrefixSet):
        assert f([3, 10, 5, 25, 2, 8]) == 28
        assert f([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]) == 127
        assert f([0]) == 0
        assert f([8, 8]) == 0
        assert f([2**31 - 1, 0]) == 2**31 - 1
        random.seed(1)
        for _ in range(200):
            arr = [random.randint(0, 2**31 - 1 if random.random() < .5 else 50)
                   for _ in range(random.randint(1, 12))]
            exp = max(a ^ b for a in arr for b in arr)
            assert f(arr) == exp, (arr, f(arr), exp)
    print("All tests passed")
