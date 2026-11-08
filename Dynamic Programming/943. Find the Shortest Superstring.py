"""
943. Find the Shortest Superstring
Difficulty: Hard
Topics: Array, String, Dynamic Programming, Bitmask

Problem:
Given an array of strings words, return the smallest string that contains each string in
words as a substring. If there are multiple valid strings of the smallest length, return
any of them. You may assume that no string in words is a substring of another string
in words.

Example 1:
    Input: words = ["alex","loves","leetcode"]
    Output: "alexlovesleetcode"
    Explanation: All permutations of words are valid answers.
Example 2:
    Input: words = ["catg","ctaagt","gcta","ttca","atgcatc"]
    Output: "gctaagttcatgcatc"

Constraints:
    1 <= words.length <= 12
    1 <= words[i].length <= 20
    words[i] consists of lowercase English letters.
    All the strings of words are unique.

Approach (bitmask DP / shortest Hamiltonian path):
Let overlap[i][j] be the longest suffix of words[i] that is a prefix of words[j].
Appending words[j] after words[i] adds len(words[j]) - overlap[i][j] characters.
dp[mask][i] = minimum length of a string covering the words in mask and ending with
words[i]. Transition: dp[mask | 1<<j][j] = min(dp[mask][i] + len(words[j]) - overlap[i][j]).
Keep parent pointers, pick the best final word, then walk the parents backwards and
rebuild the string by appending only the non-overlapping suffix of each word.

Complexity:
    Time:  O(2^n * n^2 + n^2 * L)
    Space: O(2^n * n)
"""
from itertools import permutations
from typing import List


def shortestSuperstring(words: List[str]) -> str:
    n = len(words)
    ov = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a, b = words[i], words[j]
            for k in range(min(len(a), len(b)), 0, -1):
                if a.endswith(b[:k]):
                    ov[i][j] = k
                    break

    INF = float("inf")
    full = 1 << n
    dp = [[INF] * n for _ in range(full)]
    parent = [[-1] * n for _ in range(full)]
    for i in range(n):
        dp[1 << i][i] = len(words[i])

    for mask in range(full):
        for i in range(n):
            if dp[mask][i] == INF:
                continue
            for j in range(n):
                if mask >> j & 1:
                    continue
                nm = mask | (1 << j)
                cost = dp[mask][i] + len(words[j]) - ov[i][j]
                if cost < dp[nm][j]:
                    dp[nm][j] = cost
                    parent[nm][j] = i

    mask = full - 1
    last = min(range(n), key=lambda i: dp[mask][i])
    order = []
    while last != -1:
        order.append(last)
        prev = parent[mask][last]
        mask ^= 1 << last
        last = prev
    order.reverse()

    res = words[order[0]]
    for a, b in zip(order, order[1:]):
        res += words[b][ov[a][b]:]
    return res


# Alternative: brute-force over all permutations, O(n! * n * L). Only for small n / testing.
def shortestSuperstring_bruteforce(words: List[str]) -> str:
    def merge(a: str, b: str) -> str:
        for k in range(min(len(a), len(b)), 0, -1):
            if a.endswith(b[:k]):
                return a + b[k:]
        return a + b

    best = None
    for p in permutations(words):
        s = p[0]
        for w in p[1:]:
            s = merge(s, w)
        if best is None or len(s) < len(best):
            best = s
    return best


if __name__ == "__main__":
    import random
    r = shortestSuperstring(["alex", "loves", "leetcode"])
    assert len(r) == len("alexlovesleetcode") and all(w in r for w in ["alex", "loves", "leetcode"])
    ws = ["catg", "ctaagt", "gcta", "ttca", "atgcatc"]
    r = shortestSuperstring(ws)
    assert len(r) == 16 and all(w in r for w in ws)
    assert shortestSuperstring(["abc"]) == "abc"
    r = shortestSuperstring(["ab", "bc"])
    assert r == "abc"
    random.seed(1)
    for _ in range(200):
        n = random.randint(1, 6)
        words = list({"".join(random.choice("abc") for _ in range(random.randint(1, 5))) for _ in range(n)})
        words = [w for w in words if not any(w != o and w in o for o in words)]
        r = shortestSuperstring(words)
        assert all(w in r for w in words)
        assert len(r) == len(shortestSuperstring_bruteforce(words))
    print("All tests passed")
