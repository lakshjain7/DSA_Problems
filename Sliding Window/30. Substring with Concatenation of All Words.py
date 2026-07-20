"""
30. Substring with Concatenation of All Words
Difficulty: Hard
Topics: Hash Table, String, Sliding Window

Problem Statement
-----------------
You are given a string `s` and an array of strings `words`. All the strings
in `words` are of the same length.

A concatenated substring in `s` is a substring that contains all the strings
of any permutation of `words` concatenated together.

    - For example, if words = ["ab", "cd", "ef"], then "abcdef", "abefcd",
      "cdabef", "cdefab", "efabcd", and "efcdab" are all concatenated
      substrings. "acdbef" is not because it is not the concatenation of any
      permutation of words.

Return the starting indices of all the concatenated substrings in `s`. You
can return the answer in any order.

Examples
--------
Example 1:
    Input:  s = "barfoothefoobarman", words = ["foo", "bar"]
    Output: [0, 9]
    Explanation: The substring starting at 0 is "barfoo" (bar + foo);
                 the substring starting at 9 is "foobar" (foo + bar).

Example 2:
    Input:  s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]
    Output: []
    Explanation: There is no concatenated substring.

Example 3:
    Input:  s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]
    Output: [6, 9, 12]

Constraints
-----------
    1 <= s.length <= 10^4
    1 <= words.length <= 5000
    1 <= words[i].length <= 30
    s and words[i] consist of lowercase English letters.

Approach (Sliding Window over word boundaries)
----------------------------------------------
Let:
    k = len(words)          number of words
    w = len(words[0])       length of each word (all equal)
    total = k * w           length of every concatenated substring

Because every word has the same length w, any valid concatenation is aligned
to one of w possible offsets (0, 1, ..., w-1) relative to the start of s.
For each offset we run a sliding window that moves w characters at a time, so
each window boundary lands exactly on a word boundary.

For a fixed offset:
    - `need` is a Counter of the required word frequencies.
    - `window` is a Counter of words currently inside the window.
    - `count` is how many complete words are currently in the window.
    - `left` marks the start of the current window (a multiple of w from
      the offset).

We advance `right` in steps of w, extracting the next word:
    - If the word is one of the required words, add it to the window and
      increment count. While its frequency exceeds what is needed, shrink
      the window from the left (removing whole words) until the excess is
      gone.
    - If the word is NOT required at all, the whole window is invalid: reset
      the window Counter and count, and move `left` past this word.
    - Whenever `count == k`, the window holds exactly all words -> record
      `left` as a starting index, then slide `left` forward by one word so we
      can look for the next match.

Why it works: aligning windows to the w offsets guarantees we never split a
word. Within each offset the window expands and contracts by whole words,
maintaining the invariant that `window`/`count` exactly describe the words in
[left, right). A window of exactly k words that never over-counts any word is
precisely a permutation of `words`.

Complexity
----------
Let n = len(s). There are w offsets, and across all offsets the window
pointers together traverse O(n / w) word positions, each doing O(w) work to
slice a word. This yields:

Time:  O(n * w) in the worst case (often summarized as O(n * w) or
       O(w * (n / w)) amortized word moves times O(w) slicing).
Space: O(k * w) for the Counters holding up to k distinct words.
"""

from collections import Counter
from typing import List


def find_substring(s: str, words: List[str]) -> List[int]:
    """Return start indices of substrings that are a concatenation of words."""
    if not s or not words:
        return []

    w = len(words[0])
    k = len(words)
    total = w * k
    n = len(s)
    if total > n:
        return []

    need = Counter(words)
    result: List[int] = []

    for offset in range(w):
        left = offset
        count = 0
        window: Counter = Counter()

        for right in range(offset, n - w + 1, w):
            word = s[right:right + w]

            if word in need:
                window[word] += 1
                count += 1

                # Too many copies of `word`: shrink from the left until valid.
                while window[word] > need[word]:
                    left_word = s[left:left + w]
                    window[left_word] -= 1
                    left += w
                    count -= 1

                if count == k:
                    result.append(left)
                    # Slide left by one word to search for the next window.
                    left_word = s[left:left + w]
                    window[left_word] -= 1
                    left += w
                    count -= 1
            else:
                # `word` is not needed at all; discard the whole window.
                window.clear()
                count = 0
                left = right + w

    return result


if __name__ == "__main__":
    # Example 1
    assert sorted(find_substring("barfoothefoobarman", ["foo", "bar"])) == [0, 9]

    # Example 2
    assert find_substring(
        "wordgoodgoodgoodbestword",
        ["word", "good", "best", "word"],
    ) == []

    # Example 3
    assert sorted(
        find_substring("barfoofoobarthefoobarman", ["bar", "foo", "the"])
    ) == [6, 9, 12]

    # Duplicate words must be matched with correct multiplicity
    assert sorted(
        find_substring("wordgoodgoodgoodbestword", ["word", "good", "best", "good"])
    ) == [8]

    # Single word repeated
    assert sorted(find_substring("aaaaaa", ["aa", "aa"])) == [0, 1, 2]

    # Whole string is the concatenation
    assert find_substring("foobar", ["foo", "bar"]) == [0]

    # No match
    assert find_substring("abcdef", ["gh"]) == []

    # words longer than s
    assert find_substring("ab", ["abc", "def"]) == []

    # Single one-character words
    assert sorted(find_substring("ab", ["a", "b"])) == [0]
    assert sorted(find_substring("aba", ["a", "a"])) == []  # only one 'a' pairable each window

    # Overlapping matches at multiple offsets
    assert sorted(find_substring("lingmindraboofooowingdingbarrwingmonkeypoundcake",
                                 ["fooo", "barr", "wing", "ding", "wing"])) == [13]

    # Brute-force cross validation
    import random

    def brute(s: str, words: List[str]) -> List[int]:
        w = len(words[0])
        total = w * len(words)
        need = Counter(words)
        res = []
        for i in range(len(s) - total + 1):
            seen = Counter(s[j:j + w] for j in range(i, i + total, w))
            if seen == need:
                res.append(i)
        return res

    alphabet = "ab"
    for _ in range(500):
        w = random.randint(1, 3)
        k = random.randint(1, 3)
        words_r = ["".join(random.choice(alphabet) for _ in range(w)) for _ in range(k)]
        s_len = random.randint(1, 12)
        s_r = "".join(random.choice(alphabet) for _ in range(s_len))
        assert sorted(find_substring(s_r, words_r)) == brute(s_r, words_r), (
            s_r, words_r,
        )

    print("All tests passed for 30. Substring with Concatenation of All Words")
