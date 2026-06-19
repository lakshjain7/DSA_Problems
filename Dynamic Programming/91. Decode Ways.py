"""
Problem #91 — Decode Ways
Difficulty: Medium
Topics: Dynamic Programming, String

dp[i] = ways to decode s[0:i]. Single-digit and two-digit transitions.
Complexity: O(n) time, O(n) space (reducible to O(1)).
"""


def numDecodings(s: str) -> int:
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 0 if s[0] == '0' else 1

    for i in range(2, n + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        two_digit = int(s[i - 2: i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]

    return dp[n]


def numDecodings_constant_space(s: str) -> int:
    n = len(s)
    prev2 = 1
    prev1 = 0 if s[0] == '0' else 1

    for i in range(2, n + 1):
        curr = 0
        if s[i - 1] != '0':
            curr += prev1
        two_digit = int(s[i - 2: i])
        if 10 <= two_digit <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr

    return prev1 if n >= 2 else (0 if s[0] == '0' else 1)


if __name__ == "__main__":
    assert numDecodings("12") == 2
    assert numDecodings("226") == 3
    assert numDecodings("06") == 0
    assert numDecodings("0") == 0
    assert numDecodings("1") == 1
    assert numDecodings("10") == 1
    assert numDecodings("100") == 0
    assert numDecodings("27") == 1
    assert numDecodings("1111") == 5
    assert numDecodings("11106") == 2
    assert numDecodings("111") == 3
    assert numDecodings("1111") == 5
    for case, expected in [("12", 2), ("226", 3), ("06", 0), ("0", 0),
                            ("10", 1), ("100", 0), ("11106", 2)]:
        result = numDecodings_constant_space(case)
        assert result == expected
    print("All tests passed!")
