"""
97. Interleaving String
Difficulty: Hard
Topics: String, Dynamic Programming

Problem Statement
-----------------
Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of
s1 and s2.

An interleaving of two strings s and t is a configuration where s and t are
divided into n and m substrings respectively, such that:
    s = s1 + s2 + ... + sn
    t = t1 + t2 + ... + tm
    |n - m| <= 1
and the interleaving is
    s1 + t1 + s2 + t2 + ...   or   t1 + s1 + t2 + s2 + ...

Note: a + b is the concatenation of strings a and b.

Examples
--------
Example 1:
    Input:  s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
    Output: True

Example 2:
    Input:  s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
    Output: False

Example 3:
    Input:  s1 = "", s2 = "", s3 = ""
    Output: True

Constraints
-----------
    0 <= s1.length, s2.length <= 100
    0 <= s3.length <= 200
    s1, s2, and s3 consist of lowercase English letters.

Approach: 2D Dynamic Programming
--------------------------------
First, a necessary length check: if len(s1) + len(s2) != len(s3), it is
impossible.

Let dp[i][j] be True iff the first i characters of s1 and the first j characters
of s2 can interleave to form the first (i + j) characters of s3.

Transition - the character s3[i + j - 1] must come from either s1 or s2:
    dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1])   # last char taken from s1
             or (dp[i][j-1] and s2[j-1] == s3[i+j-1])  # last char taken from s2

Base case: dp[0][0] = True (two empty strings interleave to the empty string).
The first row and column fill in naturally from the transition (using only s2 or
only s1 respectively).

Why it works: interleaving builds s3 one character at a time; at each step the
newly appended character is the next unused character of exactly one source
string. dp captures every reachable (i, j) prefix state, and overlapping
subproblems are solved once.

Complexity
----------
Time:  O(m * n) where m = len(s1), n = len(s2).
Space: O(m * n) for the full table; the rolling 1D version below uses O(n).
"""

from functools import lru_cache
from typing import List


def is_interleave(s1: str, s2: str, s3: str) -> bool:
    """Bottom-up 2D DP. Returns True iff s3 is an interleaving of s1 and s2."""
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False

    dp: List[List[bool]] = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    for i in range(m + 1):
        for j in range(n + 1):
            if i > 0 and s1[i - 1] == s3[i + j - 1]:
                dp[i][j] = dp[i][j] or dp[i - 1][j]
            if j > 0 and s2[j - 1] == s3[i + j - 1]:
                dp[i][j] = dp[i][j] or dp[i][j - 1]

    return dp[m][n]


def is_interleave_rolling(s1: str, s2: str, s3: str) -> bool:
    """Space-optimized DP using a single row. O(n) space."""
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False

    dp = [False] * (n + 1)
    dp[0] = True
    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]

    for i in range(1, m + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
        for j in range(1, n + 1):
            from_s1 = dp[j] and s1[i - 1] == s3[i + j - 1]
            from_s2 = dp[j - 1] and s2[j - 1] == s3[i + j - 1]
            dp[j] = from_s1 or from_s2
    return dp[n]


def is_interleave_memo(s1: str, s2: str, s3: str) -> bool:
    """Top-down memoized recursion, for contrast with the tabulation above."""
    if len(s1) + len(s2) != len(s3):
        return False

    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> bool:
        if i == len(s1) and j == len(s2):
            return True
        k = i + j
        if i < len(s1) and s1[i] == s3[k] and solve(i + 1, j):
            return True
        if j < len(s2) and s2[j] == s3[k] and solve(i, j + 1):
            return True
        return False

    return solve(0, 0)


if __name__ == "__main__":
    tests = [
        ("aabcc", "dbbca", "aadbbcbcac", True),
        ("aabcc", "dbbca", "aadbbbaccc", False),
        ("", "", "", True),
        ("", "abc", "abc", True),
        ("abc", "", "abc", True),
        ("a", "b", "ab", True),
        ("a", "b", "ba", True),
        ("a", "b", "aa", False),          # length matches but content cannot
        ("aa", "ab", "aaba", True),
        ("aa", "ab", "abaa", True),
        ("aabc", "abad", "aabadabc", True),
        ("aabc", "abad", "aabadacb", False),
        ("abc", "def", "abcdefg", False),  # length mismatch
    ]
    for s1, s2, s3, expected in tests:
        got = is_interleave(s1, s2, s3)
        assert got == expected, f"is_interleave({s1!r},{s2!r},{s3!r}) = {got}, expected {expected}"
        assert is_interleave_rolling(s1, s2, s3) == expected, f"rolling failed on {s1!r},{s2!r},{s3!r}"
        assert is_interleave_memo(s1, s2, s3) == expected, f"memo failed on {s1!r},{s2!r},{s3!r}"

    print("All tests passed for 97. Interleaving String")
