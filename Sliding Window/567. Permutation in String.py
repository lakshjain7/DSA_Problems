"""
Problem: 567. Permutation in String
Difficulty: Medium
Topics: Sliding Window, Hash Map, String

Problem Statement:
    Given two strings s1 and s2, return true if s2 contains a permutation of s1,
    or false otherwise. In other words, return true if one of s1's permutations
    is a substring of s2.

Examples:
    Input: s1 = "ab", s2 = "eidbaooo"
    Output: True  (s2 contains "ba" which is a permutation of "ab")

    Input: s1 = "ab", s2 = "eidboaoo"
    Output: False

Constraints:
    - 1 <= s1.length, s2.length <= 10^4
    - s1 and s2 consist of lowercase English letters

Approach:
    Fixed-size sliding window of length len(s1) over s2.
    Maintain frequency counts for s1 and the current window.
    Track how many of the 26 characters have matching counts (matches variable).
    Slide the window: add right char, remove left char, update matches accordingly.
    If matches == 26, the window is a permutation of s1.

    This is more efficient than comparing entire dicts each step.

Complexity:
    Time:  O(26 + n) = O(n) where n = len(s2)
    Space: O(1) — fixed 26-char arrays

Alternative Approach:
    Sort s1 and every window substring → O(n * k log k) — much slower.
"""

from typing import List


def checkInclusion(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False

    count1 = [0] * 26
    count2 = [0] * 26

    for ch in s1:
        count1[ord(ch) - ord('a')] += 1

    # Initialize first window
    for ch in s2[:len(s1)]:
        count2[ord(ch) - ord('a')] += 1

    # Count matching character frequencies
    matches = sum(1 for i in range(26) if count1[i] == count2[i])

    if matches == 26:
        return True

    left = 0
    for right in range(len(s1), len(s2)):
        # Add right character
        r_idx = ord(s2[right]) - ord('a')
        # Before adding: was it matching?
        if count1[r_idx] == count2[r_idx]:
            matches -= 1
        count2[r_idx] += 1
        if count1[r_idx] == count2[r_idx]:
            matches += 1

        # Remove left character
        l_idx = ord(s2[left]) - ord('a')
        if count1[l_idx] == count2[l_idx]:
            matches -= 1
        count2[l_idx] -= 1
        if count1[l_idx] == count2[l_idx]:
            matches += 1

        left += 1

        if matches == 26:
            return True

    return False


if __name__ == "__main__":
    # Basic cases
    assert checkInclusion("ab", "eidbaooo") == True
    assert checkInclusion("ab", "eidboaoo") == False
    assert checkInclusion("adc", "dcda") == True

    # Edge cases
    assert checkInclusion("a", "a") == True
    assert checkInclusion("a", "b") == False
    assert checkInclusion("abc", "ab") == False   # s1 longer than s2
    assert checkInclusion("aa", "aa") == True
    assert checkInclusion("abc", "cbabadcbbabbbc") == True

    # Single char
    assert checkInclusion("z", "zzz") == True
    assert checkInclusion("z", "abc") == False

    print("All tests passed!")
