"""
Problem #269 — Alien Dictionary
Difficulty : Hard
Topics     : Graph, Topological Sort (Kahn's Algorithm / DFS), BFS, String

Return the alien alphabet ordering derived from a sorted word list, or '' if impossible.

Approach: Kahn's BFS topological sort on character ordering constraints.
Alternative: DFS post-order topological sort.

Complexity: O(C) time where C = total characters; O(U) space for U unique chars.
"""

from collections import defaultdict, deque
from typing import List


def alien_order(words: List[str]) -> str:
    in_degree: dict[str, int] = {ch: 0 for word in words for ch in word}
    adj: dict[str, set[str]] = defaultdict(set)

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break

    queue: deque[str] = deque(ch for ch in in_degree if in_degree[ch] == 0)
    result: list[str] = []

    while queue:
        ch = queue.popleft()
        result.append(ch)
        for neighbor in adj[ch]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) < len(in_degree):
        return ""

    return "".join(result)


if __name__ == "__main__":
    assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert alien_order(["z", "x"]) == "zx"
    assert alien_order(["z", "x", "z"]) == ""
    assert alien_order(["abc", "ab"]) == ""
    print("All assertions passed!")
