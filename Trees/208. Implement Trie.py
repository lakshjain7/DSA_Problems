"""
Problem: 208. Implement Trie (Prefix Tree)
Difficulty: Medium
Topics: Trie, Design, Hash Map

Problem Statement:
    A trie (pronounced "try") or prefix tree is a tree data structure used to
    efficiently store and retrieve keys in a dataset of strings.
    Implement the Trie class:
        - Trie()          Initializes the trie object.
        - insert(word)    Inserts string word into the trie.
        - search(word)    Returns true if word is in the trie (not just a prefix).
        - startsWith(prefix) Returns true if any previously inserted word has prefix.

Examples:
    trie = Trie()
    trie.insert("apple")
    trie.search("apple")    # True
    trie.search("app")      # False
    trie.startsWith("app")  # True
    trie.insert("app")
    trie.search("app")      # True

Constraints:
    - 1 <= word.length, prefix.length <= 2000
    - word and prefix consist only of lowercase English letters
    - At most 3 * 10^4 calls total to insert, search, startsWith

Approach:
    Each TrieNode holds:
      - children: dict mapping char -> TrieNode
      - is_end: bool marking whether a complete word ends here

    insert: walk/create nodes char by char, mark is_end=True at last node.
    search: walk nodes; if any char missing return False; check is_end.
    startsWith: walk nodes; if any char missing return False; return True.

    All three ops are O(m) where m is word/prefix length.

Complexity:
    Time:  O(m) per operation, m = length of word/prefix
    Space: O(n * m) total for n words of average length m

Alternative Approach:
    Use a dict-of-dicts (nested defaultdict) instead of explicit TrieNode class.
    Same complexity, slightly less readable.
"""


class TrieNode:
    def __init__(self):
        self.children: dict = {}
        self.is_end: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


# Alternative: nested dict implementation
class TrieDict:
    def __init__(self):
        self.root = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node['#'] = True  # end marker

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return '#' in node

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True


if __name__ == "__main__":
    # Test TrieNode-based implementation
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") == True
    assert trie.search("app") == False
    assert trie.startsWith("app") == True
    trie.insert("app")
    assert trie.search("app") == True

    # More edge cases
    trie2 = Trie()
    trie2.insert("a")
    assert trie2.search("a") == True
    assert trie2.search("ab") == False
    assert trie2.startsWith("a") == True
    assert trie2.startsWith("b") == False

    trie3 = Trie()
    trie3.insert("hello")
    trie3.insert("help")
    trie3.insert("world")
    assert trie3.search("hello") == True
    assert trie3.search("hell") == False
    assert trie3.startsWith("hel") == True
    assert trie3.startsWith("wor") == True
    assert trie3.startsWith("xyz") == False
    assert trie3.search("world") == True

    # Test dict-based alternative
    td = TrieDict()
    td.insert("apple")
    assert td.search("apple") == True
    assert td.search("app") == False
    assert td.startsWith("app") == True
    td.insert("app")
    assert td.search("app") == True

    print("All tests passed!")
