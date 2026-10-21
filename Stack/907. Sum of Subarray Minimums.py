"""
907. Sum of Subarray Minimums
Difficulty: Medium
Topics: Array, Dynamic Programming, Stack, Monotonic Stack

Problem:
Given an array of integers arr, find the sum of min(b), where b ranges over
every (contiguous) subarray of arr. Since the answer may be large, return it
modulo 10^9 + 7.

Examples:
  Input: arr = [3,1,2,4]  -> 17
    Subarrays: [3],[1],[2],[4],[3,1],[1,2],[2,4],[3,1,2],[1,2,4],[3,1,2,4]
    Minimums: 3,1,2,4,1,1,2,1,1,1 -> 17
  Input: arr = [11,81,94,43,3] -> 444

Constraints:
  1 <= arr.length <= 3 * 10^4
  1 <= arr[i] <= 3 * 10^4

Approach (monotonic stack, contribution technique):
  Count, for each element arr[i], in how many subarrays it is the minimum.
  Let L = distance to the previous element that is strictly smaller and
  R = distance to the next element that is smaller or equal (the asymmetry
  breaks ties so each subarray is counted once). Then arr[i] is the minimum of
  L * R subarrays and contributes arr[i] * L * R. A monotonic increasing stack
  finds both boundaries in one pass: when index j pops index i, j is the next
  smaller-or-equal element of i and the new stack top is the previous
  strictly-smaller element.

Complexity:
  Time:  O(n)  (each index pushed and popped once)
  Space: O(n)
"""
from typing import List

MOD = 10**9 + 7


def sum_subarray_mins(arr: List[int]) -> int:
    stack: List[int] = []  # indices with strictly increasing values
    total = 0
    n = len(arr)
    for j in range(n + 1):
        cur = arr[j] if j < n else 0  # sentinel flushes the stack
        while stack and arr[stack[-1]] >= cur:
            i = stack.pop()
            left = i - (stack[-1] if stack else -1)
            right = j - i
            total += arr[i] * left * right
        stack.append(j)
    return total % MOD


def sum_subarray_mins_dp(arr: List[int]) -> int:
    """Alternative: dp[i] = sum of minimums of subarrays ending at i, with the
    stack used to jump back to the previous smaller element."""
    stack: List[int] = []
    dp = [0] * len(arr)
    total = 0
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] >= x:
            stack.pop()
        if stack:
            p = stack[-1]
            dp[i] = dp[p] + x * (i - p)
        else:
            dp[i] = x * (i + 1)
        stack.append(i)
        total += dp[i]
    return total % MOD


if __name__ == "__main__":
    import random

    def brute(a):
        s = 0
        for i in range(len(a)):
            m = a[i]
            for j in range(i, len(a)):
                m = min(m, a[j])
                s += m
        return s % MOD

    assert sum_subarray_mins([3, 1, 2, 4]) == 17
    assert sum_subarray_mins([11, 81, 94, 43, 3]) == 444
    assert sum_subarray_mins([1]) == 1
    assert sum_subarray_mins([2, 2, 2]) == 12      # duplicates
    assert sum_subarray_mins([1, 2, 3, 4]) == brute([1, 2, 3, 4])
    assert sum_subarray_mins([4, 3, 2, 1]) == brute([4, 3, 2, 1])
    big = [30000] * 30000
    assert sum_subarray_mins(big) == sum_subarray_mins_dp(big)
    random.seed(2)
    for _ in range(1000):
        a = [random.randint(1, 6) for _ in range(random.randint(1, 10))]
        assert sum_subarray_mins(a) == brute(a) == sum_subarray_mins_dp(a), a
    print("All tests passed.")
