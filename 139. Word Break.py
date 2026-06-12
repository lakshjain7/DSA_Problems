"""
Problem 139 - Word Break
Difficulty: Medium
Topics: Dynamic Programming, Strings, Hash Table

Problem Statement:
Given a string s and a dictionary of strings wordDict, return true if s can be
segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the
segmentation.

Example 1:
    Input: s = "leetcode", wordDict = ["leet","code"]
    Output: true
    Explanation: Return true because "leetcode" can be segmented as "leet code".

Example 2:
    Input: s = "applepenapple", wordDict = ["apple","pen"]
    Output: true
    Explanation: Return true because "applepenapple" can be segmented as
    "apple pen apple". Note that you are allowed to reuse a dictionary word.

Example 3:
    Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
    Output: false

Constraints:
    1 <= s.length <= 300
    1 <= wordDict.length <= 1000
    1 <= wordDict[i].length <= 20
    s and wordDict[i] consist of only lowercase English letters
    All the strings of wordDict are unique

Approach (1D DP):
    Define dp[i] = True if s[0:i] can be segmented using wordDict.
    Base case: dp[0] = True (empty string is always valid).
    Transition: for each i, scan every j < i:
        if dp[j] is True AND s[j:i] is in word_set -> set dp[i] = True.

    We convert wordDict to a set for O(1) lookups.
    The key insight: if we can segment s[0:j] and s[j:i] is a valid word,
    then s[0:i] is also segmentable.

Complexity:
    Time:  O(n^2) iterations * O(m) for string slice comparison = O(n^2 * m)
           where n = len(s), m = max word length
    Space: O(n) for the dp array, O(W) for the word set

Alternative Approach (BFS):
    Treat each index as a node. Start a BFS from index 0.
    From each index, try every word: if s[start:start+len(word)] == word,
    enqueue (start + len(word)). Return True if we reach index n.
    Same asymptotic complexity; can be faster when the word list is small.
"""
from typing import List
from collections import deque


def wordBreak(s: str, wordDict: List[str]) -> bool:
    """
    DP approach: dp[i] means s[0:i] is segmentable.
    """
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # empty prefix is always valid

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break  # found one valid split -- no need to continue

    return dp[n]


def wordBreak_bfs(s: str, wordDict: List[str]) -> bool:
    """
    Alternative: BFS over string indices.
    Each node is a starting position; edges are valid word matches.
    """
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
    # --- DP version ---
    assert wordBreak("leetcode", ["leet", "code"]) == True
    assert wordBreak("applepenapple", ["apple", "pen"]) == True
    assert wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False

    # Single character
    assert wordBreak("a", ["a"]) == True
    assert wordBreak("a", ["b"]) == False

    # Reuse same word
    assert wordBreak("aaaaaa", ["aaa", "a"]) == True
    assert wordBreak("aaaaaaa", ["aaaa", "aaa"]) == True   # 4+3 or 3+4

    # No valid segmentation
    assert wordBreak("abcd", ["ab", "c"]) == False
    assert wordBreak("abcd", ["ab", "cd"]) == True

    # Entire string is one word
    assert wordBreak("hello", ["hello"]) == True

    # --- BFS version (same expected results) ---
    assert wordBreak_bfs("leetcode", ["leet", "code"]) == True
    assert wordBreak_bfs("applepenapple", ["apple", "pen"]) == True
    assert wordBreak_bfs("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False
    assert wordBreak_bfs("aaaaaa", ["aaa", "a"]) == True

    print("All tests passed!")
