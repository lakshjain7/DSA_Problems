"""
LeetCode 132. Palindrome Partitioning II
Difficulty: Hard
Topics: Dynamic Programming, String

Problem Statement:
    Given a string s, partition s such that every substring of the partition is
    a palindrome.

    Return the minimum number of cuts needed for a palindrome partitioning of s.

Examples:
    Example 1:
        Input:  s = "aab"
        Output: 1
        Explanation: The palindrome partitioning ["aa","b"] could be produced
                     using 1 cut.

    Example 2:
        Input:  s = "a"
        Output: 0

    Example 3:
        Input:  s = "ab"
        Output: 1

Constraints:
    - 1 <= s.length <= 2000
    - s consists of lowercase English letters only.

Approach (two-layer DP: palindrome table + min-cut DP):
    Step 1 - Precompute palindrome information.
        Build a 2D boolean table is_pal[i][j] that is True iff s[i..j]
        (inclusive) is a palindrome. Fill it by increasing substring length:
            s[i..j] is a palindrome  <=>  s[i] == s[j] AND
                                          (j - i < 2 OR is_pal[i+1][j-1]).
        This lets any palindrome test run in O(1).

    Step 2 - Minimum cuts DP.
        Let cut[i] = minimum cuts needed for the prefix s[0..i-1] (first i
        characters). We want cut[n].
            cut[0] = 0 (empty string needs no cut).
        For each end position i (1..n), consider every start j (0..i-1). If
        s[j..i-1] is a palindrome, then we can cut right before j:
            cut[i] = min(cut[i], cut[j] + (1 if j > 0 else 0))
        The +1 accounts for the cut separating the prefix s[0..j-1] from the
        palindrome piece s[j..i-1]; when j == 0 the whole prefix is itself a
        palindrome, needing 0 cuts.

Why it works:
    cut[i] is defined over strictly smaller prefixes, so the recurrence has no
    cycles and every subproblem is solved before it is used. Every valid
    palindrome partition of s[0..i-1] ends in some palindrome suffix s[j..i-1];
    enumerating all such j and taking the minimum over the already-optimal
    cut[j] guarantees the global optimum for cut[i].

Complexity:
    Let n = len(s).
    Time:  O(n^2) - building the palindrome table is O(n^2) and the cut DP is
           O(n^2).
    Space: O(n^2) for the palindrome table plus O(n) for the cut array.

Alternative:
    An O(n^2) time / O(n) space variant avoids the full table by expanding
    around each center and relaxing cut[] on the fly (provided below as
    minCutExpand).
"""

from typing import List


class Solution:
    def minCut(self, s: str) -> int:
        n = len(s)
        if n <= 1:
            return 0

        # Step 1: palindrome table.
        is_pal = [[False] * n for _ in range(n)]
        for i in range(n):
            is_pal[i][i] = True
        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and (length < 3 or is_pal[i + 1][j - 1]):
                    is_pal[i][j] = True

        # Step 2: min-cut DP.
        # cut[i] = min cuts for prefix of length i (s[0..i-1]).
        cut = [0] * (n + 1)
        for i in range(1, n + 1):
            best = i - 1  # worst case: cut between every character
            for j in range(i):
                if is_pal[j][i - 1]:
                    best = 0 if j == 0 else min(best, cut[j] + 1)
            cut[i] = best
        return cut[n]

    # Alternative approach: expand-around-center, O(n) space.
    def minCutExpand(self, s: str) -> int:
        n = len(s)
        if n <= 1:
            return 0
        # dp[i] = min cuts for prefix s[0..i-1]; dp[0] = -1 sentinel so that a
        # full-prefix palindrome yields 0 cuts.
        dp = [i - 1 for i in range(n + 1)]

        def expand(left: int, right: int) -> None:
            while left >= 0 and right < n and s[left] == s[right]:
                # s[left..right] is a palindrome; relax dp[right+1].
                dp[right + 1] = min(dp[right + 1], dp[left] + 1)
                left -= 1
                right += 1

        for center in range(n):
            expand(center, center)      # odd-length palindromes
            expand(center, center + 1)  # even-length palindromes
        return dp[n]


def _brute_min_cut(s: str) -> int:
    """Reference O(2^n) solver for cross-checking on small inputs."""
    n = len(s)

    def is_pal(a: int, b: int) -> bool:
        while a < b:
            if s[a] != s[b]:
                return False
            a += 1
            b -= 1
        return True

    best = [n]  # at most n-1 cuts, use n as an upper bound

    def rec(start: int, pieces: int) -> None:
        if start == n:
            best[0] = min(best[0], pieces - 1)  # cuts = pieces - 1
            return
        for end in range(start, n):
            if is_pal(start, end):
                rec(end + 1, pieces + 1)

    rec(0, 0)
    return best[0]


if __name__ == "__main__":
    sol = Solution()

    for solver in (sol.minCut, sol.minCutExpand):
        # Provided examples
        assert solver("aab") == 1
        assert solver("a") == 0
        assert solver("ab") == 1

        # Whole string already a palindrome -> 0 cuts
        assert solver("aba") == 0
        assert solver("aaaa") == 0

        # No palindromic substrings of length > 1 -> n-1 cuts
        assert solver("abcde") == 4

        # Mixed case
        assert solver("noonabbad") == 2  # noon | abba | d

        # Empty string edge case
        assert solver("") == 0

    # Cross-check DP solvers against brute force on many short strings
    import itertools

    for length in range(1, 8):
        for combo in itertools.product("ab", repeat=length):
            test = "".join(combo)
            expected = _brute_min_cut(test)
            assert sol.minCut(test) == expected, (test, sol.minCut(test), expected)
            assert sol.minCutExpand(test) == expected, (
                test,
                sol.minCutExpand(test),
                expected,
            )

    print("All tests passed for 132. Palindrome Partitioning II")
