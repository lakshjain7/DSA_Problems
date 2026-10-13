"""
692. Top K Frequent Words
Difficulty: Medium
Topics: Hash Table, String, Trie, Sorting, Heap (Priority Queue), Counting

Problem:
Given an array of strings words and an integer k, return the k most frequent
strings. Sort the answer by frequency from highest to lowest; words with the
same frequency are sorted by lexicographical order (smallest first).

Example 1:
    Input: words = ["i","love","leetcode","i","love","coding"], k = 2
    Output: ["i","love"]
Example 2:
    Input: words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
    Output: ["the","is","sunny","day"]

Constraints:
    1 <= words.length <= 500
    1 <= words[i].length <= 10, lowercase English letters
    k is in the range [1, number of unique words]

Approach (min-heap of size k):
    Count frequencies. Keep a heap of the k "best" words. The heap root must be
    the *worst* of the kept words, so a word is worse if it has lower
    frequency, or equal frequency and lexicographically larger. A wrapper class
    reverses the string comparison on ties so heapq's min-heap pops the worst.
    Each new word replaces the root if it is better. Finally pop everything and
    reverse to get best-first order.

Complexity:
    Time: O(n + u log k) where u = unique words    Space: O(u)

Alternative: sort unique words by (-count, word) - O(u log u).
"""
import heapq
from collections import Counter
from typing import List


class _Item:
    __slots__ = ("cnt", "word")

    def __init__(self, cnt: int, word: str):
        self.cnt, self.word = cnt, word

    def __lt__(self, other: "_Item") -> bool:
        # "smaller" == worse: lower count, or same count and larger word
        if self.cnt != other.cnt:
            return self.cnt < other.cnt
        return self.word > other.word


def topKFrequent(words: List[str], k: int) -> List[str]:
    heap: List[_Item] = []
    for w, c in Counter(words).items():
        item = _Item(c, w)
        if len(heap) < k:
            heapq.heappush(heap, item)
        elif heap[0] < item:
            heapq.heapreplace(heap, item)
    res = []
    while heap:
        res.append(heapq.heappop(heap).word)
    return res[::-1]


def topKFrequentSort(words: List[str], k: int) -> List[str]:
    """Alternative: sort by (-count, word)."""
    cnt = Counter(words)
    return sorted(cnt, key=lambda w: (-cnt[w], w))[:k]


if __name__ == "__main__":
    tests = [
        (["i","love","leetcode","i","love","coding"], 2, ["i","love"]),
        (["the","day","is","sunny","the","the","the","sunny","is","is"], 4, ["the","is","sunny","day"]),
        (["a"], 1, ["a"]),
        (["b","a","c"], 3, ["a","b","c"]),
        (["b","a","c"], 1, ["a"]),
        (["aaa","aa","a"], 1, ["a"]),
        (["x","x","y","y","z"], 2, ["x","y"]),
    ]
    for w, k, exp in tests:
        assert topKFrequent(w, k) == exp, (w, k, exp, topKFrequent(w, k))
        assert topKFrequentSort(w, k) == exp
    print("All tests passed.")
