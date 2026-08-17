"""
22. Generate Parentheses
Difficulty: Medium
Topics: String, Dynamic Programming, Backtracking

Problem Statement
-----------------
Given n pairs of parentheses, write a function to generate all combinations
of well-formed parentheses.

Example 1:
    Input:  n = 3
    Output: ["((()))","(()())","(())()","()(())","()()()"]

Example 2:
    Input:  n = 1
    Output: ["()"]

Constraints:
    1 <= n <= 8


Approach (Backtracking)
-----------------------
Build the string one character at a time, tracking how many '(' and ')'
have been placed. Two rules keep every partial string a valid prefix:

1. We may add '(' as long as we have used fewer than n of them
   (open < n).
2. We may add ')' only when it would close an existing unmatched '('
   (close < open).

When the string reaches length 2 * n it is a complete, balanced
combination, so we record it. Because we only ever extend valid prefixes,
we never generate an invalid string and never need to filter afterwards.

Why it works:
- A parenthesis string of length 2n is valid iff every prefix has
  #'(' >= #')' and the totals are equal. Rule 2 enforces the prefix
  invariant; reaching length 2n with open == close == n enforces equality.

Complexity
----------
Let C(n) be the nth Catalan number (the number of valid results).
Time:  O(4^n / sqrt(n)) - proportional to C(n) strings, each of length 2n.
Space: O(n) recursion depth (excluding the output list).
"""

from typing import List


def generateParenthesis(n: int) -> List[str]:
    result: List[str] = []
    path: List[str] = []

    def backtrack(open_count: int, close_count: int) -> None:
        if len(path) == 2 * n:
            result.append("".join(path))
            return

        if open_count < n:
            path.append("(")
            backtrack(open_count + 1, close_count)
            path.pop()

        if close_count < open_count:
            path.append(")")
            backtrack(open_count, close_count + 1)
            path.pop()

    backtrack(0, 0)
    return result


def generateParenthesis_dp(n: int) -> List[str]:
    """
    Alternative approach: dynamic programming on structure.
    Every valid string of n pairs has the unique form:
        "(" + A + ")" + B
    where A uses i pairs and B uses n-1-i pairs, for i in [0, n-1].
    Build the table bottom-up from dp[0] = [""].
    """
    dp: List[List[str]] = [[""] for _ in range(n + 1)]
    for total in range(1, n + 1):
        combos: List[str] = []
        for i in range(total):
            for inside in dp[i]:
                for tail in dp[total - 1 - i]:
                    combos.append("(" + inside + ")" + tail)
        dp[total] = combos
    return dp[n]


if __name__ == "__main__":
    # Example 2 (smallest case)
    assert generateParenthesis(1) == ["()"]

    # Example 1 - compare as sets since order is not specified by the problem.
    expected_3 = {"((()))", "(()())", "(())()", "()(())", "()()()"}
    assert set(generateParenthesis(3)) == expected_3

    # Count must equal the Catalan number for each n.
    catalan = [1, 1, 2, 5, 14, 42, 132, 429, 1430]
    for k in range(1, 9):
        out = generateParenthesis(k)
        assert len(out) == catalan[k], (k, len(out))
        # No duplicates.
        assert len(set(out)) == len(out)
        # Every result is balanced.
        for s in out:
            bal = 0
            for ch in s:
                bal += 1 if ch == "(" else -1
                assert bal >= 0
            assert bal == 0

    # Both approaches must agree (as sets) for all n in range.
    for k in range(1, 9):
        assert set(generateParenthesis(k)) == set(generateParenthesis_dp(k))

    print("All tests passed for 22. Generate Parentheses")
