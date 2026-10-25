"""
214. Shortest Palindrome
Difficulty: Hard
Topics: String, Rolling Hash, String Matching, Hash Function

You are given a string s. You can convert s to a palindrome by adding
characters in front of it. Return the shortest palindrome you can find by
performing this transformation.

Example 1:
    Input: s = "aacecaaa"
    Output: "aaacecaaa"
Example 2:
    Input: s = "abcd"
    Output: "dcbabcd"

Constraints:
    0 <= s.length <= 5 * 10^4
    s consists of lowercase English letters only.

Approach (KMP prefix function):
    We need the longest palindromic prefix of s; the remaining suffix,
    reversed, is prepended. Build t = s + "#" + reverse(s) and compute the KMP
    failure function. The last value is the length of the longest prefix of s
    that equals a suffix of reverse(s), i.e. the longest palindromic prefix.
    The separator prevents overlap beyond len(s).

Complexity: Time O(n), Space O(n).
"""


def shortest_palindrome(s: str) -> str:
    if not s:
        return s
    t = s + "#" + s[::-1]
    fail = [0] * len(t)
    for i in range(1, len(t)):
        j = fail[i - 1]
        while j and t[i] != t[j]:
            j = fail[j - 1]
        if t[i] == t[j]:
            j += 1
        fail[i] = j
    return s[fail[-1]:][::-1] + s


def shortest_palindrome_two_pointer(s: str) -> str:
    """Alternative: O(n^2) worst case; shrink end until prefix is palindrome."""
    for end in range(len(s), 0, -1):
        p = s[:end]
        if p == p[::-1]:
            return s[end:][::-1] + s
    return s


if __name__ == "__main__":
    cases = [("aacecaaa", "aaacecaaa"), ("abcd", "dcbabcd"), ("", ""),
             ("a", "a"), ("aa", "aa"), ("ab", "bab"), ("aba", "aba"),
             ("abb", "bbabb"), ("aaaa", "aaaa"), ("abac", "cabac")]
    for s, exp in cases:
        assert shortest_palindrome(s) == exp, (s, shortest_palindrome(s), exp)
        assert shortest_palindrome_two_pointer(s) == exp, s
    print("All tests passed.")
