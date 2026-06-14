"""
Problem Number: 49
Title: Group Anagrams
Difficulty: Medium
Topics: Array, Hash Table, String, Sorting

Problem Statement:
    Given an array of strings strs, group the anagrams together. You can return
    the answer in any order.

    An Anagram is a word or phrase formed by rearranging the letters of a different
    word or phrase, typically using all the original letters exactly once.

Examples:
    Example 1:
        Input:  strs = ["eat","tea","tan","ate","nat","bat"]
        Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

    Example 2:
        Input:  strs = [""]
        Output: [[""]]

    Example 3:
        Input:  strs = ["a"]
        Output: [["a"]]

Constraints:
    - 1 <= strs.length <= 10^4
    - 0 <= strs[i].length <= 100
    - strs[i] consists of lowercase English letters

Approach:
    Two strings are anagrams if and only if their sorted characters are identical.
    We use a hash map where the key is the sorted version of each word, and the
    value is the list of words that produce that sorted key.

    Walk through each word, sort its characters to form the key, and append the
    original word to the corresponding bucket in the dictionary.

    Alternative: Instead of sorting (O(k log k) per word), use a character
    frequency tuple as the key — a fixed-length tuple of 26 counts. This gives
    O(k) per word and is faster for long strings.

Time Complexity:
    Sorting approach:     O(n * k log k) where n = len(strs), k = max word length
    Frequency approach:   O(n * k)

Space Complexity:
    O(n * k) — storing all words in the hash map
"""

from collections import defaultdict
from typing import List


def groupAnagrams(strs: List[str]) -> List[List[str]]:
    """
    Group anagrams using sorted-string as hash key.

    Args:
        strs: List of strings to group.

    Returns:
        List of groups, each group containing mutually anagrammatic strings.
    """
    groups: dict[str, List[str]] = defaultdict(list)
    for word in strs:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())


# ---------------------------------------------------------------------------
# Alternative Approach: character-frequency tuple as key (O(k) per word)
# ---------------------------------------------------------------------------

def groupAnagrams_freq(strs: List[str]) -> List[List[str]]:
    """
    Group anagrams using a 26-element character frequency tuple as the key.
    Avoids sorting; useful when strings are very long.

    Args:
        strs: List of strings to group.

    Returns:
        List of anagram groups.
    """
    groups: dict[tuple, List[str]] = defaultdict(list)
    for word in strs:
        freq = [0] * 26
        for ch in word:
            freq[ord(ch) - ord('a')] += 1
        groups[tuple(freq)].append(word)
    return list(groups.values())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    def normalize(result: List[List[str]]) -> List[List[str]]:
        """Sort each inner list and the outer list for comparison."""
        return sorted(sorted(group) for group in result)

    # Example 1: standard case
    result = groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    expected = [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    assert normalize(result) == normalize(expected), f"Test 1 failed: {result}"

    # Example 2: single empty string
    result = groupAnagrams([""])
    assert normalize(result) == [[""]], f"Test 2 failed: {result}"

    # Example 3: single character
    result = groupAnagrams(["a"])
    assert normalize(result) == [["a"]], f"Test 3 failed: {result}"

    # Edge: all same anagram group
    result = groupAnagrams(["abc", "bca", "cab"])
    assert normalize(result) == [["abc", "bca", "cab"]], f"Test 4 failed: {result}"

    # Edge: no anagrams, all distinct
    result = groupAnagrams(["abc", "def", "ghi"])
    assert normalize(result) == [["abc"], ["def"], ["ghi"]], f"Test 5 failed: {result}"

    # Edge: multiple groups with same sizes but different chars
    result = groupAnagrams(["ab", "ba", "cd", "dc"])
    assert normalize(result) == [["ab", "ba"], ["cd", "dc"]], f"Test 6 failed: {result}"

    # Frequency-key alternative gives same results
    result_freq = groupAnagrams_freq(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert normalize(result_freq) == normalize(expected), f"Freq Test 1 failed: {result_freq}"

    result_freq = groupAnagrams_freq([""])
    assert normalize(result_freq) == [[""]], f"Freq Test 2 failed: {result_freq}"

    print("All tests passed!")
