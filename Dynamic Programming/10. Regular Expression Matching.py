"""
Problem 10: Regular Expression Matching
Difficulty: Hard
Topics: Dynamic Programming, Recursion, String

Problem Statement:
Given an input string s and a pattern p, implement regular expression matching
with support for '.' and '*' where:
    - '.' Matches any single character.
    - '*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

Examples:
    Input: s = "aa", p = "a"
    Output: false
    Explanation: "a" does not match the entire string "aa".

    Input: s = "aa", p = "a*"
    Output: true
    Explanation: '*' means zero or more of the preceding element 'a'. "aa" == "aa".

    Input: s = "ab", p = ".*"
    Output: true
    Explanation: ".*" means zero or more of any character.

Constraints:
    - 1 <= s.length <= 20
    - 1 <= p.length <= 30
    - s contains only lowercase English letters.
    - p contains only lowercase English letters, '.', and '*'.
    - It is guaranteed for each occurrence of '*', there will be a valid preceding element.

Approach (Bottom-Up DP):
    dp[i][j] = True if s[i:] matches p[j:].
    Base case: dp[len(s)][len(p)] = True (both exhausted).
    Transition:
      - first_match = i < len(s) and (p[j] == s[i] or p[j] == '.')
      - If p[j+1] == '*':
          dp[i][j] = dp[i][j+2]  (use '*' as zero occurrences)
                  OR (first_match AND dp[i+1][j])  (use '*' for one+ occurrence)
      - Else:
          dp[i][j] = first_match AND dp[i+1][j+1]

Complexity:
    Time:  O(m * n) where m = len(s), n = len(p)
    Space: O(m * n) for table; reducible to O(n) with row compression
"""


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        # dp[i][j] = does s[i:] match p[j:]?
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True

        # Fill bottom-up (from end of both strings)
        for i in range(m, -1, -1):
            for j in range(n - 1, -1, -1):
                first_match = i < m and (p[j] == s[i] or p[j] == '.')
                if j + 1 < n and p[j + 1] == '*':
                    # Either skip x* entirely, or consume one char and stay at j
                    dp[i][j] = dp[i][j + 2] or (first_match and dp[i + 1][j])
                else:
                    dp[i][j] = first_match and dp[i + 1][j + 1]

        return dp[0][0]


class SolutionMemo:
    """Top-down memoized recursion."""
    def isMatch(self, s: str, p: str) -> bool:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(i: int, j: int) -> bool:
            if j == len(p):
                return i == len(s)
            first_match = i < len(s) and (p[j] == s[i] or p[j] == '.')
            if j + 1 < len(p) and p[j + 1] == '*':
                return dp(i, j + 2) or (first_match and dp(i + 1, j))
            return first_match and dp(i + 1, j + 1)

        return dp(0, 0)


if __name__ == "__main__":
    sol = Solution()
    sol_memo = SolutionMemo()

    for fn in [sol.isMatch, sol_memo.isMatch]:
        # Test 1: no match
        assert fn("aa", "a") == False

        # Test 2: a* matches aa
        assert fn("aa", "a*") == True

        # Test 3: .* matches anything
        assert fn("ab", ".*") == True

        # Test 4: "aab" with "c*a*b"
        assert fn("aab", "c*a*b") == True  # c* = empty, a* = aa, b = b

        # Test 5: tricky mississippi case
        assert fn("mississippi", "mis*is*p*.") == False

        # Test 6: dot matches single char
        assert fn("ab", "a.") == True

        # Test 7: b* matches zero b's
        assert fn("a", "ab*") == True

        # Test 8: edge cases
        assert fn("a", ".") == True
        assert fn("", "") == True
        assert fn("", "a*") == True     # a* = zero a's

        # Test 9: complex patterns
        assert fn("aaa", "a*a") == True
        assert fn("aaa", "ab*a") == False
        assert fn("aaa", "ab*ac*a") == True

    print("All tests passed!")
