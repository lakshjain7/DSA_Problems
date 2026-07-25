"""
131. Palindrome Partitioning
Difficulty: Medium
Topics: String, Backtracking, Dynamic Programming, Recursion

Problem Statement
-----------------
Given a string `s`, partition `s` such that every substring of the partition
is a palindrome. Return all possible palindrome partitionings of `s`.

Examples
--------
Example 1:
    Input:  s = "aab"
    Output: [["a","a","b"],["aa","b"]]

Example 2:
    Input:  s = "a"
    Output: [["a"]]

Constraints
-----------
- 1 <= s.length <= 16
- s contains only lowercase English letters.

Approach (Backtracking with palindrome checks)
----------------------------------------------
We explore every way to cut the string from left to right. Starting at index
`start`, we try every possible end index `end`. If the substring
s[start:end+1] is a palindrome, we add it to the current path and recurse from
`end + 1`. When `start` reaches the end of the string, the current path is one
valid partition and we record a copy of it.

Because s.length <= 16, the exponential number of partitions (up to 2^(n-1))
is small enough to enumerate directly.

Optimization
------------
Naively re-checking each candidate substring for being a palindrome costs
O(n) per check. We precompute a boolean DP table `is_pal[i][j]` = whether
s[i..j] is a palindrome, using the recurrence:
    is_pal[i][j] = (s[i] == s[j]) and (j - i < 2 or is_pal[i+1][j-1])
This makes each palindrome test O(1) inside the backtracking.

Why it works
------------
Every partition of the string corresponds to a unique choice of cut points.
By only descending into substrings that are palindromes, we prune the search
tree to exactly the valid partitions, and the base case (start == n) captures
each complete valid partition once.

Complexity
----------
Let n = len(s).
Time:  O(n * 2^n) - up to 2^(n-1) partitions, each of length up to n to copy.
Space: O(n^2) for the palindrome DP table, plus O(n) recursion depth
       (output not counted).
"""

from typing import List


def partition(s: str) -> List[List[str]]:
    """Return all palindrome partitions of s using backtracking + DP table."""
    n = len(s)

    # Precompute palindrome table: is_pal[i][j] == True iff s[i..j] is a palindrome.
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True

    result: List[List[str]] = []
    path: List[str] = []

    def backtrack(start: int) -> None:
        if start == n:
            result.append(path[:])
            return
        for end in range(start, n):
            if is_pal[start][end]:
                path.append(s[start:end + 1])
                backtrack(end + 1)
                path.pop()

    backtrack(0)
    return result


def partition_simple(s: str) -> List[List[str]]:
    """Alternative without the DP table (checks palindromes on the fly)."""
    result: List[List[str]] = []
    path: List[str] = []

    def backtrack(start: int) -> None:
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start, len(s)):
            sub = s[start:end + 1]
            if sub == sub[::-1]:
                path.append(sub)
                backtrack(end + 1)
                path.pop()

    backtrack(0)
    return result


def _normalize(res: List[List[str]]):
    """Order-independent comparison helper."""
    return sorted(tuple(p) for p in res)


if __name__ == "__main__":
    # Example 1
    assert _normalize(partition("aab")) == _normalize([["a", "a", "b"], ["aa", "b"]])
    # Example 2
    assert _normalize(partition("a")) == _normalize([["a"]])

    # Full palindrome yields many partitions including the whole string
    res_aaa = partition("aaa")
    assert ["aaa"] in res_aaa
    assert ["a", "a", "a"] in res_aaa
    assert ["a", "aa"] in res_aaa and ["aa", "a"] in res_aaa
    assert len(res_aaa) == 4  # 2^(3-1) partitions, all palindromic

    # No multi-char palindromes -> only the single-character partition
    assert _normalize(partition("abc")) == _normalize([["a", "b", "c"]])

    # A known palindrome across the whole string
    assert ["aba"] in partition("aba")

    # Cross-check the two implementations on several inputs
    for word in ["aab", "a", "aaa", "abc", "aba", "abba", "racecar"]:
        assert _normalize(partition(word)) == _normalize(partition_simple(word))

    print("All tests passed for 131. Palindrome Partitioning")
