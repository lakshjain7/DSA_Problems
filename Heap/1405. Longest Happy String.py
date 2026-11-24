"""
1405. Longest Happy String
Difficulty: Medium
Topics: String, Greedy, Heap (Priority Queue)

Problem:
A string s is called happy if it satisfies the following conditions:
    - s only contains the letters 'a', 'b', and 'c'.
    - s does not contain any of "aaa", "bbb", or "ccc" as a substring.
    - s contains at most a occurrences of the letter 'a'.
    - s contains at most b occurrences of the letter 'b'.
    - s contains at most c occurrences of the letter 'c'.
Given three integers a, b, and c, return the longest possible happy string.
If there are multiple longest happy strings, return any of them. If there is
no such string, return the empty string "".

Example 1:
    Input: a = 1, b = 1, c = 7
    Output: "ccaccbcc"   ("ccbccacc" is also correct)

Example 2:
    Input: a = 7, b = 1, c = 0
    Output: "aabaa"

Constraints:
    0 <= a, b, c <= 100
    a + b + c > 0

Approach (Greedy + Max-Heap):
    Always try to place the letter with the most remaining copies - using up
    the most abundant letter early is what lets the scarcer letters act as
    separators later. Keep a max-heap of (count, letter).
      - Pop the most frequent letter. If appending it would create three in a
        row, pop the second most frequent letter instead, append it once, and
        push both back.
      - If there's no second letter available, we're stuck: stop.
    Exchange argument: any optimal string can be rearranged to follow this
    greedy order without shortening it, so the greedy length is maximal.

Complexity:
    Time:  O(a + b + c) - each step appends one character; heap has <= 3 items.
    Space: O(1) extra besides the output string.

Alternative (Greedy without heap):
    At each step, scan the three letters sorted by remaining count and pick the
    first one that doesn't create a triple. Same complexity, no heap.
"""
import heapq
from typing import List


def longestDiverseString(a: int, b: int, c: int) -> str:
    heap = [(-cnt, ch) for cnt, ch in ((a, "a"), (b, "b"), (c, "c")) if cnt > 0]
    heapq.heapify(heap)
    res: List[str] = []

    while heap:
        cnt1, ch1 = heapq.heappop(heap)
        if len(res) >= 2 and res[-1] == res[-2] == ch1:
            if not heap:
                break
            cnt2, ch2 = heapq.heappop(heap)
            res.append(ch2)
            if cnt2 + 1 < 0:
                heapq.heappush(heap, (cnt2 + 1, ch2))
            heapq.heappush(heap, (cnt1, ch1))
        else:
            res.append(ch1)
            if cnt1 + 1 < 0:
                heapq.heappush(heap, (cnt1 + 1, ch1))
    return "".join(res)


def longestDiverseString_scan(a: int, b: int, c: int) -> str:
    counts = {"a": a, "b": b, "c": c}
    res: List[str] = []
    while True:
        placed = False
        for ch in sorted(counts, key=lambda k: -counts[k]):
            if counts[ch] == 0:
                break
            if len(res) >= 2 and res[-1] == res[-2] == ch:
                continue
            res.append(ch)
            counts[ch] -= 1
            placed = True
            break
        if not placed:
            return "".join(res)


def _is_happy(s: str, a: int, b: int, c: int) -> bool:
    return (
        set(s) <= set("abc")
        and "aaa" not in s and "bbb" not in s and "ccc" not in s
        and s.count("a") <= a and s.count("b") <= b and s.count("c") <= c
    )


def _optimal_length(a: int, b: int, c: int) -> int:
    x, y, z = sorted((a, b, c), reverse=True)
    return min(x, 2 * (y + z + 1)) + y + z


if __name__ == "__main__":
    for f in (longestDiverseString, longestDiverseString_scan):
        s = f(1, 1, 7)
        assert _is_happy(s, 1, 1, 7) and len(s) == 8
        s = f(7, 1, 0)
        assert _is_happy(s, 7, 1, 0) and len(s) == 5
        assert f(0, 0, 1) == "c"
        assert f(0, 0, 5) == "cc"
        s = f(2, 2, 1)
        assert _is_happy(s, 2, 2, 1) and len(s) == 5

    for a in range(0, 12):
        for b in range(0, 12):
            for c in range(0, 12):
                if a + b + c == 0:
                    continue
                for f in (longestDiverseString, longestDiverseString_scan):
                    s = f(a, b, c)
                    assert _is_happy(s, a, b, c), (a, b, c, s)
                    assert len(s) == _optimal_length(a, b, c), (a, b, c, s)

    s = longestDiverseString(100, 100, 100)
    assert len(s) == 300 and _is_happy(s, 100, 100, 100)

    print("All tests passed!")
