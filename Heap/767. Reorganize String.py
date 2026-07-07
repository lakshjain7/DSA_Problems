"""
767. Reorganize String
Difficulty: Medium
Topics: Hash Table, String, Greedy, Sorting, Heap (Priority Queue), Counting

Problem Statement:
Given a string `s`, rearrange the characters of `s` so that any two adjacent
characters are not the same.

Return any possible rearrangement of `s`, or return "" if not possible.

Examples:
    Input: s = "aab"
    Output: "aba"

    Input: s = "aaab"
    Output: ""

Constraints:
    1 <= s.length <= 500
    s consists of only lowercase English letters.

Approach (Greedy + Max-Heap):
The key insight is that the most frequent character is the bottleneck: if
any character occurs more than ceil(len(s) / 2) times, it is impossible to
separate all its occurrences with other characters, so we should return "".

Otherwise, a greedy strategy works: always place the character that
currently has the highest remaining frequency (as long as it isn't the same
as the character we just placed). Using a max-heap (Python's heapq is a
min-heap, so we push negative counts) lets us efficiently fetch the most
frequent remaining character at each step.

Algorithm:
  1. Count frequency of every character.
  2. Push (-count, char) for every character onto a heap.
  3. Repeatedly pop the most frequent character. If it's different from the
     last character placed, append it to the result, decrement its count,
     and push it back onto the heap if count > 0. If it's the *same* as the
     last placed character, pop the next-most-frequent character instead,
     place that one, then push the first one back for later use.
  4. If at any point we cannot place a character without repeating the
     previous one (heap empty but we still need to place blocked char),
     rearrangement is impossible.

Why it works: greedily using the most frequent remaining character keeps
the counts balanced, minimizing the risk of being forced to place the same
character twice in a row later.

Complexity:
    Time:  O(n log k) where n = len(s), k = number of distinct characters
           (at most 26, so effectively O(n))
    Space: O(k) for the heap and counter, O(n) for the output string

Alternative Approach (Sort + Fill Even/Odd Indices):
Sort characters by frequency descending. Place the most frequent character
into alternating positions of the output (0, 2, 4, ...), wrapping to odd
positions (1, 3, 5, ...) once even positions are exhausted. This achieves
the same guarantee in O(n log n) time without needing a heap, provided the
feasibility check (max frequency <= ceil(n/2)) passes first.
"""

import heapq
from collections import Counter
from typing import List


def reorganize_string(s: str) -> str:
    n = len(s)
    counts = Counter(s)
    max_freq = max(counts.values())
    if max_freq > (n + 1) // 2:
        return ""

    heap = [(-count, char) for char, count in counts.items()]
    heapq.heapify(heap)

    result: List[str] = []
    prev_count, prev_char = 0, ""

    while heap:
        count, char = heapq.heappop(heap)
        result.append(char)
        count += 1  # one fewer occurrence remaining (count is negative)

        if prev_count < 0:
            heapq.heappush(heap, (prev_count, prev_char))

        prev_count, prev_char = count, char

    reorganized = "".join(result)
    return reorganized if len(reorganized) == n else ""


def reorganize_string_sort(s: str) -> str:
    """Alternative approach: sort by frequency, fill even then odd indices."""
    n = len(s)
    counts = Counter(s)
    max_freq = max(counts.values())
    if max_freq > (n + 1) // 2:
        return ""

    sorted_chars = sorted(counts.items(), key=lambda item: -item[1])

    result = [""] * n
    index = 0
    for char, freq in sorted_chars:
        for _ in range(freq):
            if index >= n:
                index = 1
            result[index] = char
            index += 2

    return "".join(result)


def _is_valid_reorganization(original: str, candidate: str) -> bool:
    if candidate == "":
        return False
    if sorted(candidate) != sorted(original):
        return False
    return all(candidate[i] != candidate[i + 1] for i in range(len(candidate) - 1))


if __name__ == "__main__":
    # "aab" -> some valid rearrangement like "aba"
    assert _is_valid_reorganization("aab", reorganize_string("aab"))
    assert _is_valid_reorganization("aab", reorganize_string_sort("aab"))

    # "aaab" -> impossible
    assert reorganize_string("aaab") == ""
    assert reorganize_string_sort("aaab") == ""

    # Single character
    assert reorganize_string("a") == "a"
    assert reorganize_string_sort("a") == "a"

    # All same character, length > 1 -> impossible
    assert reorganize_string("aa") == ""
    assert reorganize_string_sort("aa") == ""

    # Larger valid case
    s = "aaabbbcccdd"
    result = reorganize_string(s)
    assert _is_valid_reorganization(s, result)
    result2 = reorganize_string_sort(s)
    assert _is_valid_reorganization(s, result2)

    # Two distinct characters, equal count
    assert _is_valid_reorganization("abab", reorganize_string("abab"))

    # Exactly at the boundary of feasibility: n=5, max_freq=3 (ceil(5/2)=3)
    s2 = "aaabb"
    result3 = reorganize_string(s2)
    assert _is_valid_reorganization(s2, result3)

    print("All test cases passed!")
