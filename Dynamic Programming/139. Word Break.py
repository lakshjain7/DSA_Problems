"""
Problem 139 - Word Break
Difficulty: Medium
Topics: Dynamic Programming, Strings, Hash Table

dp[i] = True if s[0:i] can be segmented using wordDict.
Complexity: O(n^2 * m) time, O(n) space.
"""
from typing import List
from collections import deque


def wordBreak(s: str, wordDict: List[str]) -> bool:
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]


def wordBreak_bfs(s: str, wordDict: List[str]) -> bool:
    word_set = set(wordDict)
    n = len(s)
    visited = set()
    queue = deque([0])

    while queue:
        start = queue.popleft()
        if start in visited:
            continue
        visited.add(start)
        for word in word_set:
            end = start + len(word)
            if end <= n and s[start:end] == word:
                if end == n:
                    return True
                queue.append(end)

    return False


if __name__ == "__main__":
    assert wordBreak("leetcode", ["leet", "code"]) == True
    assert wordBreak("applepenapple", ["apple", "pen"]) == True
    assert wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False
    assert wordBreak("a", ["a"]) == True
    assert wordBreak("a", ["b"]) == False
    assert wordBreak("aaaaaa", ["aaa", "a"]) == True
    assert wordBreak("aaaaaaa", ["aaaa", "aaa"]) == True
    assert wordBreak("abcd", ["ab", "c"]) == False
    assert wordBreak("abcd", ["ab", "cd"]) == True
    assert wordBreak("hello", ["hello"]) == True
    assert wordBreak_bfs("leetcode", ["leet", "code"]) == True
    assert wordBreak_bfs("applepenapple", ["apple", "pen"]) == True
    assert wordBreak_bfs("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False
    assert wordBreak_bfs("aaaaaa", ["aaa", "a"]) == True
    print("All tests passed!")
