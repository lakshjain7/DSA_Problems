"""
3. Longest Substring Without Repeating Characters
Difficulty: Medium
Topics: Hash Table, String, Sliding Window

=== PROBLEM ===
Given a string s, find the length of the longest substring without duplicate characters.

Example 1:
    Input:  s = "abcabcbb"
    Output: 3
    Explanation: "abc" has length 3

Example 2:
    Input:  s = "bbbbb"
    Output: 1
    Explanation: "b" has length 1

Example 3:
    Input:  s = "pwwkew"
    Output: 3
    Explanation: "wke" has length 3

Constraints:
    0 <= s.length <= 5 * 10^4
    s consists of English letters, digits, symbols and spaces.

=== APPROACH: Sliding Window with Hash Map ===

Key Insight:
    Maintain a window [left, right] where all characters are unique.
    Use a dict to store the last seen index of each character.
    When we encounter a duplicate at index right, we jump left past
    the previous occurrence of that character.

Algorithm:
    1. left = 0, max_len = 0
    2. For each right in range(len(s)):
         char = s[right]
         If char is in our map AND map[char] >= left:
             left = map[char] + 1   ← jump past the duplicate
         map[char] = right
         max_len = max(max_len, right - left + 1)
    3. Return max_len

Why this works:
    - We never revisit characters; each index is processed once → O(n)
    - The map stores the most recent index so we can jump left directly
      instead of shrinking the window one step at a time.

Complexity:
    Time:  O(n) — single pass
    Space: O(min(n, 128)) — at most 128 ASCII characters in the map
"""

from typing import Optional


def length_of_longest_substring(s: str) -> int:
    last_seen = {}   # char → last seen index
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        # If char was seen inside the current window, shrink from left
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len


# ─── Tests ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("au") == 2
    assert length_of_longest_substring("dvdf") == 3   # "vdf"
    print("All tests passed!")
