"""
1032. Stream of Characters
Difficulty: Hard
Topics: Array, String, Design, Trie, Data Stream

Problem:
Design an algorithm that accepts a stream of characters and checks if a
suffix of these characters is a string of a given array of strings words.
For example, if words = ["abc", "xyz"] and the stream added the four
characters (one by one) 'a', 'x', 'y', and 'z', your algorithm should detect
that the suffix "xyz" of the characters "axyz" matches "xyz" from words.

Implement the StreamChecker class:
    - StreamChecker(String[] words) Initializes the object with the strings
      array words.
    - boolean query(char letter) Accepts a new character from the stream and
      returns true if any non-empty suffix from the stream forms a word that
      is in words.

Example 1:
    Input:
        ["StreamChecker", "query", "query", "query", "query", "query", "query",
         "query", "query", "query", "query", "query", "query"]
        [[["cd", "f", "kl"]], ["a"], ["b"], ["c"], ["d"], ["e"], ["f"], ["g"],
         ["h"], ["i"], ["j"], ["k"], ["l"]]
    Output:
        [null, false, false, false, true, false, true, false, false, false,
         false, false, true]

Constraints:
    1 <= words.length <= 2000
    1 <= words[i].length <= 200
    words[i] consists of lowercase English letters.
    letter is a lowercase English letter.
    At most 4 * 10^4 calls will be made to query.

Approach (Reversed-word Trie):
    A suffix of the stream ending at the newest character matches a word iff
    the word, read backwards, is a prefix of the stream read backwards.
    So insert every word reversed into a trie, keep the stream in a buffer,
    and on each query walk the trie from the newest character backwards. Stop
    as soon as we fall off the trie (no word can match) or hit an end-of-word
    node (match found). We only need to keep the last L characters, where L is
    the longest word length, so the buffer is a bounded deque.

Complexity:
    Build: O(sum of word lengths) time and space.
    Query: O(L) time, L = max word length (<= 200); usually far less because
           the walk stops at the first dead end.
    Space: O(sum of word lengths + L).

Alternative (Aho-Corasick automaton):
    Build failure links over the forward trie and keep one current state.
    Each query is amortized O(1) (just a goto transition with precomputed
    "output" flags), at the cost of a more complex build. Implemented below.
"""
from collections import deque
from typing import Deque, Dict, List


class StreamChecker:
    def __init__(self, words: List[str]) -> None:
        self.root: Dict = {}
        self.END = "#"
        self.max_len = 0
        for w in words:
            node = self.root
            for ch in reversed(w):
                node = node.setdefault(ch, {})
            node[self.END] = True
            self.max_len = max(self.max_len, len(w))
        self.stream: Deque[str] = deque(maxlen=self.max_len)

    def query(self, letter: str) -> bool:
        self.stream.appendleft(letter)
        node = self.root
        for ch in self.stream:
            if ch not in node:
                return False
            node = node[ch]
            if self.END in node:
                return True
        return False


class StreamCheckerAhoCorasick:
    def __init__(self, words: List[str]) -> None:
        # goto[state][c] -> next state; out[state] -> some word ends here
        self.goto: List[List[int]] = [[-1] * 26]
        self.out: List[bool] = [False]
        for w in words:
            s = 0
            for ch in w:
                c = ord(ch) - 97
                if self.goto[s][c] == -1:
                    self.goto[s][c] = len(self.goto)
                    self.goto.append([-1] * 26)
                    self.out.append(False)
                s = self.goto[s][c]
            self.out[s] = True

        fail = [0] * len(self.goto)
        q: Deque[int] = deque()
        for c in range(26):
            nxt = self.goto[0][c]
            if nxt == -1:
                self.goto[0][c] = 0
            else:
                fail[nxt] = 0
                q.append(nxt)
        while q:
            s = q.popleft()
            self.out[s] = self.out[s] or self.out[fail[s]]
            for c in range(26):
                nxt = self.goto[s][c]
                if nxt == -1:
                    self.goto[s][c] = self.goto[fail[s]][c]
                else:
                    fail[nxt] = self.goto[fail[s]][c]
                    q.append(nxt)
        self.state = 0

    def query(self, letter: str) -> bool:
        self.state = self.goto[self.state][ord(letter) - 97]
        return self.out[self.state]


def _brute(words: List[str], stream: str) -> List[bool]:
    res = []
    for i in range(1, len(stream) + 1):
        prefix = stream[:i]
        res.append(any(prefix.endswith(w) for w in words))
    return res


if __name__ == "__main__":
    import random

    words = ["cd", "f", "kl"]
    stream = "abcdefghijkl"
    expected = [False, False, False, True, False, True,
                False, False, False, False, False, True]
    for cls in (StreamChecker, StreamCheckerAhoCorasick):
        sc = cls(words)
        assert [sc.query(ch) for ch in stream] == expected

    # Overlapping words / word that is a suffix of another
    for cls in (StreamChecker, StreamCheckerAhoCorasick):
        sc = cls(["abc", "bc", "aaaa"])
        got = [sc.query(ch) for ch in "abcaaaaab"]
        assert got == _brute(["abc", "bc", "aaaa"], "abcaaaaab")

    # Single-letter word
    for cls in (StreamChecker, StreamCheckerAhoCorasick):
        sc = cls(["a"])
        assert [sc.query(ch) for ch in "bab"] == [False, True, False]

    # Randomized cross-check against brute force
    for _ in range(200):
        ws = ["".join(random.choice("abc") for _ in range(random.randint(1, 4)))
              for _ in range(random.randint(1, 5))]
        st = "".join(random.choice("abc") for _ in range(random.randint(1, 40)))
        exp = _brute(ws, st)
        for cls in (StreamChecker, StreamCheckerAhoCorasick):
            sc = cls(ws)
            assert [sc.query(ch) for ch in st] == exp, (ws, st)

    print("All tests passed!")
