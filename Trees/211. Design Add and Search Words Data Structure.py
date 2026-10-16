"""
Problem 211: Design Add and Search Words Data Structure
Difficulty: Medium
Topics: String, Depth-First Search, Design, Trie

Design a data structure that supports adding new words and finding if a string
matches any previously added string.

Implement the WordDictionary class:
- WordDictionary() Initializes the object.
- void addWord(word) Adds word to the data structure.
- bool search(word) Returns true if there is any string in the data structure
  that matches word, or false otherwise. word may contain dots '.' where dots
  can be matched with any letter.

Example:
    addWord("bad"); addWord("dad"); addWord("mad")
    search("pad") -> False
    search("bad") -> True
    search(".ad") -> True
    search("b..") -> True

Constraints:
- 1 <= word.length <= 25
- word in addWord consists of lowercase English letters.
- word in search consists of '.' or lowercase English letters.
- At most 2 dots in any search query.
- At most 10^4 calls to addWord and search.

Approach:
    Store words in a trie. addWord walks/creates nodes. search does DFS: for a
    normal letter follow that child; for '.' try every child. Because at most
    two dots appear, branching is bounded (26^2 worst case at those levels).

Complexity:
    addWord: O(L) time, O(L) extra space.
    search:  O(L) without dots; O(26^d * L) with d dots (d <= 2).
    Space overall: O(total characters stored).

Alternative: bucket words by length in a hash map and compare each candidate
    char by char -- simpler, but O(N*L) per search.
"""
from collections import defaultdict
from typing import Dict, List


class WordDictionary:
    def __init__(self) -> None:
        self.root: Dict = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        def dfs(i: int, node: Dict) -> bool:
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":
                return any(dfs(i + 1, child) for k, child in node.items() if k != "$")
            return ch in node and dfs(i + 1, node[ch])

        return dfs(0, self.root)


class WordDictionaryBuckets:
    """Alternative: group words by length and match with wildcard compare."""

    def __init__(self) -> None:
        self.by_len: Dict[int, List[str]] = defaultdict(list)

    def addWord(self, word: str) -> None:
        self.by_len[len(word)].append(word)

    def search(self, word: str) -> bool:
        return any(
            all(p == "." or p == c for p, c in zip(word, w))
            for w in self.by_len.get(len(word), [])
        )


if __name__ == "__main__":
    for cls in (WordDictionary, WordDictionaryBuckets):
        d = cls()
        for w in ("bad", "dad", "mad"):
            d.addWord(w)
        assert d.search("pad") is False
        assert d.search("bad") is True
        assert d.search(".ad") is True
        assert d.search("b..") is True
        assert d.search("b.") is False          # length mismatch
        assert d.search("....") is False
        assert d.search("...") is True
        d.addWord("a")
        assert d.search("a") and d.search(".") and not d.search("..a")
        e = cls()
        assert e.search("a") is False           # empty structure
        e.addWord("abc")
        assert e.search("ab") is False          # prefix is not a word
    print("All tests passed.")
