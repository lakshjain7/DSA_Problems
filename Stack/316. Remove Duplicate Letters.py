"""
316. Remove Duplicate Letters
Difficulty: Medium
Topics: String, Stack, Greedy, Monotonic Stack

Problem:
Given a string s, remove duplicate letters so that every letter appears once
and only once. You must make sure your result is the smallest in
lexicographical order among all possible results.
(Same as LeetCode 1081. Smallest Subsequence of Distinct Characters.)

Example 1:
    Input: s = "bcabc"
    Output: "abc"

Example 2:
    Input: s = "cbacdcbc"
    Output: "acdb"

Constraints:
    1 <= s.length <= 10^4
    s consists of lowercase English letters.

Approach (Greedy monotonic stack):
    Record the last index of each character. Scan left to right keeping a
    stack of chosen characters and a set of characters already in the stack.
    For each char c not in the stack: while the stack top is greater than c AND
    the top appears again later (last[top] > i), pop it - we can place it later
    and get a lexicographically smaller prefix. Then push c. Chars already in
    the stack are skipped, because keeping the earlier copy is never worse.

Complexity:
    Time:  O(n) - each char pushed and popped at most once
    Space: O(1) - at most 26 characters in the stack

Alternative (Recursive greedy):
    Find the smallest character whose suffix still contains all remaining
    distinct letters, take it, and recurse on the suffix with that char removed.
    Time O(26 * n), space O(n) for recursion/strings.
"""
from itertools import combinations


def remove_duplicate_letters(s: str) -> str:
    last = {ch: i for i, ch in enumerate(s)}
    stack: list = []
    in_stack = set()
    for i, ch in enumerate(s):
        if ch in in_stack:
            continue
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            in_stack.discard(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return "".join(stack)


def remove_duplicate_letters_recursive(s: str) -> str:
    if not s:
        return ""
    # Smallest char whose suffix still contains every distinct letter.
    pos = 0
    for i, ch in enumerate(s):
        if ch < s[pos]:
            pos = i
        if s.count(ch, i) == 1:  # last occurrence of ch: cannot skip past it
            break
    ch = s[pos]
    return ch + remove_duplicate_letters_recursive(s[pos + 1:].replace(ch, ""))


def _brute(s: str) -> str:
    distinct = set(s)
    best = None
    n = len(s)
    for r in range(len(distinct), len(distinct) + 1):
        for idxs in combinations(range(n), r):
            cand = "".join(s[i] for i in idxs)
            if len(set(cand)) == r and (best is None or cand < best):
                best = cand
    return best


if __name__ == "__main__":
    import random

    for fn in (remove_duplicate_letters, remove_duplicate_letters_recursive):
        assert fn("bcabc") == "abc"
        assert fn("cbacdcbc") == "acdb"
        assert fn("a") == "a"
        assert fn("aaaa") == "a"
        assert fn("abcd") == "abcd"
        assert fn("dcba") == "dcba"
        assert fn("ecbacba") == "eacb"
        assert fn("bbcaac") == "bac"

    random.seed(7)
    for _ in range(300):
        s = "".join(random.choice("abcd") for _ in range(random.randint(1, 10)))
        expected = _brute(s)
        assert remove_duplicate_letters(s) == expected, s
        assert remove_duplicate_letters_recursive(s) == expected, s
    print("All tests passed.")
