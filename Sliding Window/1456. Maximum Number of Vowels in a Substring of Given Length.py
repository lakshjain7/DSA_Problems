"""
1456. Maximum Number of Vowels in a Substring of Given Length
Difficulty: Medium
Topics: String, Sliding Window

Problem Statement
-----------------
Given a string `s` and an integer `k`, return the maximum number of vowel
letters in any substring of `s` with length `k`.

Vowel letters in English are 'a', 'e', 'i', 'o', and 'u'.

Examples
--------
Example 1:
    Input:  s = "abciiidef", k = 3
    Output: 3
    Explanation: The substring "iii" contains 3 vowel letters.

Example 2:
    Input:  s = "aeiou", k = 2
    Output: 2
    Explanation: Any substring of length 2 contains 2 vowels.

Example 3:
    Input:  s = "leetcode", k = 3
    Output: 2
    Explanation: "lee", "eet" and "ode" contain 2 vowels.

Example 4:
    Input:  s = "rhythms", k = 4
    Output: 0
    Explanation: There are no vowels in s, so the answer is 0.

Example 5:
    Input:  s = "tryhard", k = 4
    Output: 1

Constraints
-----------
    1 <= s.length <= 10^5
    s consists of lowercase English letters.
    1 <= k <= s.length

Approach: Fixed-size Sliding Window
-----------------------------------
A brute-force solution would recount the vowels for every window of length k,
costing O(n * k). Instead we keep a running count of vowels inside a window of
fixed width k and slide it one character at a time.

    1. Count the vowels in the first window s[0:k]; this is the initial answer.
    2. Slide the window right by one: the character entering the window is s[i]
       and the character leaving is s[i - k]. Adjust the count by +1 if the
       entering char is a vowel and -1 if the leaving char is a vowel.
    3. Track the running maximum. An early exit is possible once the count
       reaches k (a window can never hold more than k vowels).

Because each character enters and leaves the window at most once, the count is
maintained in O(1) per step.

Complexity
----------
Time:  O(n)  -- single pass over the string.
Space: O(1)  -- only counters and a constant-size vowel set.
"""

from typing import Set


VOWELS: Set[str] = {"a", "e", "i", "o", "u"}


def max_vowels(s: str, k: int) -> int:
    """Return the max number of vowels in any length-k substring of s."""
    count = sum(1 for ch in s[:k] if ch in VOWELS)
    best = count
    for i in range(k, len(s)):
        if s[i] in VOWELS:
            count += 1
        if s[i - k] in VOWELS:
            count -= 1
        if count > best:
            best = count
            if best == k:  # cannot do better than k vowels in a window
                break
    return best


def max_vowels_brute(s: str, k: int) -> int:
    """O(n*k) reference implementation used to cross-check the fast version."""
    best = 0
    for i in range(len(s) - k + 1):
        best = max(best, sum(1 for ch in s[i:i + k] if ch in VOWELS))
    return best


if __name__ == "__main__":
    # Provided examples
    assert max_vowels("abciiidef", 3) == 3
    assert max_vowels("aeiou", 2) == 2
    assert max_vowels("leetcode", 3) == 2
    assert max_vowels("rhythms", 4) == 0
    assert max_vowels("tryhard", 4) == 1

    # Edge cases
    assert max_vowels("a", 1) == 1               # single vowel
    assert max_vowels("b", 1) == 0               # single consonant
    assert max_vowels("aeiou", 5) == 5           # whole string is the window
    assert max_vowels("bbbbb", 3) == 0           # no vowels at all
    assert max_vowels("uuuuu", 3) == 3           # all vowels, window < len

    # Randomised cross-check against the brute-force reference
    import random
    letters = "abcdefghijklmnopqrstuvwxyz"
    for _ in range(500):
        n = random.randint(1, 40)
        s = "".join(random.choice(letters) for _ in range(n))
        k = random.randint(1, n)
        assert max_vowels(s, k) == max_vowels_brute(s, k), (s, k)

    print("All tests passed for 1456. Maximum Number of Vowels in a Substring of Given Length")
