"""
3. Longest Substring Without Repeating Characters
Difficulty: Medium
Topics: Hash Table, String, Sliding Window

Problem Statement:
Given a string s, find the length of the longest substring without duplicate characters.

Example 1: s = "abcabcbb" -> 3
Example 2: s = "bbbbb" -> 1
Example 3: s = "pwwkew" -> 3

Approach: Sliding Window with Hash Map — O(n) time, O(min(n,128)) space
Maintain window [left, right]; jump left past duplicate on collision.
"""


def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len


if __name__ == "__main__":
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("au") == 2
    assert length_of_longest_substring("dvdf") == 3
    print("All tests passed!")
