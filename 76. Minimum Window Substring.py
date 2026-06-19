"""
Problem: 76. Minimum Window Substring
Difficulty: Hard
Topics: String, Sliding Window, Hash Table, Two Pointers

Problem Statement:
    Given two strings s and t of lengths m and n, return the minimum window
    substring of s such that every character in t (including duplicates) is
    included in the window. If there is no such substring, return the empty string "".

    The test cases will be generated such that the answer is unique.

Examples:
    Input: s = "ADOBECODEBANC", t = "ABC"
    Output: "BANC"
    Explanation: "BANC" contains A, B, C and is the minimum such window.

    Input: s = "a", t = "a"
    Output: "a"

    Input: s = "a", t = "aa"
    Output: ""
    Explanation: Both 'a's from t must be in the window. Only one 'a' in s.

Constraints:
    - m == s.length, n == t.length
    - 1 <= m, n <= 10^5
    - s and t consist of uppercase and lowercase English letters.

Approach:
    Sliding Window with two frequency counters:
    - `need`: frequency map of characters required (from t)
    - `window`: frequency map of characters currently in the sliding window
    - `have`: number of character types currently satisfied (window[c] >= need[c])
    - `required`: total number of character types that must be satisfied (len(need))

    Expand right pointer: add s[right] to window, update `have` if newly satisfied.
    When have == required (all chars satisfied), try to shrink from the left:
      - Record current window if it's smaller than best
      - Remove s[left] from window, update `have` if a char type drops below needed
      - Advance left

    This achieves O(m + n) because each character is added and removed at most once.

Complexity:
    Time:  O(m + n) — each of the m characters in s is visited at most twice (expand + shrink)
                       plus O(n) to build the need map
    Space: O(m + n) — at most O(|Σ|) = O(52) for the counters, technically O(1)
                       for fixed alphabet; O(n) for need map

Alternative Approach:
    Filtered sliding window: if |t| << |s|, first filter s to only positions with
    chars in t. Then slide over filtered positions. Reduces constant factors for
    sparse matches. Same asymptotic complexity.
"""

from collections import Counter
from typing import Tuple


def minWindow(s: str, t: str) -> str:
    """
    Find minimum window substring of s containing all characters of t.

    Args:
        s: Source string to search within.
        t: Target string whose characters must all appear in the window.

    Returns:
        Minimum window substring, or "" if no valid window exists.
    """
    if not t or not s:
        return ""

    need = Counter(t)          # {char: count_needed}
    window = {}                # {char: count_in_current_window}
    required = len(need)       # distinct chars we need to satisfy
    have = 0                   # distinct chars currently satisfied

    left = 0
    best_len = float('inf')
    best_left = 0

    for right in range(len(s)):
        # Expand: add s[right] to window
        c = s[right]
        window[c] = window.get(c, 0) + 1

        # Check if this char type is now fully satisfied
        if c in need and window[c] == need[c]:
            have += 1

        # Shrink: while all requirements are met, try to minimize window
        while have == required:
            # Update best window if current is smaller
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_left = left

            # Remove s[left] from window
            left_c = s[left]
            window[left_c] -= 1
            if left_c in need and window[left_c] < need[left_c]:
                have -= 1
            left += 1

    return s[best_left:best_left + best_len] if best_len != float('inf') else ""


def minWindow_filtered(s: str, t: str) -> str:
    """
    Alternative: Filtered sliding window — only slide over chars that appear in t.
    Better constant factor when |t| << |s|.
    """
    if not t or not s:
        return ""

    need = Counter(t)
    # Filter s to only positions with chars in t
    filtered = [(i, c) for i, c in enumerate(s) if c in need]

    window = {}
    required = len(need)
    have = 0
    left = 0
    best_len = float('inf')
    best_left = 0

    for right in range(len(filtered)):
        idx, c = filtered[right]
        window[c] = window.get(c, 0) + 1
        if window[c] == need[c]:
            have += 1

        while have == required:
            l_idx, l_c = filtered[left]
            window_len = idx - l_idx + 1
            if window_len < best_len:
                best_len = window_len
                best_left = l_idx
            window[l_c] -= 1
            if window[l_c] < need[l_c]:
                have -= 1
            left += 1

    return s[best_left:best_left + best_len] if best_len != float('inf') else ""


if __name__ == "__main__":
    # Basic examples from problem
    assert minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert minWindow("a", "a") == "a"
    assert minWindow("a", "aa") == ""

    # t not present at all
    assert minWindow("abc", "d") == ""

    # s == t
    assert minWindow("abc", "abc") == "abc"

    # Duplicate chars in t
    assert minWindow("aa", "aa") == "aa"
    assert minWindow("aab", "aab") == "aab"

    # Window is whole string
    assert minWindow("ab", "ba") == "ab"

    # Multiple valid windows, return shortest
    result = minWindow("ADOBECODEBANC", "ABC")
    assert result == "BANC"

    # Case sensitive
    assert minWindow("a", "A") == ""
    assert minWindow("aA", "A") == "A"

    # Verify filtered version matches on all cases
    assert minWindow_filtered("ADOBECODEBANC", "ABC") == "BANC"
    assert minWindow_filtered("a", "aa") == ""
    assert minWindow_filtered("aa", "aa") == "aa"
    assert minWindow_filtered("ab", "ba") == "ab"

    # Longer stress case
    s = "aaaaaaaaaaaabbbbbcdd"
    t = "abcdd"
    result = minWindow(s, t)
    from collections import Counter
    result_counter = Counter(result)
    for ch, cnt in Counter(t).items():
        assert result_counter[ch] >= cnt
    for i in range(len(s)):
        for j in range(i, len(s)):
            window = s[i:j+1]
            w_cnt = Counter(window)
            valid = all(w_cnt[ch] >= cnt for ch, cnt in Counter(t).items())
            if valid:
                assert len(window) >= len(result)
                break

    print("All tests passed for 76. Minimum Window Substring!")
