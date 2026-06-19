"""
Problem Number: 424
Title: Longest Repeating Character Replacement
Difficulty: Medium
Topics: String, Sliding Window, Hash Table

Problem Statement:
    Given string s and integer k, you can change any character at most k times.
    Return the length of the longest substring containing the same letter you can get.

Examples:
    "ABAB", k=2 -> 4
    "AABABBA", k=1 -> 4

Approach: Sliding Window — O(n) time, O(1) space
Window is valid when: window_size - max_freq <= k
Keep max_count stable (never shrink it) for O(n) amortized.
"""

from collections import defaultdict


def characterReplacement(s: str, k: int) -> int:
    count: dict[str, int] = defaultdict(int)
    left = 0
    max_count = 0
    result = 0

    for right in range(len(s)):
        count[s[right]] += 1
        max_count = max(max_count, count[s[right]])

        window_size = right - left + 1
        if window_size - max_count > k:
            count[s[left]] -= 1
            left += 1

        result = max(result, right - left + 1)

    return result


if __name__ == "__main__":
    assert characterReplacement("ABAB", 2) == 4
    assert characterReplacement("AABABBA", 1) == 4
    assert characterReplacement("AAAA", 0) == 4
    assert characterReplacement("A", 0) == 1
    assert characterReplacement("ABCD", 4) == 4
    assert characterReplacement("AABABBA", 0) == 2
    assert characterReplacement("BAAAB", 2) == 5
    print("All tests passed for 424. Longest Repeating Character Replacement!")
