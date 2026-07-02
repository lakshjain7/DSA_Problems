"""
5. Longest Palindromic Substring
Difficulty: Medium
Topics: Dynamic Programming, Two Pointers, String

Problem Statement:
Given a string s, return the longest palindromic substring in s.

Examples:
    Example 1:
        Input: s = "babad"
        Output: "bab" (or "aba", both are valid answers)
    Example 2:
        Input: s = "cbbd"
        Output: "bb"

Constraints:
    1 <= s.length <= 1000
    s consist of only digits and English letters.

Approach (Dynamic Programming):
    Define dp[i][j] = True if the substring s[i:j+1] is a palindrome.
    Base cases: every single character is a palindrome (dp[i][i] = True),
    and two equal adjacent characters form a palindrome (dp[i][i+1] = s[i] == s[i+1]).
    For substrings of length >= 3, s[i:j+1] is a palindrome iff s[i] == s[j] and
    the inner substring s[i+1:j] is also a palindrome (dp[i+1][j-1] is True).
    We fill the table by increasing substring length so that dp[i+1][j-1] is
    already computed when we need it, and we track the start index and length
    of the longest palindrome found.

Complexity Analysis:
    Time:  O(n^2) - we fill an n x n table, O(1) work per cell.
    Space: O(n^2) - the dp table. (The alternative approach below uses O(1).)

Alternative Approach (Expand Around Center):
    A palindrome mirrors around its center, which can either be a single
    character (odd length) or between two characters (even length). There are
    2n - 1 possible centers. For each center, expand outward while the
    characters on both sides match, and track the longest palindrome seen.
    Time: O(n^2), Space: O(1). This is generally preferred in practice due to
    much lower memory usage, though asymptotic time is the same.
"""

from typing import Tuple


def longest_palindrome(s: str) -> str:
    """Return the longest palindromic substring of s using DP."""
    n = len(s)
    if n < 2:
        return s

    # dp[i][j] True if s[i..j] is a palindrome
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1

    for i in range(n):
        dp[i][i] = True

    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            if s[i] != s[j]:
                continue
            if length == 2:
                dp[i][j] = True
            else:
                dp[i][j] = dp[i + 1][j - 1]

            if dp[i][j] and length > max_len:
                start = i
                max_len = length

    return s[start:start + max_len]


def longest_palindrome_expand(s: str) -> str:
    """Alternative: expand around center, O(n^2) time, O(1) space."""
    if len(s) < 2:
        return s

    def expand(left: int, right: int) -> Tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # left+1, right-1 is the last valid palindrome bound
        return left + 1, right - 1

    start, end = 0, 0
    for i in range(len(s)):
        l1, r1 = expand(i, i)       # odd length, center at i
        if r1 - l1 > end - start:
            start, end = l1, r1
        l2, r2 = expand(i, i + 1)   # even length, center between i, i+1
        if r2 - l2 > end - start:
            start, end = l2, r2

    return s[start:end + 1]


def _is_palindrome(x: str) -> bool:
    return x == x[::-1]


if __name__ == "__main__":
    for fn in (longest_palindrome, longest_palindrome_expand):
        # Basic cases - multiple valid answers possible, so check validity + length
        r1 = fn("babad")
        assert r1 in ("bab", "aba"), f"{fn.__name__} failed babad: {r1}"

        r2 = fn("cbbd")
        assert r2 == "bb", f"{fn.__name__} failed cbbd: {r2}"

        # Single character
        assert fn("a") == "a", f"{fn.__name__} failed single char"

        # Two identical characters
        assert fn("aa") == "aa", f"{fn.__name__} failed aa"

        # Two different characters -> any single char valid
        r3 = fn("ac")
        assert r3 in ("a", "c"), f"{fn.__name__} failed ac: {r3}"

        # Entire string is a palindrome
        assert fn("racecar") == "racecar", f"{fn.__name__} failed racecar"

        # Longer string with palindrome in middle
        r4 = fn("forgeeksskeegfor")
        assert _is_palindrome(r4) and len(r4) == 10, f"{fn.__name__} failed skeeg case: {r4}"

        # All same characters
        assert fn("aaaa") == "aaaa", f"{fn.__name__} failed aaaa"

        # No repeated chars at all
        r5 = fn("abcde")
        assert len(r5) == 1 and r5 in "abcde", f"{fn.__name__} failed abcde: {r5}"

        print(f"{fn.__name__}: all tests passed")

    print("All tests passed!")
