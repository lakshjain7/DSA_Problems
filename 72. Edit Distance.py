"""
Problem #72 — Edit Distance
Difficulty : Hard
Topics     : Dynamic Programming, Strings

─────────────────────────────────────────────────────────────────────────────
PROBLEM STATEMENT
─────────────────────────────────────────────────────────────────────────────
Given two strings word1 and word2, return the minimum number of operations
required to convert word1 into word2.

You have the following three operations permitted on a word:
  • Insert a character
  • Delete a character
  • Replace a character

Examples:
  Input : word1 = "horse", word2 = "ros"    Output: 3
    horse → rorse (replace 'h' with 'r')
    rorse → rose  (delete 'r')
    rose  → ros   (delete 'e')

  Input : word1 = "intention", word2 = "execution"   Output: 5

Constraints:
  0 <= word1.length, word2.length <= 500
  word1 and word2 consist of lowercase English letters.

─────────────────────────────────────────────────────────────────────────────
APPROACH — 2-D DP (Levenshtein Distance)
─────────────────────────────────────────────────────────────────────────────
Define dp[i][j] = minimum edits to convert word1[:i] → word2[:j].

Base cases:
  dp[i][0] = i   (delete i chars from word1)
  dp[0][j] = j   (insert j chars from word2)

Transition:
  If word1[i-1] == word2[j-1]:
      dp[i][j] = dp[i-1][j-1]          # characters match, no extra cost
  Else:
      dp[i][j] = 1 + min(
          dp[i-1][j],     # delete from word1
          dp[i][j-1],     # insert into word1
          dp[i-1][j-1]    # replace in word1
      )

Answer: dp[m][n]

─────────────────────────────────────────────────────────────────────────────
COMPLEXITY
─────────────────────────────────────────────────────────────────────────────
Time  : O(m × n)   — fill an m×n table
Space : O(m × n)   — the table itself
        (can be reduced to O(min(m,n)) with a rolling two-row approach)
"""


def minDistance(word1: str, word2: str) -> int:
    """Return the Levenshtein (edit) distance between word1 and word2."""
    m, n = len(word1), len(word2)

    # dp[i][j]: min edits to convert word1[:i] → word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],     # delete
                    dp[i][j - 1],     # insert
                    dp[i - 1][j - 1]  # replace
                )

    return dp[m][n]


# ─────────────────────────────────────────────────────────────────────────────
# ALTERNATIVE APPROACH — Space-optimised rolling two rows
# ─────────────────────────────────────────────────────────────────────────────
def minDistance_optimised(word1: str, word2: str) -> int:
    """
    Use only two 1-D arrays (previous row and current row) instead of
    the full m×n table.

    Time : O(m × n)   Space: O(min(m, n))
    """
    # Ensure word2 is the shorter string for minimum space
    if len(word1) < len(word2):
        word1, word2 = word2, word1

    m, n = len(word1), len(word2)
    prev = list(range(n + 1))   # dp[0][0..n]

    for i in range(1, m + 1):
        curr = [i] + [0] * n    # dp[i][0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr

    return prev[n]


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Examples from the problem statement
    assert minDistance("horse", "ros") == 3,               "TC1 failed"
    assert minDistance("intention", "execution") == 5,     "TC2 failed"

    # Edge cases
    assert minDistance("", "") == 0,                       "Both empty"
    assert minDistance("abc", "") == 3,                    "Delete all"
    assert minDistance("", "abc") == 3,                    "Insert all"
    assert minDistance("abc", "abc") == 0,                 "Identical strings"
    assert minDistance("a", "b") == 1,                     "Single char replace"
    assert minDistance("ab", "ba") == 2,                   "Swap (replace twice)"
    assert minDistance("kitten", "sitting") == 3,          "Classic Levenshtein"
    assert minDistance("sunday", "saturday") == 3,         "saturday example"

    # Optimised version must match
    assert minDistance_optimised("horse", "ros") == 3
    assert minDistance_optimised("intention", "execution") == 5
    assert minDistance_optimised("kitten", "sitting") == 3
    assert minDistance_optimised("", "abc") == 3
    assert minDistance_optimised("abc", "") == 3

    print("All tests passed for 72. Edit Distance ✓")
