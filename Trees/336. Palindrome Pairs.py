"""
336. Palindrome Pairs
Difficulty: Hard
Topics: Array, Hash Table, String, Trie

Problem:
You are given a 0-indexed array of unique strings words. A palindrome pair is
a pair of indices (i, j) such that 0 <= i, j < words.length, i != j, and
words[i] + words[j] is a palindrome. Return all palindrome pairs.

Example 1:
    Input: words = ["abcd","dcba","lls","s","sssll"]
    Output: [[0,1],[1,0],[3,2],[2,4]]
Example 2:
    Input: words = ["bat","tab","cat"]
    Output: [[0,1],[1,0]]
Example 3:
    Input: words = ["a",""]
    Output: [[0,1],[1,0]]

Constraints:
    1 <= words.length <= 5000
    0 <= words[i].length <= 300
    words[i] consists of lowercase English letters.

Approach:
Map each word to its index. For each word w and each split w = left + right:
  - if left is a palindrome, then reverse(right) + w is a palindrome, so a
    word equal to reverse(right) (with a different index) pairs as (that, w).
  - if right is a palindrome, then w + reverse(left) is a palindrome, so a
    word equal to reverse(left) pairs as (w, that).
Splits include the empty prefix/suffix, which handles the "" word and exact
reverses. To avoid duplicates, the right-palindrome case skips an empty right
side (it was already covered by the left-palindrome case with empty left).

Complexity: Time O(n * L^2), Space O(n * L).
"""
from typing import List


def palindromePairs(words: List[str]) -> List[List[int]]:
    idx = {w: i for i, w in enumerate(words)}
    res = []
    for i, w in enumerate(words):
        for cut in range(len(w) + 1):
            left, right = w[:cut], w[cut:]
            if left == left[::-1]:
                j = idx.get(right[::-1])
                if j is not None and j != i:
                    res.append([j, i])
            if right and right == right[::-1]:
                j = idx.get(left[::-1])
                if j is not None and j != i:
                    res.append([i, j])
    return res


def palindromePairsTrie(words: List[str]) -> List[List[int]]:
    """Alternative: trie of reversed words; same O(n * L^2) worst case."""
    def is_pal(s, lo, hi):
        while lo < hi:
            if s[lo] != s[hi]:
                return False
            lo += 1
            hi -= 1
        return True

    root = {"ch": {}, "end": -1, "pal": []}
    for i, w in enumerate(words):
        node = root
        for k in range(len(w) - 1, -1, -1):
            if is_pal(w, 0, k):
                node["pal"].append(i)
            node = node["ch"].setdefault(w[k], {"ch": {}, "end": -1, "pal": []})
        node["end"] = i
        node["pal"].append(i)

    res = []
    for i, w in enumerate(words):
        node = root
        ok = True
        for k, c in enumerate(w):
            if node["end"] >= 0 and node["end"] != i and is_pal(w, k, len(w) - 1):
                res.append([i, node["end"]])
            node = node["ch"].get(c)
            if node is None:
                ok = False
                break
        if ok:
            for j in node["pal"]:
                if j != i:
                    res.append([i, j])
    return res


def _brute(words):
    out = []
    for i in range(len(words)):
        for j in range(len(words)):
            if i != j:
                s = words[i] + words[j]
                if s == s[::-1]:
                    out.append([i, j])
    return out


if __name__ == "__main__":
    import random
    for f in (palindromePairs, palindromePairsTrie):
        assert sorted(f(["abcd", "dcba", "lls", "s", "sssll"])) == sorted([[0, 1], [1, 0], [3, 2], [2, 4]])
        assert sorted(f(["bat", "tab", "cat"])) == [[0, 1], [1, 0]]
        assert sorted(f(["a", ""])) == [[0, 1], [1, 0]]
        assert f(["abc"]) == []
        for _ in range(300):
            n = random.randint(1, 8)
            ws = list({"".join(random.choice("ab") for _ in range(random.randint(0, 4))) for _ in range(n)})
            assert sorted(f(ws)) == sorted(_brute(ws)), ws
    print("All tests passed")
