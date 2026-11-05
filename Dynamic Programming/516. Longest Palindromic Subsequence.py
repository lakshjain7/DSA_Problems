"""
516. Longest Palindromic Subsequence
Difficulty: Medium
Topics: String, Dynamic Programming

Given a string s, find the longest palindromic subsequence's length in s.
A subsequence is a sequence that can be derived from another sequence by
deleting some or no elements without changing the order of the remaining
elements.

Example 1:
    Input: s = "bbbab"
    Output: 4          (one possible longest palindromic subsequence is "bbbb")
Example 2:
    Input: s = "cbbd"
    Output: 2          ("bb")

Constraints:
    1 <= s.length <= 1000
    s consists only of lowercase English letters.

Approach (interval DP):
    Let dp[i][j] be the LPS length of s[i..j].
      - if s[i] == s[j]: dp[i][j] = dp[i+1][j-1] + 2
      - else:            dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    Base: dp[i][i] = 1, empty range = 0. Rows depend only on row i+1 and the
    current row, so we compress to O(n) space.

Complexity:
    Time:  O(n^2)
    Space: O(n) (rolling 1-D array); O(n^2) for the 2-D alternative.

Alternative: LPS(s) == LCS(s, reverse(s)).
"""


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        dp = [0] * n  # dp[j] holds dp[i][j] for the current i
        for i in range(n - 1, -1, -1):
            prev_diag = 0  # dp[i+1][j-1]
            dp[i] = 1
            for j in range(i + 1, n):
                tmp = dp[j]  # dp[i+1][j]
                if s[i] == s[j]:
                    dp[j] = prev_diag + 2
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                prev_diag = tmp
        return dp[n - 1]

    def longestPalindromeSubseqLCS(self, s: str) -> int:
        t = s[::-1]
        n = len(s)
        prev = [0] * (n + 1)
        for i in range(1, n + 1):
            cur = [0] * (n + 1)
            for j in range(1, n + 1):
                if s[i - 1] == t[j - 1]:
                    cur[j] = prev[j - 1] + 1
                else:
                    cur[j] = max(prev[j], cur[j - 1])
            prev = cur
        return prev[n]


if __name__ == "__main__":
    sol = Solution()
    cases = [("bbbab", 4), ("cbbd", 2), ("a", 1), ("aa", 2), ("ab", 1),
             ("abcde", 1), ("racecar", 7), ("agbdba", 5), ("a" * 50, 50)]
    for s, exp in cases:
        assert sol.longestPalindromeSubseq(s) == exp, (s, exp)
        assert sol.longestPalindromeSubseqLCS(s) == exp, (s, exp)
    print("All tests passed.")
