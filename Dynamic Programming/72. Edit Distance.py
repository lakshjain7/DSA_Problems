"""
Problem #72 — Edit Distance
Difficulty : Hard
Topics     : Dynamic Programming, Strings

Minimum insert/delete/replace operations to convert word1 to word2.
dp[i][j] = min edits for word1[:i] -> word2[:j].
Complexity: O(m*n) time, O(m*n) space (reducible to O(min(m,n))).
"""


def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


def minDistance_optimised(word1: str, word2: str) -> int:
    if len(word1) < len(word2):
        word1, word2 = word2, word1
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr
    return prev[n]


if __name__ == "__main__":
    assert minDistance("horse", "ros") == 3
    assert minDistance("intention", "execution") == 5
    assert minDistance("", "") == 0
    assert minDistance("abc", "") == 3
    assert minDistance("", "abc") == 3
    assert minDistance("abc", "abc") == 0
    assert minDistance("a", "b") == 1
    assert minDistance("ab", "ba") == 2
    assert minDistance("kitten", "sitting") == 3
    assert minDistance("sunday", "saturday") == 3
    assert minDistance_optimised("horse", "ros") == 3
    assert minDistance_optimised("intention", "execution") == 5
    assert minDistance_optimised("kitten", "sitting") == 3
    assert minDistance_optimised("", "abc") == 3
    assert minDistance_optimised("abc", "") == 3
    print("All tests passed for 72. Edit Distance ✓")
