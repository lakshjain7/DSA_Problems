"""
Problem Number: 127
Title: Word Ladder
Difficulty: Hard
Topics: Hash Table, String, BFS

Problem Statement:
    A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence
    of words beginWord -> s1 -> s2 -> ... -> sk such that:
    - Every adjacent pair of words differs by exactly one letter.
    - Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
    - sk == endWord.
    Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the
    shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

Examples:
    Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
    Output: 5
    Explanation: "hit" -> "hot" -> "dot" -> "dog" -> "cog"

    Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
    Output: 0
    Explanation: endWord "cog" is not in wordList.

Constraints:
    1 <= beginWord.length <= 10
    endWord.length == beginWord.length
    1 <= wordList.length <= 5000
    wordList[i].length == beginWord.length
    beginWord, endWord, and wordList[i] consist of lowercase English letters.
    beginWord != endWord
    All the words in wordList are unique.

Approach:
    BFS from beginWord. At each step, generate all words that differ by exactly one character
    from the current word, check if they exist in the wordList set, and add unseen ones to the queue.
    The first time we reach endWord, we return the current level (step count).

    Key optimization: build a pattern -> [words] adjacency map.
    For each word, replace each character with '*' to get a pattern (e.g., "hit" -> "*it", "h*t", "hi*").
    This avoids O(26 * L) per word by grouping words with the same wildcard pattern.
    Then BFS traverses these pattern groups instead of trying all 26 letters.

    Alternative (simpler O(26*L*N) BFS): For each word in the queue, try replacing each position
    with 'a'-'z' and check if the result is in the word set. Faster in practice for small alphabets.

Complexity (pattern map approach):
    Time:  O(M^2 * N) where M = word length, N = number of words (building pattern map + BFS)
    Space: O(M^2 * N) for the pattern map

Complexity (simple BFS):
    Time:  O(M * 26 * N) = O(M * N)
    Space: O(N) for visited set and queue
"""

from typing import List
from collections import deque, defaultdict


def ladderLength(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """Pattern-based BFS for clarity and interview elegance."""
    word_set = set(wordList)
    if endWord not in word_set:
        return 0

    # Build pattern -> list of matching words
    L = len(beginWord)
    pattern_map = defaultdict(list)
    for word in wordList:
        for i in range(L):
            pattern = word[:i] + '*' + word[i+1:]
            pattern_map[pattern].append(word)

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, level = queue.popleft()
        for i in range(L):
            pattern = word[:i] + '*' + word[i+1:]
            for neighbor in pattern_map[pattern]:
                if neighbor == endWord:
                    return level + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, level + 1))

    return 0


def ladderLength_simple(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """Simple BFS trying all 26 letters at each position."""
    word_set = set(wordList)
    if endWord not in word_set:
        return 0

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, level = queue.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                if new_word == endWord:
                    return level + 1
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, level + 1))

    return 0


if __name__ == "__main__":
    # Basic examples
    assert ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0

    # endWord not in wordList
    assert ladderLength("a", "c", ["a", "b", "c"]) == 2

    # Direct one-step transformation
    assert ladderLength("hot", "dog", ["hot", "dot", "dog"]) == 3

    # No path possible
    assert ladderLength("hit", "xyz", ["hot", "dot", "dog"]) == 0

    # Simple BFS version matches
    assert ladderLength_simple("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert ladderLength_simple("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    assert ladderLength_simple("a", "c", ["a", "b", "c"]) == 2

    print("All tests passed for 127. Word Ladder")
