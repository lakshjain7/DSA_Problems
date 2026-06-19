"""
Problem 56: Merge Intervals
Difficulty: Medium
Topics: Array, Sorting

Problem Statement:
Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping
intervals, and return an array of the non-overlapping intervals that cover all the
intervals in the input.

Examples:
    Example 1:
        Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
        Output: [[1,6],[8,10],[15,18]]
        Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

    Example 2:
        Input: intervals = [[1,4],[4,5]]
        Output: [[1,5]]
        Explanation: Intervals [1,4] and [4,5] are considered overlapping.

Constraints:
    - 1 <= intervals.length <= 10^4
    - intervals[i].length == 2
    - 0 <= starti <= endi <= 10^4

Approach:
    Sort intervals by start time. Then iterate through:
    - If the current interval's start <= last merged interval's end, they overlap ->
      extend the last interval's end to max(last.end, curr.end).
    - Otherwise, no overlap -> push current interval as a new merged interval.

    Sorting guarantees that if two intervals overlap, they are adjacent after sorting,
    so a single linear pass is sufficient.

Complexity:
    Time:  O(n log n) -- dominated by sorting
    Space: O(n) -- output list (O(log n) for sort stack if in-place, but output is O(n))
"""

from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:
            # Overlapping: extend the last interval's end
            merged[-1][1] = max(last_end, end)
        else:
            # Non-overlapping: start a new interval
            merged.append([start, end])

    return merged


# Alternative Approach: Same logic but written more explicitly using index tracking
def merge_v2(intervals: List[List[int]]) -> List[List[int]]:
    """
    Equivalent approach using explicit index -- useful when the sorted array is
    given and you need to modify in-place.
    """
    intervals.sort()
    result = []
    i = 0
    while i < len(intervals):
        curr_start, curr_end = intervals[i]
        # Absorb all subsequent intervals that overlap
        while i + 1 < len(intervals) and intervals[i + 1][0] <= curr_end:
            i += 1
            curr_end = max(curr_end, intervals[i][1])
        result.append([curr_start, curr_end])
        i += 1
    return result


if __name__ == "__main__":
    # Basic overlap
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]

    # Touch at boundary (should merge)
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]

    # All non-overlapping
    assert merge([[1, 2], [3, 4], [5, 6]]) == [[1, 2], [3, 4], [5, 6]]

    # All overlapping (one big interval)
    assert merge([[1, 10], [2, 5], [3, 8]]) == [[1, 10]]

    # Single interval
    assert merge([[5, 5]]) == [[5, 5]]

    # Unsorted input
    assert merge([[15, 18], [1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10], [15, 18]]

    # Contained interval
    assert merge([[1, 10], [2, 3]]) == [[1, 10]]

    # v2 produces same results
    assert merge_v2([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge_v2([[1, 4], [4, 5]]) == [[1, 5]]

    print("All tests passed!")
