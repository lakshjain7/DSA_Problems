"""
87. Scramble String
Difficulty: Hard
Topics: String, Dynamic Programming, Memoization

Problem:
We can scramble a string s to get a string t using the following algorithm:
  1. If the length of the string is 1, stop.
  2. If the length is > 1, do the following:
     - Split the string into two non-empty substrings at a random index, i.e.
       if s is x + y, split into x and y.
     - Randomly decide to swap the two substrings or keep them in the same
       order: s may become x + y or y + x.
     - Apply step 1 recursively to each of the two substrings.
Given two strings s1 and s2 of the same length, return true if s2 is a
scrambled string of s1, otherwise return false.

Example 1:
  Input: s1 = "great", s2 = "rgeat"   Output: true
Example 2:
  Input: s1 = "abcde", s2 = "caebd"   Output: false
Example 3:
  Input: s1 = "a", s2 = "a"           Output: true

Constraints:
  s1.length == s2.length
  1 <= s1.length <= 30
  s1 and s2 consist of lowercase English letters.

Approach (memoized recursion):
  s2 is a scramble of s1 iff for some split point k (1 <= k < n) either
    - no swap:  s1[:k] ~ s2[:k]  and s1[k:] ~ s2[k:]
    - swap:     s1[:k] ~ s2[n-k:] and s1[k:] ~ s2[:n-k]
  where ~ means "is a scramble of". Memoize on (s1, s2) pairs (substrings).
  Prune early: if the two strings are equal the answer is True; if their
  sorted characters differ (not anagrams) the answer is False.

Complexity:
  Time:  O(n^4) -- O(n^3) distinct (i, j, length) states, O(n) splits each
  Space: O(n^3) for the memo (plus recursion depth O(n))

Alternative: bottom-up DP dp[len][i][j] = s1[i:i+len] ~ s2[j:j+len], same
O(n^4) time and O(n^3) space.
"""
from functools import lru_cache


class Solution:
    def isScramble(self, s1: str, s2: str) -> bool:
        if len(s1) != len(s2):
            return False

        @lru_cache(maxsize=None)
        def go(a: str, b: str) -> bool:
            if a == b:
                return True
            if sorted(a) != sorted(b):
                return False
            n = len(a)
            for k in range(1, n):
                if go(a[:k], b[:k]) and go(a[k:], b[k:]):
                    return True
                if go(a[:k], b[n - k:]) and go(a[k:], b[:n - k]):
                    return True
            return False

        return go(s1, s2)

    def isScrambleBottomUp(self, s1: str, s2: str) -> bool:
        """Alternative: iterative DP over (length, i, j)."""
        n = len(s1)
        if n != len(s2):
            return False
        # dp[l][i][j]: s1[i:i+l] is a scramble of s2[j:j+l]
        dp = [[[False] * n for _ in range(n)] for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                dp[1][i][j] = s1[i] == s2[j]
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                for j in range(n - l + 1):
                    for k in range(1, l):
                        if dp[k][i][j] and dp[l - k][i + k][j + k]:
                            dp[l][i][j] = True
                            break
                        if dp[k][i][j + l - k] and dp[l - k][i + k][j]:
                            dp[l][i][j] = True
                            break
        return dp[n][0][0]


if __name__ == "__main__":
    s = Solution()
    cases = [
        ("great", "rgeat", True),
        ("abcde", "caebd", False),
        ("a", "a", True),
        ("a", "b", False),
        ("ab", "ba", True),
        ("abc", "bca", True),
        ("abcd", "badc", True),
        ("abcd", "bdac", False),
        ("aabb", "abab", True),
        ("abcdefghijklmnopq", "efghijklmnopqcadb", False),
        ("eebaacbcbcadaaedceaaacadccd", "eadcaacabaddaceacbceaabeccd", False),
    ]
    for a, b, exp in cases:
        assert s.isScramble(a, b) == exp, (a, b)
        if len(a) <= 12:
            assert s.isScrambleBottomUp(a, b) == exp, (a, b)
    assert s.isScramble("abcdefghijklmnopqrstuvwxyzabcd", "abcdefghijklmnopqrstuvwxyzabcd")
    print("All tests passed!")
