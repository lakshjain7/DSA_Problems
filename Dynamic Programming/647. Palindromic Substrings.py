"""
647. Palindromic Substrings
Difficulty: Medium
Topics: Two Pointers, String, Dynamic Programming

Problem Statement
-----------------
Given a string `s`, return the number of palindromic substrings in it.

A string is a palindrome when it reads the same backward as forward.
A substring is a contiguous sequence of characters within the string.

Examples
--------
Example 1:
    Input:  s = "abc"
    Output: 3
    Explanation: Three palindromic strings: "a", "b", "c".

Example 2:
    Input:  s = "aaa"
    Output: 6
    Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".

Constraints
-----------
    1 <= s.length <= 1000
    s consists of lowercase English letters.

Approach (Expand Around Center)
-------------------------------
Every palindrome has a center. For a string of length n there are 2n - 1
possible centers: n single-character centers (odd-length palindromes) and n - 1
between-character centers (even-length palindromes).

For each center we expand two pointers (left, right) outward while they stay in
bounds and s[left] == s[right]. Every successful expansion corresponds to one
distinct palindromic substring, so we increment a counter on each match.

Why it works: a substring is a palindrome iff its outer characters match and the
inner substring is a palindrome. Expanding around a fixed center enumerates
exactly the palindromes sharing that center, in increasing length, without
missing or double-counting any. Iterating over all 2n - 1 centers therefore
counts every palindromic substring exactly once.

Complexity
----------
Time:  O(n^2) - 2n - 1 centers, each expansion is at most O(n).
Space: O(1) auxiliary.

Alternative Approach (Dynamic Programming)
------------------------------------------
Let dp[i][j] be True if s[i..j] is a palindrome. Then:
    dp[i][j] = (s[i] == s[j]) and (j - i < 2 or dp[i + 1][j - 1])
Fill the table by increasing substring length and count all True entries.
This is also O(n^2) time but uses O(n^2) space. Manacher's algorithm can count
in O(n) but is far more intricate; expand-around-center is the interview-standard
answer.
"""


def countSubstrings(s: str) -> int:
    """Expand-around-center. Returns count of palindromic substrings."""
    n = len(s)
    count = 0

    def expand(left: int, right: int) -> int:
        c = 0
        while left >= 0 and right < n and s[left] == s[right]:
            c += 1
            left -= 1
            right += 1
        return c

    for center in range(n):
        count += expand(center, center)      # odd-length palindromes
        count += expand(center, center + 1)  # even-length palindromes
    return count


def countSubstrings_dp(s: str) -> int:
    """Dynamic programming alternative using a 2D palindrome table."""
    n = len(s)
    if n == 0:
        return 0
    dp = [[False] * n for _ in range(n)]
    count = 0
    # Iterate by substring length so inner subproblems are ready.
    for length in range(1, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and (length < 3 or dp[i + 1][j - 1]):
                dp[i][j] = True
                count += 1
    return count


if __name__ == "__main__":
    # Provided examples
    assert countSubstrings("abc") == 3
    assert countSubstrings("aaa") == 6

    # Single character
    assert countSubstrings("a") == 1

    # Even-length palindrome
    assert countSubstrings("aa") == 3          # "a", "a", "aa"

    # No repeats beyond singles
    assert countSubstrings("abcd") == 4

    # Mixed odd/even centers
    assert countSubstrings("aba") == 4         # a,b,a,aba
    assert countSubstrings("abba") == 6        # a,b,b,a,bb,abba

    # Longer known case: n singles + ...
    assert countSubstrings("racecar") == 10

    # DP alternative must agree with expand-around-center everywhere
    for t in ["abc", "aaa", "a", "aa", "abcd", "aba", "abba", "racecar",
              "zzzzz", "abacabad", "xyzzyx"]:
        assert countSubstrings(t) == countSubstrings_dp(t), t

    # All-same string of length k has k*(k+1)/2 palindromic substrings
    k = 5
    assert countSubstrings("z" * k) == k * (k + 1) // 2

    print("All tests passed for 647. Palindromic Substrings")
