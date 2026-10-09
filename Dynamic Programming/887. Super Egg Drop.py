"""
887. Super Egg Drop
Difficulty: Hard
Topics: Math, Binary Search, Dynamic Programming

Problem:
You are given k identical eggs and a building with n floors labeled 1..n.
There is a floor f (0 <= f <= n) such that any egg dropped from a floor higher
than f breaks, and any egg dropped from floor f or below does not break.
Each move, you may take an unbroken egg and drop it from any floor x. If the
egg breaks it cannot be reused; otherwise it can be reused.
Return the minimum number of moves needed to determine with certainty the
value of f.

Example 1:
    Input: k = 1, n = 2
    Output: 2

Example 2:
    Input: k = 2, n = 6
    Output: 3

Example 3:
    Input: k = 3, n = 14
    Output: 4

Constraints:
    1 <= k <= 100
    1 <= n <= 10^4

Approach (Invert the DP: moves -> floors):
    Let f(m, e) be the maximum number of floors we can fully resolve with m
    moves and e eggs. Dropping an egg from some floor: if it breaks we have
    (m-1, e-1) left to resolve the floors below; if it survives, (m-1, e) to
    resolve the floors above. So
        f(m, e) = f(m-1, e-1) + f(m-1, e) + 1.
    The answer is the smallest m with f(m, k) >= n. Moves needed is at most n,
    and with many eggs it grows like log n, so the loop is short.

Complexity:
    Time:  O(k * m) where m is the answer (m <= n, usually ~ log n .. sqrt n)
    Space: O(k) with a rolling 1-D array

Alternative (Classic DP + binary search on the drop floor):
    dp[e][f] = 1 + min over x of max(dp[e-1][x-1], dp[e][f-x]); the first term
    increases and the second decreases in x, so binary search the crossover.
    Time O(k * n * log n), space O(k * n).
"""
from functools import lru_cache


def super_egg_drop(k: int, n: int) -> int:
    dp = [0] * (k + 1)  # dp[e] = floors resolvable with e eggs and current moves
    moves = 0
    while dp[k] < n:
        moves += 1
        for e in range(k, 0, -1):
            dp[e] = dp[e] + dp[e - 1] + 1
    return moves


def super_egg_drop_bs(k: int, n: int) -> int:
    @lru_cache(maxsize=None)
    def go(e: int, f: int) -> int:
        if f == 0:
            return 0
        if e == 1:
            return f
        lo, hi = 1, f
        while lo < hi:
            mid = (lo + hi) // 2
            if go(e - 1, mid - 1) < go(e, f - mid):
                lo = mid + 1
            else:
                hi = mid
        return 1 + max(go(e - 1, lo - 1), go(e, f - lo))

    return go(k, n)


def _brute(k: int, n: int) -> int:
    @lru_cache(maxsize=None)
    def go(e: int, f: int) -> int:
        if f == 0:
            return 0
        if e == 1:
            return f
        return 1 + min(max(go(e - 1, x - 1), go(e, f - x)) for x in range(1, f + 1))

    return go(k, n)


if __name__ == "__main__":
    for fn in (super_egg_drop, super_egg_drop_bs):
        assert fn(1, 2) == 2
        assert fn(2, 6) == 3
        assert fn(3, 14) == 4
        assert fn(1, 1) == 1
        assert fn(5, 1) == 1
        assert fn(1, 100) == 100
        assert fn(2, 100) == 14
        assert fn(100, 10000) == 14  # ceil(log2(10001))
    assert super_egg_drop(2, 10000) == 141

    for k in range(1, 6):
        for n in range(1, 41):
            exp = _brute(k, n)
            assert super_egg_drop(k, n) == exp, (k, n)
            assert super_egg_drop_bs(k, n) == exp, (k, n)
    print("All tests passed.")
