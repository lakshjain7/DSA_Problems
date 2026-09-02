"""
126. Word Ladder II
Difficulty: Hard
Topics: Hash Table, String, Backtracking, Breadth-First Search

Problem Statement
-----------------
A transformation sequence from word beginWord to word endWord using a dictionary
wordList is a sequence of words
    beginWord -> s1 -> s2 -> ... -> sk
such that:
  - Every adjacent pair of words differs by a single letter.
  - Every si for 1 <= i <= k is in wordList. Note that beginWord does not need
    to be in wordList.
  - sk == endWord.

Given two words, beginWord and endWord, and a dictionary wordList, return all the
shortest transformation sequences from beginWord to endWord, or an empty list if
no such sequence exists. Each sequence should be returned as a list of the words
[beginWord, s1, s2, ..., sk].

Examples
--------
Example 1:
    Input:  beginWord = "hit", endWord = "cog",
            wordList = ["hot","dot","dog","lot","log","cog"]
    Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]

Example 2:
    Input:  beginWord = "hit", endWord = "cog",
            wordList = ["hot","dot","dog","lot","log"]
    Output: []
    Explanation: endWord "cog" is not in wordList, so no valid sequence exists.

Constraints
-----------
    - 1 <= beginWord.length <= 5
    - endWord.length == beginWord.length
    - 1 <= wordList.length <= 500
    - wordList[i].length == beginWord.length
    - beginWord, endWord, and wordList[i] consist of lowercase English letters.
    - beginWord != endWord
    - All the words in wordList are unique.
    - The sum of all shortest transformation sequences does not exceed 10^5.

Approach (BFS layer-by-layer to build parents, then DFS to reconstruct)
-----------------------------------------------------------------------
We need ALL shortest paths, so a plain BFS that stops at the first hit is not
enough — we must record, for every word reached at its shortest distance, which
predecessor words could reach it on a shortest path.

Two phases:

1. BFS by levels. Maintain a frontier (set of words at the current distance).
   For each word in the frontier, generate every one-letter neighbor that is in
   the dictionary and has NOT been finalized in an earlier level. Record
   parents[neighbor].add(word). Crucially we only remove the words discovered in
   THIS level from the unused dictionary AFTER the whole level is processed, so
   two different parents in the same level can both point to the same child
   (both are shortest). Stop as soon as endWord appears in a level, or when the
   frontier becomes empty (no path).

2. DFS/backtracking from endWord back to beginWord using the parents map,
   building each path in reverse and then reversing it. Because parents only
   contains shortest-path predecessors, every reconstructed path is a shortest
   transformation sequence.

Generating neighbors: for a word of length L over 26 letters, trying every
position and every letter is O(L * 26) string builds per word, each O(L) — good
enough for the given constraints.

Complexity
----------
    Let N = number of words, L = word length.
    Time:  O(N * L * 26) for the BFS neighbor generation, plus O(P) to emit the
           P total path characters during reconstruction.
    Space: O(N * L) for the visited/parents structures (plus output size).
"""

from collections import defaultdict, deque
from typing import Dict, List, Set


class Solution:
    def findLadders(self, beginWord: str, endWord: str,
                    wordList: List[str]) -> List[List[str]]:
        word_set: Set[str] = set(wordList)
        if endWord not in word_set:
            return []

        # parents[child] = set of words that reach `child` on a shortest path.
        parents: Dict[str, Set[str]] = defaultdict(set)

        # Words still available to be discovered (not yet finalized).
        unused: Set[str] = set(word_set)
        unused.discard(beginWord)

        current_level: Set[str] = {beginWord}
        found = False

        while current_level and not found:
            # Words discovered at the next distance during this level.
            next_level: Set[str] = set()

            for word in current_level:
                for i in range(len(word)):
                    prefix, suffix = word[:i], word[i + 1:]
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        if c == word[i]:
                            continue
                        candidate = prefix + c + suffix
                        if candidate in unused:
                            next_level.add(candidate)
                            parents[candidate].add(word)

            # Remove this level's discoveries from `unused` only now, so that
            # multiple words in the same level can share a child.
            for w in next_level:
                unused.discard(w)

            if endWord in next_level:
                found = True

            current_level = next_level

        if not found:
            return []

        # Phase 2: reconstruct all shortest paths via DFS over `parents`.
        results: List[List[str]] = []
        path: List[str] = [endWord]

        def backtrack(word: str) -> None:
            if word == beginWord:
                results.append(path[::-1])
                return
            for parent in parents[word]:
                path.append(parent)
                backtrack(parent)
                path.pop()

        backtrack(endWord)
        return results


def normalize(paths: List[List[str]]):
    """Sort a list of paths so results can be compared order-independently."""
    return sorted(tuple(p) for p in paths)


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    res1 = sol.findLadders(
        "hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]
    )
    assert normalize(res1) == normalize([
        ["hit", "hot", "dot", "dog", "cog"],
        ["hit", "hot", "lot", "log", "cog"],
    ]), res1

    # Example 2: endWord not in list -> no path.
    res2 = sol.findLadders(
        "hit", "cog", ["hot", "dot", "dog", "lot", "log"]
    )
    assert res2 == [], res2

    # Direct one-step transformation.
    res3 = sol.findLadders("a", "c", ["a", "b", "c"])
    assert normalize(res3) == normalize([["a", "c"]]), res3

    # No possible neighbors at all.
    res4 = sol.findLadders("hit", "cog", ["xxx", "yyy"])
    assert res4 == [], res4

    # Multiple distinct shortest paths of length 3.
    res5 = sol.findLadders(
        "red", "tax",
        ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"]
    )
    # Shortest length is 4 words. Verify every returned path is valid & shortest.
    assert res5, "expected at least one path"
    lengths = {len(p) for p in res5}
    assert len(lengths) == 1, lengths  # all shortest -> same length
    for p in res5:
        assert p[0] == "red" and p[-1] == "tax"
        for a, b in zip(p, p[1:]):
            diff = sum(1 for x, y in zip(a, b) if x != y)
            assert diff == 1
        for w in p[1:]:
            assert w in {"ted", "tex", "red", "tax", "tad",
                         "den", "rex", "pee"}

    # endWord equals a reachable word one step away with several routes.
    res6 = sol.findLadders(
        "hot", "dog", ["hot", "dog", "dot"]
    )
    assert normalize(res6) == normalize([["hot", "dot", "dog"]]), res6

    print("All tests passed for 126. Word Ladder II")
