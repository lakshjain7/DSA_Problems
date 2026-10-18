"""
493. Reverse Pairs
Difficulty: Hard
Topics: Array, Binary Search, Divide and Conquer, Binary Indexed Tree, Segment Tree, Merge Sort

Problem:
    Given an integer array nums, return the number of reverse pairs in the array.
    A reverse pair is a pair (i, j) where 0 <= i < j < nums.length and
    nums[i] > 2 * nums[j].

Examples:
    Input: nums = [1,3,2,3,1]   Output: 2
    Input: nums = [2,4,3,5,1]   Output: 3

Constraints:
    1 <= nums.length <= 5 * 10^4
    -2^31 <= nums[i] <= 2^31 - 1

Approach:
    Modified merge sort. Split in half, count reverse pairs inside each half
    recursively, then count cross pairs (i in left, j in right) while both halves
    are sorted: for each i, advance a pointer j in the right half while
    nums[i] > 2*nums[j]; because the left half is ascending, j never moves back,
    so the cross count is linear. Then merge the halves (sorted()) and return.

Complexity:
    Time: O(n log n).  Space: O(n).
"""
from typing import List
import bisect


def reversePairs(nums: List[int]) -> int:
    arr = list(nums)

    def sort_count(lo: int, hi: int) -> int:  # [lo, hi)
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        cnt = sort_count(lo, mid) + sort_count(mid, hi)
        j = mid
        for i in range(lo, mid):
            while j < hi and arr[i] > 2 * arr[j]:
                j += 1
            cnt += j - mid
        arr[lo:hi] = sorted(arr[lo:hi])  # Timsort merges two runs in O(n)
        return cnt

    return sort_count(0, len(arr))


def reversePairsBIT(nums: List[int]) -> int:
    """Alternative: Fenwick tree over compressed values. O(n log n) time, O(n) space."""
    vals = sorted(set(nums) | {2 * x for x in nums})
    n = len(vals)
    tree = [0] * (n + 1)

    def add(i):
        i += 1
        while i <= n:
            tree[i] += 1
            i += i & -i

    def query(i):  # count of inserted with rank <= i
        i += 1
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    res = 0
    inserted = 0
    for x in nums:
        # earlier elements y with y > 2x  => inserted - count(y <= 2x)
        res += inserted - query(bisect.bisect_left(vals, 2 * x))
        add(bisect.bisect_left(vals, x))
        inserted += 1
    return res


def _brute(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > 2 * a[j])


if __name__ == "__main__":
    import random
    for f in (reversePairs, reversePairsBIT):
        assert f([1, 3, 2, 3, 1]) == 2
        assert f([2, 4, 3, 5, 1]) == 3
        assert f([5]) == 0
        assert f([1, 2, 3]) == 0
        assert f([-5, -5]) == 1
        assert f([0, 0]) == 0
    big = [2147483647, -2147483648, 2147483647, -2147483648]
    assert reversePairs(big) == _brute(big) == reversePairsBIT(big)
    random.seed(2)
    for _ in range(300):
        a = [random.randint(-20, 20) for _ in range(random.randint(1, 20))]
        e = _brute(a)
        assert reversePairs(a) == e and reversePairsBIT(a) == e
    print("All tests passed.")
