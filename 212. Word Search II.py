"""
Problem 212: Word Search II
Difficulty: Hard
Topics: Array, String, Backtracking, Trie, Matrix

Problem Statement:
    Given an m x n board of characters and a list of strings words, return all words
    in the board. Each word must be built from sequentially adjacent cells (horizontal
    or vertical). The same cell may not be reused within a single word.

Examples:
    board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    words = ["oath","pea","eat","rain"]  =>  Output: ["eat","oath"]

    board = [["a","b"],["c","d"]], words = ["abcb"]  =>  Output: []

Constraints:
    1 <= m, n <= 12; 1 <= words.length <= 3*10^4; 1 <= words[i].length <= 10.
    All chars are lowercase English letters.

Approach (Trie + DFS Backtracking):
    1. Build a Trie from all target words. Each terminal node stores the full word.
    2. DFS from every board cell, walking the Trie in parallel.
       - If the current char is not a child in the Trie, prune immediately.
       - If a node has a stored word, record it and clear (avoids duplicates).
       - Mark board[r][c] = '#' during recursion; restore on backtrack.
    3. Trie pruning: delete childless nodes after use to speed up future searches.

    Why better than brute force: shared Trie prefixes mean one failed character
    prunes ALL words with that prefix simultaneously.

Complexity:
    Build Trie: O(W * L). DFS: O(m * n * 4^L) where L = max word length.
    Space: O(W * L) Trie + O(L) call stack.

Alternative: Run Word Search I (LC 79) for each word independently.
    Works but is O(W * m * n * 4^L) -- much worse when W is large.
"""
from typing import List


class TrieNode:
    __slots__ = ("children", "word")

    def __init__(self) -> None:
        self.children: dict = {}
        self.word: str = ""


def findWords(board: List[List[str]], words: List[str]) -> List[str]:
    """Return every word from words that can be traced on board."""
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = w

    rows, cols = len(board), len(board[0])
    result: List[str] = []

    def dfs(r: int, c: int, node: TrieNode) -> None:
        ch = board[r][c]
        nxt = node.children.get(ch)
        if nxt is None:
            return
        if nxt.word:
            result.append(nxt.word)
            nxt.word = ""
        board[r][c] = "#"
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, nxt)
        board[r][c] = ch
        if not nxt.children:
            del node.children[ch]

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    return result


if __name__ == "__main__":
    b1 = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    assert sorted(findWords(b1, ["oath","pea","eat","rain"])) == ["eat","oath"]

    assert findWords([["a","b"],["c","d"]], ["abcb"]) == []

    assert findWords([["a"]], ["a"]) == ["a"]
    assert findWords([["a"]], ["b"]) == []

    assert findWords([["a","a"]], ["aaa"]) == []

    b5 = [["a","b","c"],["d","e","f"],["g","h","i"]]
    r5 = sorted(findWords(b5, ["abc","adc","ghi","abef","beh","xyz"]))
    assert r5 == sorted(["abc","ghi","abef","beh"]), f"Test 5 failed: {r5}"

    b6 = [["a","b"],["c","d"]]
    r6 = sorted(findWords(b6, ["ab","ac","ba","cd","dc","xy"]))
    assert r6 == ["ab","ac","ba","cd","dc"], f"Test 6 failed: {r6}"

    print("All tests passed for 212. Word Search II!")
