"""
528. Random Pick with Weight
Difficulty: Medium
Topics: Array, Math, Binary Search, Prefix Sum, Randomized

Problem:
You are given a 0-indexed array of positive integers w where w[i] describes
the weight of the i-th index. Implement pickIndex(), which randomly picks an
index in the range [0, w.length - 1] (inclusive) and returns it. The
probability of picking index i is w[i] / sum(w).

Example 1:
  Input:  ["Solution","pickIndex"]  [[[1]],[]]
  Output: [null,0]
  Explanation: only one index, so it is always picked.

Example 2:
  Input:  ["Solution","pickIndex","pickIndex",...]  [[[1,3]],[],[],...]
  Output: index 1 is returned ~75% of the time, index 0 ~25%.

Constraints:
  1 <= w.length <= 10^4
  1 <= w[i] <= 10^5
  pickIndex will be called at most 10^4 times.

Approach (prefix sums + binary search):
  Build prefix[i] = w[0] + ... + w[i]. Draw r uniformly from [1, total]. The
  index i owns the r-values in (prefix[i-1], prefix[i]] -- exactly w[i] of
  them -- so the answer is the first i with prefix[i] >= r, found by binary
  search (bisect_left). Each index is therefore chosen with probability
  w[i] / total.

Complexity:
  Init:      O(n) time, O(n) space
  pickIndex: O(log n) time, O(1) extra space

Alternative: linear scan over prefix sums per pick -- O(n) per call.
"""
import random
from bisect import bisect_left
from typing import List


class Solution:
    def __init__(self, w: List[int]):
        self.prefix: List[int] = []
        total = 0
        for x in w:
            total += x
            self.prefix.append(total)
        self.total = total

    def _find(self, r: int) -> int:
        """Index owning the 1-based ticket r in [1, total] (binary search)."""
        lo, hi = 0, len(self.prefix) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if self.prefix[mid] >= r:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def _find_linear(self, r: int) -> int:
        """Alternative: linear scan."""
        for i, p in enumerate(self.prefix):
            if p >= r:
                return i
        return len(self.prefix) - 1

    def pickIndex(self) -> int:
        return self._find(random.randint(1, self.total))


if __name__ == "__main__":
    s = Solution([1])
    assert all(s.pickIndex() == 0 for _ in range(50))

    s = Solution([1, 3])
    assert s.prefix == [1, 4] and s.total == 4
    assert [s._find(r) for r in range(1, 5)] == [0, 1, 1, 1]

    s = Solution([3, 14, 1, 7])
    assert s.prefix == [3, 17, 18, 25]
    owners = [s._find(r) for r in range(1, 26)]
    assert owners == [0] * 3 + [1] * 14 + [2] * 1 + [3] * 7
    assert owners == [s._find_linear(r) for r in range(1, 26)]

    # statistical check
    random.seed(7)
    s = Solution([1, 3])
    n = 40000
    ones = sum(s.pickIndex() for _ in range(n))
    assert abs(ones / n - 0.75) < 0.02, ones / n

    # all picks in range
    s = Solution([5, 5, 5, 100000])
    assert all(0 <= s.pickIndex() < 4 for _ in range(1000))
    print("All tests passed!")
