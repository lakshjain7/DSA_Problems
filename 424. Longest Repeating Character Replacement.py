"""
Problem Number: 424
Title: Longest Repeating Character Replacement
Difficulty: Medium
Topics: String, Sliding Window, Hash Table

Problem Statement:
    You are given a string s and an integer k. You can choose any character of the
    string and change it to any other uppercase English character. You can perform
    this operation at most k times.

    Return the length of the longest substring containing the same letter you can get
    after performing the above operations.

Examples:
    Example 1:
        Input: s = "ABAB", k = 2
        Output: 4
        Explanation: Replace the two 'A's with two 'B's or vice versa.

    Example 2:
        Input: s = "AABABBA", k = 1
        Output: 4
        Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
        The answer is 4.

Constraints:
    - 1 <= s.length <= 10^5
    - s consists of only uppercase English letters.
    - 0 <= k <= s.length

Approach (Sliding Window):
    Maintain a window [left, right]. Track the frequency of each character in the
    window using a count map. The key insight is:
        window_size - max_freq <= k
    means we can make the entire window one character by replacing at most k chars.

    When the condition is violated, shrink from the left.

    Crucially, we never shrink max_freq below its highest seen value (we only
    decrement the left char's count but keep max_count stable). This is safe because
    a smaller max_count would only produce a smaller or equal window — we already
    recorded that maximum, so no need to shrink aggressively. This makes the window
    monotonically non-decreasing in size, which means we only advance left by 1 each
    time, giving O(n) overall.

Complexity:
    Time:  O(n) — each character is processed at most twice (added and removed once)
    Space: O(1) — count array of at most 26 uppercase letters

Alternative Approach (same complexity, explicit shrink):
    Instead of keeping max_count stable, recalculate max over the window each time
    we shrink. This is correct but has a hidden O(26) factor per shrink, still O(n)
    overall but with a larger constant. The stable-max trick is cleaner.
"""

from collections import defaultdict


def characterReplacement(s: str, k: int) -> int:
    """
    Return the length of the longest valid window after at most k replacements.

    Args:
        s: Uppercase English string.
        k: Maximum number of character replacements allowed.

    Returns:
        Length of the longest substring that can be made uniform with <= k changes.
    """
    count: dict[str, int] = defaultdict(int)
    left = 0
    max_count = 0  # highest frequency of any single char seen in any window
    result = 0

    for right in range(len(s)):
        count[s[right]] += 1
        max_count = max(max_count, count[s[right]])

        # Window size minus the dominant character count = replacements needed
        window_size = right - left + 1
        if window_size - max_count > k:
            # Shrink window from the left
            count[s[left]] -= 1
            left += 1
            # Note: max_count is NOT updated here intentionally.
            # The window size stays the same (we moved both pointers),
            # so we can only improve by expanding right.

        result = max(result, right - left + 1)

    return result


# ---------------------------------------------------------------------------
# Alternative: explicit max recalculation on shrink (cleaner logic, same O(n))
# ---------------------------------------------------------------------------

def characterReplacement_v2(s: str, k: int) -> int:
    """Same problem solved by explicitly recalculating max_count after shrinking."""
    count: dict[str, int] = defaultdict(int)
    left = 0
    result = 0

    for right in range(len(s)):
        count[s[right]] += 1

        while (right - left + 1) - max(count.values()) > k:
            count[s[left]] -= 1
            left += 1

        result = max(result, right - left + 1)

    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Basic examples from the problem
    assert characterReplacement("ABAB", 2) == 4, "Expected 4"
    assert characterReplacement("AABABBA", 1) == 4, "Expected 4"

    # All same characters — no replacements needed
    assert characterReplacement("AAAA", 0) == 4, "Expected 4"
    assert characterReplacement("AAAA", 2) == 4, "Expected 4"

    # Single character string
    assert characterReplacement("A", 0) == 1, "Expected 1"
    assert characterReplacement("A", 5) == 1, "Expected 1"

    # k covers whole string
    assert characterReplacement("ABCD", 4) == 4, "Expected 4"
    assert characterReplacement("ABCD", 3) == 4, "Expected 4"

    # k = 0 — longest run of same char
    assert characterReplacement("AABABBA", 0) == 2, "Expected 2"
    assert characterReplacement("ABBB", 0) == 3, "Expected 3"

    # Longer mixed string
    assert characterReplacement("BAAAB", 2) == 5, "Expected 5"

    # Validate v2 matches on all cases
    test_cases = [
        ("ABAB", 2), ("AABABBA", 1), ("AAAA", 0), ("A", 0),
        ("ABCD", 4), ("AABABBA", 0), ("BAAAB", 2),
    ]
    for s, k in test_cases:
        assert characterReplacement(s, k) == characterReplacement_v2(s, k), \
            f"Mismatch on ({s!r}, {k})"

    print("All tests passed for 424. Longest Repeating Character Replacement!")
