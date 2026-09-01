"""
340. Longest Substring with At Most K Distinct Characters
Difficulty: Medium
Topics: Hash Table, String, Sliding Window

PROBLEM STATEMENT
-----------------
Given a string `s` and an integer `k`, return the length of the longest
substring of `s` that contains at most `k` distinct characters.

Example 1:
    Input:  s = "eceba", k = 2
    Output: 3
    Explanation: The substring "ece" has length 3 and 2 distinct characters.

Example 2:
    Input:  s = "aa", k = 1
    Output: 2
    Explanation: The substring "aa" has length 2 and 1 distinct character.

Constraints:
    1 <= s.length <= 5 * 10^4
    0 <= k <= 50


APPROACH — Variable-size sliding window with a hash map of counts (primary)
---------------------------------------------------------------------------
Maintain a window [left, right] and a dictionary `count` mapping each character
in the window to its frequency. Expand the window one character at a time by
moving `right`. Whenever the number of distinct characters (len(count)) exceeds
k, shrink the window from the left: decrement count[s[left]], removing the key
when its count hits zero, and advance `left`. After each expansion the window is
valid (at most k distinct chars), so record its length.

Why it works: every substring corresponds to some [left, right] window. For a
fixed right endpoint, the smallest valid left is monotonic non-decreasing as
right grows (adding characters can only force left to move rightward, never
back). This monotonicity is exactly what lets a single forward pass with two
pointers examine every maximal valid window in O(n) total pointer movement.

Edge case: k == 0 admits no character, so the answer is 0.

Time Complexity:  O(n) — each character is added once and removed at most once;
                  dictionary operations are O(1) average.
Space Complexity: O(k) — the map holds at most k + 1 distinct characters.


ALTERNATIVE — "last seen index" map bounded to size k (ordered-dict flavour)
----------------------------------------------------------------------------
Instead of frequency counts, store the last index at which each character
appeared. When the map exceeds k keys, find the character with the smallest last
index (the leftmost) and jump `left` to just past it, deleting that key. This
trades the shrink loop for an O(k) scan (or O(1) with an OrderedDict). Included
below as `lengthOfLongestSubstringKDistinctLastSeen` for cross-verification.

Time Complexity:  O(n * k) with the plain-dict scan (or O(n) with OrderedDict).
Space Complexity: O(k).
"""

from __future__ import annotations

from collections import OrderedDict, defaultdict


class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        """Sliding window with a frequency map. See APPROACH."""
        if k == 0:
            return 0

        count: dict[str, int] = defaultdict(int)
        left = 0
        best = 0

        for right, ch in enumerate(s):
            count[ch] += 1
            # Shrink until at most k distinct characters remain.
            while len(count) > k:
                left_ch = s[left]
                count[left_ch] -= 1
                if count[left_ch] == 0:
                    del count[left_ch]
                left += 1
            best = max(best, right - left + 1)

        return best

    def lengthOfLongestSubstringKDistinctLastSeen(self, s: str, k: int) -> int:
        """OrderedDict of last-seen indices. See ALTERNATIVE."""
        if k == 0:
            return 0

        last_seen: "OrderedDict[str, int]" = OrderedDict()
        left = 0
        best = 0

        for right, ch in enumerate(s):
            # Refresh recency: move ch to the end of the ordered dict.
            if ch in last_seen:
                del last_seen[ch]
            last_seen[ch] = right

            if len(last_seen) > k:
                # Evict the least-recently-seen character (first item).
                _, oldest_idx = last_seen.popitem(last=False)
                left = oldest_idx + 1

            best = max(best, right - left + 1)

        return best


if __name__ == "__main__":
    sol = Solution()

    def check(s: str, k: int, expected: int) -> None:
        got = sol.lengthOfLongestSubstringKDistinct(s, k)
        got2 = sol.lengthOfLongestSubstringKDistinctLastSeen(s, k)
        assert got == expected, f"window: ({s!r}, {k}) -> {got}, want {expected}"
        assert got2 == expected, f"lastseen: ({s!r}, {k}) -> {got2}, want {expected}"

    # Provided examples.
    check("eceba", 2, 3)
    check("aa", 1, 2)

    # k == 0 -> nothing qualifies.
    check("abc", 0, 0)

    # Empty string.
    check("", 3, 0)

    # k larger than the number of distinct chars -> whole string.
    check("abaccc", 10, 6)

    # Exactly k distinct across the entire string.
    check("aabbcc", 3, 6)

    # Single character repeated.
    check("aaaa", 1, 4)

    # Classic: window slides past a third distinct char.
    check("abcadcacacaca", 3, 11)  # "cadcacacaca" -> {a,c,d}, length 11

    # k = 1 picks the longest single-char run.
    check("abaccccb", 1, 4)  # "cccc"

    # All distinct, k = 2 -> any 2 adjacent.
    check("abcdef", 2, 2)

    # Brute-force cross-check on many small random-ish strings.
    import itertools

    def brute(s: str, k: int) -> int:
        best = 0
        for i in range(len(s)):
            for j in range(i, len(s)):
                if len(set(s[i : j + 1])) <= k:
                    best = max(best, j - i + 1)
        return best

    alphabet = "abcd"
    for length in range(0, 7):
        for combo in itertools.product(alphabet, repeat=length):
            test = "".join(combo)
            for kk in range(0, 4):
                expected = brute(test, kk)
                assert sol.lengthOfLongestSubstringKDistinct(test, kk) == expected, (
                    test,
                    kk,
                )
                assert (
                    sol.lengthOfLongestSubstringKDistinctLastSeen(test, kk) == expected
                ), (test, kk)

    print("All 340. Longest Substring with At Most K Distinct Characters tests passed!")
