"""
828. Count Unique Characters of All Substrings of a Given String
Difficulty: Hard
Topics: Hash Table, String, Dynamic Programming

Problem:
Let's define a function countUniqueChars(s) that returns the number of unique
characters in s (characters that appear exactly once).

    For example, calling countUniqueChars(s) if s = "LEETCODE" then "L", "T", "C",
    "O", "D" are the unique characters since they appear only once in s, therefore
    countUniqueChars(s) = 5.

Given a string s, return the sum of countUniqueChars(t) where t is a substring of s.
The test cases are generated such that the answer fits in a 32-bit integer.

Notice that some substrings can be repeated, so in this case you have to count the
repeated ones too.

Example 1:
    Input: s = "ABC"
    Output: 10
    Explanation: All possible substrings are: "A","B","C","AB","BC" and "ABC".
    Every substring is composed with only unique letters.
    Sum of lengths of all substrings is 1 + 1 + 1 + 2 + 2 + 3 = 10

Example 2:
    Input: s = "ABA"
    Output: 8
    Explanation: The same as example 1, except countUniqueChars("ABA") = 1.

Example 3:
    Input: s = "LEETCODE"
    Output: 92

Constraints:
    1 <= s.length <= 10^5
    s consists of uppercase English letters only.

Approach (contribution technique):
    Flip the sum: instead of asking "how many unique chars does each substring
    have?", ask "in how many substrings is position i the *only* occurrence of
    s[i]?". Let prev be the previous index of the same letter (or -1) and nxt the
    next index (or n). A substring [l, r] counts s[i] as unique iff
    prev < l <= i <= r < nxt, giving (i - prev) * (nxt - i) substrings.
    Summing that over all i yields the answer.

    One-pass implementation: keep, for each letter, its last two positions
    (p2 < p1). When we see the letter again at i, we now know the "next" of p1,
    so we finalise p1's contribution (p1 - p2) * (i - p1). After the scan, every
    letter's last occurrence is finalised with nxt = n.

Complexity:
    Time:  O(n)
    Space: O(1) - 26 letters x 2 positions.

Alternative (DP over right endpoint):
    Let cur = sum of unique counts over all substrings ending at i. Moving from
    i-1 to i, s[i] gains (i - last[c]) substrings where it's unique, and loses
    (last[c] - prev_last[c]) where its previous occurrence used to be unique.
    cur += (i - last) - (last - prev_last); answer += cur. Also O(n)/O(1).
"""

from typing import List


class Solution:
    def uniqueLetterString(self, s: str) -> int:
        n = len(s)
        last = [[-1, -1] for _ in range(26)]  # [second-last, last]
        total = 0
        for i, ch in enumerate(s):
            c = ord(ch) - 65
            p2, p1 = last[c]
            if p1 != -1:
                total += (p1 - p2) * (i - p1)
            last[c] = [p1, i]
        for p2, p1 in last:
            if p1 != -1:
                total += (p1 - p2) * (n - p1)
        return total

    def uniqueLetterStringDP(self, s: str) -> int:
        last: List[int] = [-1] * 26
        prev_last: List[int] = [-1] * 26
        cur = total = 0
        for i, ch in enumerate(s):
            c = ord(ch) - 65
            cur += (i - last[c]) - (last[c] - prev_last[c])
            prev_last[c], last[c] = last[c], i
            total += cur
        return total


def _brute(s: str) -> int:
    from collections import Counter
    total = 0
    for i in range(len(s)):
        cnt = Counter()
        for j in range(i, len(s)):
            cnt[s[j]] += 1
            total += sum(1 for v in cnt.values() if v == 1)
    return total


if __name__ == "__main__":
    import random

    sol = Solution()
    cases = [
        ("ABC", 10),
        ("ABA", 8),
        ("LEETCODE", 92),
        ("A", 1),
        ("AA", 2),     # "A","A" unique; "AA" has none
        ("AAA", 3),
        ("ABAB", 12),
    ]
    for s, exp in cases:
        assert sol.uniqueLetterString(s) == exp, s
        assert sol.uniqueLetterStringDP(s) == exp, s
        assert _brute(s) == exp, s

    random.seed(2)
    for _ in range(300):
        s = "".join(random.choice("ABCD") for _ in range(random.randint(1, 30)))
        e = _brute(s)
        assert sol.uniqueLetterString(s) == e, s
        assert sol.uniqueLetterStringDP(s) == e, s

    big = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(10**5))
    assert sol.uniqueLetterString(big) == sol.uniqueLetterStringDP(big)
    print("All tests passed!")
