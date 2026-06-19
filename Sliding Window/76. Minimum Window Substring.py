"""
Problem: 76. Minimum Window Substring
Difficulty: Hard
Topics: String, Sliding Window, Hash Table, Two Pointers

Given two strings s and t, return the minimum window substring of s such that
every character in t is included in the window.

Examples:
    s = "ADOBECODEBANC", t = "ABC" -> "BANC"
    s = "a", t = "a" -> "a"
    s = "a", t = "aa" -> ""

Approach: Sliding Window with have/required counters — O(m+n)
Expand right until all chars satisfied, then shrink from left.
"""

from collections import Counter


def minWindow(s: str, t: str) -> str:
    if not t or not s:
        return ""

    need = Counter(t)
    window = {}
    required = len(need)
    have = 0

    left = 0
    best_len = float('inf')
    best_left = 0

    for right in range(len(s)):
        c = s[right]
        window[c] = window.get(c, 0) + 1

        if c in need and window[c] == need[c]:
            have += 1

        while have == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_left = left

            left_c = s[left]
            window[left_c] -= 1
            if left_c in need and window[left_c] < need[left_c]:
                have -= 1
            left += 1

    return s[best_left:best_left + best_len] if best_len != float('inf') else ""


if __name__ == "__main__":
    assert minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert minWindow("a", "a") == "a"
    assert minWindow("a", "aa") == ""
    assert minWindow("abc", "d") == ""
    assert minWindow("abc", "abc") == "abc"
    assert minWindow("aa", "aa") == "aa"
    assert minWindow("ab", "ba") == "ab"
    assert minWindow("a", "A") == ""
    assert minWindow("aA", "A") == "A"
    print("All tests passed for 76. Minimum Window Substring!")
