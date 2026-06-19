"""
Problem 212: Word Search II
Difficulty: Hard
Topics: Array, String, Backtracking, Trie, Matrix

Given an m x n board and a list of words, return all words found on the board.
Each word must be built from sequentially adjacent cells; same cell not reusable.

Approach (Trie + DFS Backtracking):
  1. Build Trie from all target words.
  2. DFS from every cell, walking the Trie in parallel.
  3. Prune: delete childless nodes after finding a word.

Complexity: Build Trie O(W*L); DFS O(m*n*4^L).
"""
from typing import List


class TrieNode:
    __slots__ = ("children", "word")
    def __init__(self) -> None:
        self.children: dict = {}
        self.word: str = ""


def findWords(board: List[List[str]], words: List[str]) -> List[str]:
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
    assert findWords([["a","a"]], ["aaa"]) == []
    b5 = [["a","b","c"],["d","e","f"],["g","h","i"]]
    assert sorted(findWords(b5, ["abc","adc","ghi","abef","beh","xyz"])) == sorted(["abc","ghi","abef","beh"])
    print("All tests passed for 212. Word Search II!")
