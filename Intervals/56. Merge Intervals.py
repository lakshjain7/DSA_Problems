"""
Problem 56: Merge Intervals
Difficulty: Medium
Topics: Array, Sorting

Sort by start time, then merge overlapping intervals in a single pass.
Complexity: O(n log n) time, O(n) space.
"""

from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged


def merge_v2(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort()
    result = []
    i = 0
    while i < len(intervals):
        curr_start, curr_end = intervals[i]
        while i + 1 < len(intervals) and intervals[i + 1][0] <= curr_end:
            i += 1
            curr_end = max(curr_end, intervals[i][1])
        result.append([curr_start, curr_end])
        i += 1
    return result


if __name__ == "__main__":
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge([[1, 2], [3, 4], [5, 6]]) == [[1, 2], [3, 4], [5, 6]]
    assert merge([[1, 10], [2, 5], [3, 8]]) == [[1, 10]]
    assert merge([[5, 5]]) == [[5, 5]]
    assert merge([[15, 18], [1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[1, 10], [2, 3]]) == [[1, 10]]
    assert merge_v2([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge_v2([[1, 4], [4, 5]]) == [[1, 5]]
    print("All tests passed!")
