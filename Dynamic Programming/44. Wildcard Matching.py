"""
44. Wildcard Matching
Difficulty: Hard
Topics: String, Dynamic Programming, Greedy, Recursion

Problem Statement
-----------------
Given an input string s and a pattern p, implement wildcard pattern matching
with support for '?' and '*' where:

    '?' Matches any single character.
    '*' Matches any sequence of characters (including the empty sequence).

The matching should cover the entire input string (not partial).

Examples
--------
Example 1:
    Input: s = "aa", p = "a"
    Output: false
    Explanation: "a" does not match the entire string "aa".

Example 2:
    Input: s = "aa", p = "*"
    Output: true
    Explanation: '*' matches any sequence.

Example 3:
    Input: s = "cb", p = "?a"
    Output: false
    Explanation: '?' matches 'c', but the second letter is 'a', which does not
    match 'b'.

Constraints
-----------
    * 0 <= s.length, p.length <= 2000
    * s contains only lowercase English letters.
    * p contains only lowercase English letters, '?' or '*'.

Approach 1: Dynamic Programming (clear and general)
---------------------------------------------------
Let dp[i][j] be True iff the first i characters of s match the first j
characters of p. We want dp[len(s)][len(p)].

Base cases:
    * dp[0][0] = True: empty string matches empty pattern.
    * dp[0][j]: an empty string matches p[:j] only if every pattern character so
      far is '*', since only '*' can match the empty sequence.

Transitions, comparing s[i-1] with p[j-1]:
    * If p[j-1] is a letter or '?': the current characters must line up, so
      dp[i][j] = dp[i-1][j-1] and (p[j-1] == '?' or p[j-1] == s[i-1]).
    * If p[j-1] == '*': it can match the empty sequence (dp[i][j-1]) or absorb
      one more character of s (dp[i-1][j]), so dp[i][j] = dp[i][j-1] or dp[i-1][j].

Why it works: every prefix pairing reduces to a strictly smaller subproblem, and
the '*' branch encodes its two fundamental choices (match nothing, or consume a
character and stay available). Covering the whole grid answers the full match.

Complexity
----------
Time:  O(m * n) where m = len(s), n = len(p).
Space: O(m * n); easily reduced to O(n) with two rolling rows.

Approach 2: Greedy Two-Pointer (optimal space)
----------------------------------------------
Walk s with pointer i and p with pointer j. On a direct match ('?' or equal
letters) advance both. On '*' remember its position (star) and the current i
(match), then tentatively let '*' match empty by advancing only j. On a
mismatch, if a previous '*' exists, backtrack: let that '*' absorb one more
character (match += 1, i = match) and reset j past the star. If no '*' is
available, the strings cannot match. Finally, any trailing '*' in p may be
skipped. This runs in O(m * n) worst case but O(1) extra space and is typically
much faster in practice.
"""


def is_match(s: str, p: str) -> bool:
    """Bottom-up DP. O(m * n) time, O(m * n) space."""
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Empty string vs pattern prefixes: only leading '*'s can match "".
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]


def is_match_greedy(s: str, p: str) -> bool:
    """Greedy two-pointer with backtracking on '*'. O(1) extra space."""
    i = j = 0
    star = -1          # index in p of the most recent '*'
    match = 0          # index in s to resume from when backtracking
    m, n = len(s), len(p)

    while i < m:
        if j < n and (p[j] == '?' or p[j] == s[i]):
            i += 1
            j += 1
        elif j < n and p[j] == '*':
            star = j
            match = i
            j += 1          # first try '*' matching the empty sequence
        elif star != -1:
            j = star + 1     # let the remembered '*' absorb one more char
            match += 1
            i = match
        else:
            return False

    while j < n and p[j] == '*':
        j += 1

    return j == n


if __name__ == "__main__":
    # Provided examples
    assert is_match("aa", "a") is False
    assert is_match("aa", "*") is True
    assert is_match("cb", "?a") is False

    # Empty-string / empty-pattern edge cases
    assert is_match("", "") is True
    assert is_match("", "*") is True
    assert is_match("", "***") is True
    assert is_match("", "?") is False
    assert is_match("a", "") is False

    # Mixed wildcards
    assert is_match("adceb", "*a*b") is True
    assert is_match("acdcb", "a*c?b") is False
    assert is_match("abcabczzzde", "*abc???de*") is True
    assert is_match("abefcdgiescdfimde", "ab*cd?i*de") is True

    # Only '?' wildcards - length must match exactly
    assert is_match("abc", "???") is True
    assert is_match("abc", "??") is False

    # Cross-check DP and greedy implementations agree
    trials = [
        ("aa", "a"),
        ("aa", "*"),
        ("cb", "?a"),
        ("", ""),
        ("", "*"),
        ("a", ""),
        ("adceb", "*a*b"),
        ("acdcb", "a*c?b"),
        ("abcabczzzde", "*abc???de*"),
        ("mississippi", "m??*ss*?i*pi"),
        ("xaylmz", "x?y*z"),
        ("aaaa", "***a"),
    ]
    for s_, p_ in trials:
        assert is_match(s_, p_) == is_match_greedy(s_, p_)

    print("All test cases passed for 44. Wildcard Matching")
