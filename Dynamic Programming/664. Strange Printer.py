"""
664. Strange Printer
Difficulty: Hard
Topics: String, Dynamic Programming

Problem:
There is a strange printer with two properties:
  - It can only print a sequence of the same character each time.
  - At each turn, it can print new characters starting from and ending at any
    place, covering the original existing characters.
Given a string s, return the minimum number of turns the printer needed to
print it.

Example 1:
    Input: s = "aaabbb"   Output: 2
Example 2:
    Input: s = "aba"      Output: 2
    (Print "aaa" first, then print "b" over the middle.)

Constraints:
    1 <= s.length <= 100
    s consists of lowercase English letters.

Approach (interval DP):
    First compress consecutive duplicates. dp[i][j] = min turns to print
    s[i..j]. Base: dp[i][i] = 1. Otherwise print s[i] on its own and then
    the rest: dp[i][j] = 1 + dp[i+1][j]. Or, if s[k] == s[i] for some
    i < k <= j, the first stroke of s[i] can be extended to cover s[k] for
    free: dp[i][j] = min(dp[i+1][k-1] + dp[k][j]) (the stretch between is
    printed over the extended stroke, and dp[k][j] absorbs s[k]).

Complexity: Time O(n^3), Space O(n^2).
"""
from functools import lru_cache
from itertools import groupby


def strange_printer(s: str) -> int:
    s = "".join(c for c, _ in groupby(s))
    n = len(s)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            best = 1 + dp[i + 1][j]
            for k in range(i + 1, j + 1):
                if s[k] == s[i]:
                    mid = dp[i + 1][k - 1] if k - 1 >= i + 1 else 0
                    best = min(best, mid + dp[k][j])
            dp[i][j] = best
    return dp[0][n - 1]


# Alternative: top-down memoization.
def strange_printer_memo(s: str) -> int:
    s = "".join(c for c, _ in groupby(s))

    @lru_cache(maxsize=None)
    def f(i: int, j: int) -> int:
        if i > j:
            return 0
        res = 1 + f(i + 1, j)
        for k in range(i + 1, j + 1):
            if s[k] == s[i]:
                res = min(res, f(i + 1, k - 1) + f(k, j))
        return res

    return f(0, len(s) - 1)


if __name__ == "__main__":
    for fn in (strange_printer, strange_printer_memo):
        assert fn("aaabbb") == 2
        assert fn("aba") == 2
        assert fn("a") == 1
        assert fn("abc") == 3
        assert fn("abab") == 3
        assert fn("tbgtgb") == 4
        assert fn("aaaaaaaa") == 1
        assert fn("abcabc") == 5
    print("All tests passed")
