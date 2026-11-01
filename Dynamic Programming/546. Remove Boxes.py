"""
546. Remove Boxes
Difficulty: Hard
Topics: Array, Dynamic Programming, Memoization

Problem:
You are given several boxes with different colors represented by different
positive numbers. You may experience several rounds to remove boxes until there
is no box left. In each round you can choose some continuous boxes with the same
color (i.e., composed of k boxes, k >= 1), remove them and get k * k points.
Return the maximum points you can get.

Example 1:
    Input: boxes = [1,3,2,2,2,3,4,3,1]
    Output: 23
Example 2:
    Input: boxes = [1,1,1]
    Output: 9
Example 3:
    Input: boxes = [1]
    Output: 1

Constraints:
    1 <= boxes.length <= 100
    1 <= boxes[i] <= 100

Approach (interval DP with extra state):
Let dp(l, r, k) = best score for boxes[l..r] when k extra boxes of color
boxes[l] are attached immediately to the left of l (already merged in).
Options:
  1. Remove boxes[l] together with its k attached ones now: (k+1)^2 + dp(l+1, r, 0).
  2. For some m in (l, r] with boxes[m] == boxes[l], first clear l+1..m-1 fully
     (dp(l+1, m-1, 0)) so boxes[l] merges with boxes[m]: + dp(m, r, k+1).
Optimisation: first extend l over equal neighbours (k += 1) since removing a
run together is never worse.

Complexity:
    Time:  O(n^4) worst case (n^3 states, O(n) transitions)
    Space: O(n^3)
"""
from functools import lru_cache
from typing import List


class Solution:
    def removeBoxes(self, boxes: List[int]) -> int:
        n = len(boxes)

        @lru_cache(maxsize=None)
        def dp(l: int, r: int, k: int) -> int:
            if l > r:
                return 0
            while l < r and boxes[l + 1] == boxes[l]:
                l += 1
                k += 1
            res = (k + 1) ** 2 + dp(l + 1, r, 0)
            for m in range(l + 1, r + 1):
                if boxes[m] == boxes[l]:
                    res = max(res, dp(l + 1, m - 1, 0) + dp(m, r, k + 1))
            return res

        ans = dp(0, n - 1, 0)
        dp.cache_clear()
        return ans

    # Alternative: brute-force over all removal orders (exponential; for validation only).
    def removeBoxesBrute(self, boxes: List[int]) -> int:
        @lru_cache(maxsize=None)
        def go(t: tuple) -> int:
            if not t:
                return 0
            best = 0
            i = 0
            while i < len(t):
                for j in range(i, len(t)):
                    if t[j] != t[i]:
                        break
                    best = max(best, (j - i + 1) ** 2 + go(t[:i] + t[j + 1:]))
                i += 1
            return best

        return go(tuple(boxes))


if __name__ == "__main__":
    import random

    sol = Solution()
    assert sol.removeBoxes([1, 3, 2, 2, 2, 3, 4, 3, 1]) == 23
    assert sol.removeBoxes([1, 1, 1]) == 9
    assert sol.removeBoxes([1]) == 1
    assert sol.removeBoxes([1, 2, 3]) == 3
    assert sol.removeBoxes([1, 2, 1]) == 5
    assert sol.removeBoxes([5] * 100) == 10000
    random.seed(7)
    for _ in range(150):
        arr = [random.randint(1, 3) for _ in range(random.randint(1, 9))]
        assert sol.removeBoxes(arr) == sol.removeBoxesBrute(arr), arr
    # performance sanity
    assert sol.removeBoxes([random.randint(1, 5) for _ in range(100)]) > 0
    print("All tests passed")
