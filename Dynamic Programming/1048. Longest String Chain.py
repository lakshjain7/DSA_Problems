"""
1048. Longest String Chain
Difficulty: Medium
Topics: Array, Hash Table, Two Pointers, String, Dynamic Programming

Problem:
You are given an array of words where each word consists of lowercase English
letters. wordA is a predecessor of wordB if and only if we can insert exactly
one letter anywhere in wordA without changing the order of the other characters
to make it equal to wordB.

A word chain is a sequence of words [word1, word2, ..., wordk] with k >= 1,
where word1 is a predecessor of word2, word2 is a predecessor of word3, etc.
A single word is trivially a word chain with k == 1.
Return the length of the longest possible word chain with words chosen from the
given list of words.

Example 1:
    Input: words = ["a","b","ba","bca","bda","bdca"]
    Output: 4   ("a" -> "ba" -> "bda" -> "bdca")
Example 2:
    Input: words = ["xbc","pcxbcf","xb","cxbc","pcxbc"]
    Output: 5
Example 3:
    Input: words = ["abcd","dbqca"]
    Output: 1

Constraints:
    1 <= words.length <= 1000
    1 <= words[i].length <= 16
    words[i] only consists of lowercase English letters.

Approach (DP over sorted lengths + hash map):
    Sort words by length. dp[w] = longest chain ending at w. For each word,
    try deleting each character to get every possible predecessor p; if p is in
    dp, dp[w] = max(dp[w], dp[p] + 1). Processing by increasing length
    guarantees predecessors are computed first.

Complexity:
    Time:  O(N * L^2)  (L deletions, each building an O(L) string)
    Space: O(N * L)
"""
from functools import lru_cache
from typing import Dict, List


def longestStrChain(words: List[str]) -> int:
    dp: Dict[str, int] = {}
    best = 1
    for w in sorted(words, key=len):
        cur = 1
        for i in range(len(w)):
            p = w[:i] + w[i + 1:]
            if p in dp:
                cur = max(cur, dp[p] + 1)
        dp[w] = cur
        best = max(best, cur)
    return best


# Alternative approach: top-down memoization over the word set.
def longestStrChainMemo(words: List[str]) -> int:
    ws = set(words)

    @lru_cache(maxsize=None)
    def go(w: str) -> int:
        res = 1
        for i in range(len(w)):
            p = w[:i] + w[i + 1:]
            if p in ws:
                res = max(res, 1 + go(p))
        return res

    return max(go(w) for w in ws)


if __name__ == "__main__":
    for f in (longestStrChain, longestStrChainMemo):
        assert f(["a", "b", "ba", "bca", "bda", "bdca"]) == 4
        assert f(["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"]) == 5
        assert f(["abcd", "dbqca"]) == 1
        assert f(["a"]) == 1
        assert f(["a", "a"]) == 1  # duplicates do not chain
        assert f(["a", "ab", "abc", "abcd", "abcde"]) == 5
        assert f(["ksqvsyq", "ks", "kss", "czvh", "zczpzvdhx", "zczpzvh",
                  "zczpzvhx", "zcpzvh", "zczvh", "gr", "grukmj", "ksqvsq",
                  "gruj", "kssq", "ksqsq", "grukkmj", "grukj", "zczpzfvdhx",
                  "gru"]) == 7
    print("All tests passed.")
