"""
Problem Number: 57
Title: Insert Interval
Difficulty: Medium
Topics: Array, Sorting, Intervals

Problem Statement:
    You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi]
    represent the start and the end of the ith interval and intervals is sorted in ascending order by starti.
    You are also given an interval newInterval = [start, end] that represents the start and end of another interval.
    Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and
    intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).
    Return intervals after the insertion.

    Note that you don't need to modify intervals in place. You can make a new array and return it.

Examples:
    Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
    Output: [[1,5],[6,9]]

    Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
    Output: [[1,2],[3,10],[12,16]]

Constraints:
    0 <= intervals.length <= 10^4
    intervals[i].length == 2
    0 <= starti <= endi <= 10^5
    intervals is sorted by starti in ascending order.
    newInterval.length == 2
    0 <= start <= end <= 10^5

Approach:
    Single-pass linear scan — three phases:
    1. Add all intervals that end strictly before newInterval starts (no overlap, comes before).
    2. Merge all intervals that overlap with newInterval (overlap when interval.start <= newInterval.end).
       Keep expanding newInterval to cover all overlapping ones.
    3. Add all remaining intervals that start strictly after the merged interval ends.

    Two intervals [a,b] and [c,d] overlap iff a <= d AND c <= b.
    Equivalently, they DON'T overlap iff b < c (current ends before new starts) or d < a (new ends before current starts).

Complexity:
    Time:  O(n) — single pass
    Space: O(n) — output list
"""

from typing import List


def insert(intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
    result = []
    i = 0
    n = len(intervals)

    # Phase 1: intervals entirely before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # Phase 2: merge all overlapping intervals into newInterval
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)

    # Phase 3: intervals entirely after newInterval
    while i < n:
        result.append(intervals[i])
        i += 1

    return result


if __name__ == "__main__":
    # Basic examples
    assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]

    # Edge: empty intervals list
    assert insert([], [5, 7]) == [[5, 7]]

    # Edge: insert at beginning
    assert insert([[3, 5], [7, 9]], [1, 2]) == [[1, 2], [3, 5], [7, 9]]

    # Edge: insert at end
    assert insert([[1, 3], [5, 7]], [8, 10]) == [[1, 3], [5, 7], [8, 10]]

    # Edge: newInterval covers all existing intervals
    assert insert([[1, 2], [3, 4], [5, 6]], [0, 10]) == [[0, 10]]

    # Edge: newInterval touches boundary exactly (adjacent, not overlapping)
    assert insert([[1, 3], [6, 9]], [3, 6]) == [[1, 9]]  # 3==3 and 6==6 so they overlap

    # Edge: single interval, no overlap
    assert insert([[5, 7]], [1, 3]) == [[1, 3], [5, 7]]

    # Edge: newInterval already contained within existing interval
    assert insert([[1, 10]], [3, 5]) == [[1, 10]]

    print("All tests passed for 57. Insert Interval")
