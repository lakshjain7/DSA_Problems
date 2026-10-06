"""
763. Partition Labels
Difficulty: Medium
Topics: Hash Table, Two Pointers, String, Greedy

You are given a string s. We want to partition the string into as many parts
as possible so that each letter appears in at most one part. Note that the
partition is done so that after concatenating all the parts in order, the
resultant string should be s.

Return a list of integers representing the size of these parts.

Example 1:
    Input: s = "ababcbacadefegdehijhklij"
    Output: [9, 7, 8]
Example 2:
    Input: s = "eccbbbbdec"
    Output: [10]

Constraints:
    1 <= s.length <= 500
    s consists of lowercase English letters.

Approach (greedy, two pointers):
    Record the last index of every character. Sweep with index i, keeping
    `end` = the furthest last-occurrence among characters seen in the current
    part. When i == end, every character in the part has all its occurrences
    inside it, so cut here. Cutting at the earliest such point maximizes the
    number of parts.

Complexity:
    Time: O(n)   Space: O(1) (26 letters)
"""
from typing import List


def partitionLabels(s: str) -> List[int]:
    last = {c: i for i, c in enumerate(s)}
    res: List[int] = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res


# Alternative: merge the [first, last] interval of each character.
def partitionLabelsIntervals(s: str) -> List[int]:
    first, last = {}, {}
    for i, c in enumerate(s):
        first.setdefault(c, i)
        last[c] = i
    intervals = sorted((first[c], last[c]) for c in first)
    res: List[int] = []
    cs, ce = intervals[0]
    for a, b in intervals[1:]:
        if a > ce:
            res.append(ce - cs + 1)
            cs, ce = a, b
        else:
            ce = max(ce, b)
    res.append(ce - cs + 1)
    return res


if __name__ == "__main__":
    for f in (partitionLabels, partitionLabelsIntervals):
        assert f("ababcbacadefegdehijhklij") == [9, 7, 8]
        assert f("eccbbbbdec") == [10]
        assert f("a") == [1]
        assert f("abc") == [1, 1, 1]
        assert f("aaaa") == [4]
        assert f("abab") == [4]
    print("All tests passed.")
