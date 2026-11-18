"""
1095. Find in Mountain Array
Difficulty: Hard
Topics: Array, Binary Search, Interactive

Problem:
(This problem is an interactive problem.)

You may recall that an array arr is a mountain array if and only if:
    arr.length >= 3
    There exists some i with 0 < i < arr.length - 1 such that:
        arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
        arr[i] > arr[i + 1] > ... > arr[arr.length - 1]

Given a mountain array mountainArr, return the minimum index such that
mountainArr.get(index) == target. If such an index does not exist, return -1.

You cannot access the mountain array directly. You may only access the array
using a MountainArray interface:
    MountainArray.get(k) returns the element of the array at index k (0-indexed).
    MountainArray.length() returns the length of the array.

Submissions making more than 100 calls to MountainArray.get will be judged
Wrong Answer.

Example 1:
    Input: array = [1,2,3,4,5,3,1], target = 3
    Output: 2
    Explanation: 3 exists in the array, at index=2 and index=5. Return the
    minimum index, which is 2.

Example 2:
    Input: array = [0,1,2,4,2,1], target = 3
    Output: -1
    Explanation: 3 does not exist in the array, so we return -1.

Constraints:
    3 <= mountainArr.length() <= 10^4
    0 <= target <= 10^9
    0 <= mountainArr.get(index) <= 10^9

Approach (Three binary searches):
    1. Find the peak: binary search on the slope. If arr[m] < arr[m+1] we are
       on the ascending side, so the peak is right of m (lo = m+1); otherwise
       the peak is at m or left of it (hi = m).
    2. Binary search the strictly increasing half [0, peak] for target. If
       found, it is automatically the minimum index (left half comes first).
    3. Otherwise binary search the strictly decreasing half [peak+1, n-1]
       with the comparison reversed.

    Each search costs about log2(10^4) ~= 14 calls; peak search does 2 gets per
    step (~28), total worst case ~= 28 + 14 + 14 = 56 < 100. Caching gets makes
    it even cheaper.

Complexity:
    Time:  O(log n) calls to get.
    Space: O(1) (plus an optional O(log n) cache).
"""
from typing import Callable, List


class MountainArray:
    """Local stand-in for LeetCode's interactive interface; counts get() calls."""

    def __init__(self, arr: List[int]):
        self._arr = arr
        self.calls = 0

    def get(self, index: int) -> int:
        self.calls += 1
        return self._arr[index]

    def length(self) -> int:
        return len(self._arr)


def find_in_mountain_array(target: int, mountain_arr: MountainArray) -> int:
    n = mountain_arr.length()
    cache: dict = {}

    def get(i: int) -> int:
        if i not in cache:
            cache[i] = mountain_arr.get(i)
        return cache[i]

    # 1) peak index
    lo, hi = 0, n - 1
    while lo < hi:
        m = (lo + hi) // 2
        if get(m) < get(m + 1):
            lo = m + 1
        else:
            hi = m
    peak = lo

    # 2) ascending half
    def search(lo: int, hi: int, key: Callable[[int], int]) -> int:
        t = key(target)
        while lo <= hi:
            m = (lo + hi) // 2
            v = key(get(m))
            if v == t:
                return m
            if v < t:
                lo = m + 1
            else:
                hi = m - 1
        return -1

    idx = search(0, peak, lambda x: x)
    if idx != -1:
        return idx
    # 3) descending half: negate values so it looks ascending
    return search(peak + 1, n - 1, lambda x: -x)


def find_in_mountain_array_ternary(target: int, mountain_arr: MountainArray) -> int:
    """
    Alternative: locate the peak with ternary search instead of slope binary
    search, then the same two binary searches. Same O(log n) bound but with a
    worse constant (log base 1.5 vs 2) — shown for comparison; it still stays
    well under 100 calls for n = 10^4 (no caching here, so call counts
    are honest).
    """
    n = mountain_arr.length()
    lo, hi = 0, n - 1
    while hi - lo > 2:
        m1 = lo + (hi - lo) // 3
        m2 = hi - (hi - lo) // 3
        if mountain_arr.get(m1) < mountain_arr.get(m2):
            lo = m1 + 1
        else:
            hi = m2 - 1  # peak is strictly left of m2
    peak = max(range(lo, hi + 1), key=mountain_arr.get)

    lo, hi = 0, peak
    while lo <= hi:
        m = (lo + hi) // 2
        v = mountain_arr.get(m)
        if v == target:
            return m
        if v < target:
            lo = m + 1
        else:
            hi = m - 1
    lo, hi = peak + 1, n - 1
    while lo <= hi:
        m = (lo + hi) // 2
        v = mountain_arr.get(m)
        if v == target:
            return m
        if v > target:
            lo = m + 1
        else:
            hi = m - 1
    return -1


if __name__ == "__main__":
    for fn in (find_in_mountain_array, find_in_mountain_array_ternary):
        assert fn(3, MountainArray([1, 2, 3, 4, 5, 3, 1])) == 2
        assert fn(3, MountainArray([0, 1, 2, 4, 2, 1])) == -1
        assert fn(2, MountainArray([1, 5, 2])) == 2          # only on descending side
        assert fn(5, MountainArray([1, 5, 2])) == 1          # the peak itself
        assert fn(1, MountainArray([1, 5, 2])) == 0
        assert fn(0, MountainArray([1, 5, 2])) == -1
        assert fn(1, MountainArray([0, 5, 3, 2, 1])) == 4

    # randomized cross-check + call budget
    import random
    random.seed(1095)
    for _ in range(3000):
        n = random.randint(3, 60)
        peak = random.randint(1, n - 2)
        left = sorted(random.sample(range(0, 200), peak))
        top = random.randint(max(left) + 60, 400)
        right = sorted(random.sample(range(0, top), n - peak - 1), reverse=True)
        arr = left + [top] + right
        target = random.choice(arr + [random.randint(0, 400)])
        expected = arr.index(target) if target in arr else -1
        for fn in (find_in_mountain_array, find_in_mountain_array_ternary):
            ma = MountainArray(arr)
            assert fn(target, ma) == expected, (arr, target, fn.__name__)

    # worst-case size: verify the 100-call limit
    n = 10000
    arr = list(range(0, 2 * 5000, 2)) + list(range(9999, 0, -2))[: n - 5000]
    for target in (arr[0], arr[4999], arr[-1], 7, 10**9):
        for fn in (find_in_mountain_array, find_in_mountain_array_ternary):
            ma = MountainArray(arr)
            expected = arr.index(target) if target in arr else -1
            assert fn(target, ma) == expected
            assert ma.calls <= 100, (fn.__name__, ma.calls)
    print("All tests passed for 1095. Find in Mountain Array")
