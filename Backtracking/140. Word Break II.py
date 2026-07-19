"""
140. Word Break II
Difficulty: Hard
Topics: Hash Table, String, Dynamic Programming, Backtracking, Trie, Memoization

Problem Statement
-----------------
Given a string s and a dictionary of strings wordDict, add spaces in s to
construct a sentence where each word is a valid dictionary word. Return all such
possible sentences in any order.

Note that the same word in the dictionary may be reused multiple times in the
segmentation.

Example 1:
    Input: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
    Output: ["cats and dog","cat sand dog"]

Example 2:
    Input: s = "pineapplepenapple",
           wordDict = ["apple","pen","applepen","pine","pineapple"]
    Output: ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
    Explanation: Note that you are allowed to reuse a dictionary word.

Example 3:
    Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
    Output: []

Constraints:
    - 1 <= s.length <= 20
    - 1 <= wordDict.length <= 1000
    - 1 <= wordDict[i].length <= 10
    - s and wordDict[i] consist of only lowercase English letters.
    - All the strings of wordDict are unique.
    - Input is generated in a way that the length of the answer doesn't exceed 10^5.


Approach: Backtracking with Memoization (DFS over suffixes)
-----------------------------------------------------------
Define solve(start) = the list of all sentences (as lists of words) that can be
formed from the suffix s[start:]. We try every dictionary word that matches at
position `start`; for each match we recurse on the remainder and prepend the word
to every sentence returned.

    solve(start):
        if start == len(s): return [[]]   # one empty sentence: the empty suffix
        results = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in wordSet:
                for tail in solve(end):
                    results.append([word] + tail)
        return results

Without memoization this is exponential: the same suffix can be reached along many
different prefix segmentations and would be recomputed each time. We cache
solve(start) keyed by the start index. Because at most len(s)+1 distinct start
positions exist, each is computed once and reused.

A first-class optimization: run the classic Word Break I feasibility DP first
(can the whole string be segmented at all?). If not, we return [] immediately and
avoid building any partial results -- this prevents pathological blow-up on inputs
like "aaa...ab" with dict ["a","aa",...] where many partial segmentations exist but
no full one does.

Why it works: solve(start) enumerates, without duplication, every way to break the
suffix, because each recursive branch commits to a specific first word and the
recursion covers all remaining breaks. Memoization preserves correctness because
the set of segmentations of a suffix depends only on the start index, not on how we
reached it.

Complexity Analysis
-------------------
Let n = len(s). There are O(n) distinct subproblems; each scans O(n) candidate end
positions and does O(n) work per substring slice/compare.
- Time:  O(n^2) to populate the memo for structure, but the true cost is dominated
  by the total number of output sentences: if there are R sentences of length up to
  n, assembling them costs O(n * R). This is unavoidable since we must emit them.
- Space: O(n) recursion depth plus the memo, plus O(n * R) for the produced output.
"""

from typing import Dict, List


def word_break(s: str, wordDict: List[str]) -> List[str]:
    """Return all sentences formed by segmenting s into dictionary words."""
    word_set = set(wordDict)
    n = len(s)

    # --- Feasibility pre-check (Word Break I) to prune hopeless inputs. ---
    # breakable[i] == True means s[i:] can be fully segmented.
    breakable = [False] * (n + 1)
    breakable[n] = True
    for start in range(n - 1, -1, -1):
        for end in range(start + 1, n + 1):
            if s[start:end] in word_set and breakable[end]:
                breakable[start] = True
                break
    if not breakable[0]:
        return []

    memo: Dict[int, List[List[str]]] = {}

    def solve(start: int) -> List[List[str]]:
        if start == n:
            return [[]]  # exactly one segmentation of the empty suffix
        if start in memo:
            return memo[start]

        results: List[List[str]] = []
        for end in range(start + 1, n + 1):
            word = s[start:end]
            # Only recurse when the remainder is also breakable (extra pruning).
            if word in word_set and breakable[end]:
                for tail in solve(end):
                    results.append([word] + tail)

        memo[start] = results
        return results

    return [" ".join(words) for words in solve(0)]


if __name__ == "__main__":
    def normalize(sentences: List[str]) -> set:
        return set(sentences)

    # Example 1
    out = word_break("catsanddog", ["cat", "cats", "and", "sand", "dog"])
    assert normalize(out) == {"cats and dog", "cat sand dog"}, out

    # Example 2
    out = word_break("pineapplepenapple",
                     ["apple", "pen", "applepen", "pine", "pineapple"])
    assert normalize(out) == {
        "pine apple pen apple",
        "pineapple pen apple",
        "pine applepen apple",
    }, out

    # Example 3: not segmentable -> empty list
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) == []

    # Single word equals the whole string
    assert word_break("apple", ["apple"]) == ["apple"]

    # Word reuse: "aaa" with dict {"a", "aa"}
    out = word_break("aaa", ["a", "aa"])
    assert normalize(out) == {"a a a", "a aa", "aa a"}, out

    # No dictionary word matches at all
    assert word_break("abc", ["x", "y", "z"]) == []

    # Pathological pruning case: many partial breaks, no full break.
    # Should return quickly with [] thanks to the feasibility pre-check.
    assert word_break("aaaaaaaaaaaaaaaaaaab",
                      ["a", "aa", "aaa", "aaaa"]) == []

    # A string where the entire string is also a dictionary word plus splits.
    out = word_break("abcd", ["a", "abc", "b", "cd", "abcd"])
    assert normalize(out) == {"a b cd", "abcd"}, out

    print("All tests passed for 140. Word Break II")
