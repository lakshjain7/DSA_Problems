"""
Problem 1312: Minimum Insertion Steps to Make a String Palindrome
Difficulty: Hard
Topics: String, Dynamic Programming

Given a string s. In one step you can insert any character at any index of the
string. Return the minimum number of steps to make s palindrome.
A Palindrome String is one that reads the same backward as well as forward.

Example 1:
    Input: s = "zzazz"
    Output: 0
    Explanation: The string "zzazz" is already palindrome.

Example 2:
    Input: s = "mbadm"
    Output: 2
    Explanation: String can be "mbdadbm" or "mdbabdm".

Example 3:
    Input: s = "leetcode"
    Output: 5
    Explanation: Inserting 5 characters the string becomes "leetcodocteel".

Constraints:
    1 <= s.length <= 500
    s consists of lowercase English letters.

Approach (interval DP):
    Let dp[i][j] be the min insertions to make s[i..j] a palindrome.
    - If s[i] == s[j]: dp[i][j] = dp[i+1][j-1]
    - Else: we must mirror one end:
      dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])
    Base: single chars / empty intervals cost 0. Fill by increasing length.
    Compress to O(n) rows by keeping only the previous two diagonals/rows.

Complexity:
    Time: O(n^2)   Space: O(n^2) for the 2D table, O(n) for the rolled version

Alternative (LPS): the characters not in the longest palindromic subsequence
need a mirror partner, so answer = n - LPS(s) = n - LCS(s, reversed(s)).
Time O(n^2), Space O(n).
"""


def min_insertions(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] if length > 2 else 0
            else:
                dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]


def min_insertions_lcs(s: str) -> int:
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
    return n - prev[n]


if __name__ == "__main__":
    import random
    cases = {"zzazz": 0, "mbadm": 2, "leetcode": 5, "a": 0, "ab": 1,
             "aa": 0, "abc": 2, "aba": 0, "abcd": 3, "g": 0}
    for fn in (min_insertions, min_insertions_lcs):
        for s, want in cases.items():
            assert fn(s) == want, (fn.__name__, s, fn(s), want)
        assert fn("a" * 500) == 0
    random.seed(1)
    for _ in range(300):
        s = "".join(random.choice("abc") for _ in range(random.randint(1, 12)))
        assert min_insertions(s) == min_insertions_lcs(s)
    print("All tests passed")
