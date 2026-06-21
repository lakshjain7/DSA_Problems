"""
Problem #438: Find All Anagrams in a String
Difficulty: Medium
Topics: Sliding Window, Hash Map, String

Problem Statement:
    Given two strings s and p, return an array of all the start indices of p's anagrams in s.
    You may return the answer in any order.
    An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase,
    typically using all the original letters exactly once.

Examples:
    Example 1:
        Input: s = "cbaebabacd", p = "abc"
        Output: [0, 6]
        Explanation:
            The substring with start index = 0 is "cba", which is an anagram of "abc".
            The substring with start index = 6 is "bac", which is an anagram of "abc".

    Example 2:
        Input: s = "abab", p = "ab"
        Output: [0, 1, 2]

Constraints:
    - 1 <= s.length, p.length <= 3 * 10^4
    - s and p consist of lowercase English letters

Approach:
    Use a fixed-size sliding window of length len(p) over s.
    Maintain frequency counts for p (p_count) and the current window (window_count).
    A window is an anagram of p iff window_count == p_count.

    Optimization: track a `matches` counter instead of comparing full dicts each step.
    - matches counts how many of the 26 letters have equal frequency in both counts.
    - When matches == 26, the window is an anagram.
    - On each slide: update counts for the outgoing left char and incoming right char,
      adjusting matches accordingly.

Complexity:
    Time:  O(n) where n = len(s) — each char processed O(1) per step
    Space: O(1) — only 26-letter frequency arrays, constant size

Alternative Approach:
    Sort-based: sort p, then sort each window of length len(p) in s.
    Compare sorted strings. O(n * k log k) time where k = len(p). Much slower.
"""

from typing import List


def findAnagrams(s: str, p: str) -> List[int]:
    if len(p) > len(s):
        return []

    p_count = [0] * 26
    window_count = [0] * 26

    for ch in p:
        p_count[ord(ch) - ord('a')] += 1

    # Initialize the first window
    for ch in s[:len(p)]:
        window_count[ord(ch) - ord('a')] += 1

    # Count matching character frequencies
    matches = sum(1 for i in range(26) if p_count[i] == window_count[i])

    result = []
    if matches == 26:
        result.append(0)

    for right in range(len(p), len(s)):
        left = right - len(p)

        # Add new right character
        r_idx = ord(s[right]) - ord('a')
        if window_count[r_idx] == p_count[r_idx]:
            matches -= 1
        window_count[r_idx] += 1
        if window_count[r_idx] == p_count[r_idx]:
            matches += 1

        # Remove old left character
        l_idx = ord(s[left]) - ord('a')
        if window_count[l_idx] == p_count[l_idx]:
            matches -= 1
        window_count[l_idx] -= 1
        if window_count[l_idx] == p_count[l_idx]:
            matches += 1

        if matches == 26:
            result.append(left + 1)

    return result


if __name__ == "__main__":
    # Basic examples
    assert findAnagrams("cbaebabacd", "abc") == [0, 6]
    assert findAnagrams("abab", "ab") == [0, 1, 2]

    # p longer than s
    assert findAnagrams("ab", "abc") == []

    # No anagrams
    assert findAnagrams("af", "be") == []

    # Entire string is an anagram
    assert findAnagrams("baa", "aab") == [0]

    # Single character match
    assert findAnagrams("aaaaaaa", "a") == [0, 1, 2, 3, 4, 5, 6]

    # s and p same length
    assert findAnagrams("ab", "ba") == [0]

    # Multiple anagrams, non-overlapping pattern
    assert findAnagrams("abcabcabc", "abc") == [0, 1, 2, 3, 4, 5, 6]

    print("All tests passed!")
