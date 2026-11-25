"""
2300. Successful Pairs of Spells and Potions
Difficulty: Medium
Topics: Array, Two Pointers, Binary Search, Sorting

Problem:
You are given two positive integer arrays `spells` and `potions`, of length n and m
respectively, where spells[i] represents the strength of the i-th spell and
potions[j] represents the strength of the j-th potion.

You are also given an integer `success`. A spell and potion pair is considered
successful if the product of their strengths is at least `success`.

Return an integer array `pairs` of length n where pairs[i] is the number of
potions that will form a successful pair with the i-th spell.

Example 1:
    Input: spells = [5,1,3], potions = [1,2,3,4,5], success = 7
    Output: [4,0,3]
    Explanation:
      spell 5 -> products [5,10,15,20,25] -> 4 successful
      spell 1 -> products [1,2,3,4,5]     -> 0 successful
      spell 3 -> products [3,6,9,12,15]   -> 3 successful

Example 2:
    Input: spells = [3,1,2], potions = [8,5,8], success = 16
    Output: [2,0,2]

Constraints:
    n == spells.length, m == potions.length
    1 <= n, m <= 10^5
    1 <= spells[i], potions[i] <= 10^5
    1 <= success <= 10^10

Approach (Sort + Binary Search):
    Sort potions once. For a spell s, a potion p is successful iff s * p >= success,
    i.e. p >= ceil(success / s). Because potions is sorted, all successful potions
    form a suffix; binary-search (bisect_left) for the first index whose value is
    >= ceil(success / s). The count is m - idx. Computing the threshold with integer
    ceiling division avoids floating point error: ceil(a/b) == (a + b - 1) // b.

Complexity:
    Time:  O(m log m + n log m)
    Space: O(m) for the sorted copy (O(1) extra if sorting in place)

Alternative (Sort both + Two Pointers):
    Sort spells (keeping original indices) ascending and potions ascending. As the
    spell grows, the minimum successful potion index can only move left, so a single
    pointer sweeping from the right end handles all spells in O(n log n + m log m).
"""

from bisect import bisect_left
from typing import List


class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions = sorted(potions)
        m = len(potions)
        res = []
        for s in spells:
            need = (success + s - 1) // s  # minimum potion strength
            res.append(m - bisect_left(potions, need))
        return res

    def successfulPairsTwoPointers(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions = sorted(potions)
        order = sorted(range(len(spells)), key=lambda i: spells[i])
        res = [0] * len(spells)
        j = len(potions)  # potions[j:] are all successful for current spell
        for i in order:
            s = spells[i]
            while j > 0 and s * potions[j - 1] >= success:
                j -= 1
            res[i] = len(potions) - j
        return res


if __name__ == "__main__":
    sol = Solution()
    cases = [
        (([5, 1, 3], [1, 2, 3, 4, 5], 7), [4, 0, 3]),
        (([3, 1, 2], [8, 5, 8], 16), [2, 0, 2]),
        (([1], [1], 1), [1]),
        (([1], [1], 2), [0]),
        (([100000], [100000], 10**10), [1]),
        (([2, 2, 2], [3, 3, 3], 6), [3, 3, 3]),
        (([10, 1], [1, 1, 1, 10], 10), [4, 1]),
    ]
    for (sp, po, su), exp in cases:
        assert sol.successfulPairs(sp, po, su) == exp, (sp, po, su)
        assert sol.successfulPairsTwoPointers(sp, po, su) == exp, (sp, po, su)

    import random
    for _ in range(300):
        sp = [random.randint(1, 50) for _ in range(random.randint(1, 8))]
        po = [random.randint(1, 50) for _ in range(random.randint(1, 8))]
        su = random.randint(1, 2500)
        brute = [sum(1 for p in po if s * p >= su) for s in sp]
        assert sol.successfulPairs(sp, po, su) == brute
        assert sol.successfulPairsTwoPointers(sp, po, su) == brute
    print("All tests passed!")
