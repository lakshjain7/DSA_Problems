"""
Problem: 435. Non-overlapping Intervals
Difficulty: Medium
Topics: Greedy, Intervals, Sorting

Problem Statement:
    Given an array of intervals intervals where intervals[i] = [starti, endi],
    return the minimum number of intervals you need to remove to make the rest
    of the intervals non-overlapping.

    Note that intervals which only touch at a point are non-overlapping.
    For example, [1, 2] and [2, 3] are non-overlapping.

Examples:
    Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
    Output: 1
    Explanation: Remove [1,3] to make rest non-overlapping.

    Input: intervals = [[1,2],[1,2],[1,2]]
    Output: 2
    Explanation: Need to remove two [1,2] to keep only one.

    Input: intervals = [[1,2],[2,3]]
    Output: 0
    Explanation: They touch at 2 but are non-overlapping.

Constraints:
    - 1 <= intervals.length <= 10^5
    - intervals[i].length == 2
    - -5 * 10^4 <= starti < endi <= 5 * 10^4

Approach (Greedy — Activity Selection):
    This is equivalent to finding the maximum number of non-overlapping intervals
    (Activity Selection Problem), then subtracting from total count.

    Key insight: Sort by END time. Greedily pick the interval with the earliest
    end time, since it leaves maximum room for future intervals. If the next
    interval's start >= current end, it's compatible — take it and advance our
    "current end" pointer. Otherwise, skip it (count as removed).

    Why sort by end (not start)? Sorting by end ensures we always choose the
    interval that finishes earliest, maximally freeing space for future choices.

Complexity:
    Time:  O(n log n) for sorting
    Space: O(1) extra (in-place sort)

Alternative:
    DP approach: dp[i] = max non-overlapping intervals ending at i.
    Sort by end, for each i find latest j where end[j] <= start[i].
    dp[i] = dp[j] + 1. Time: O(n log n), Space: O(n) — less elegant.
"""

from typing import List


def eraseOverlapIntervals(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0

    # Sort by end time
    intervals.sort(key=lambda x: x[1])

    keep = 1                    # greedily keep the first interval
    current_end = intervals[0][1]

    for i in range(1, len(intervals)):
        start, end = intervals[i]
        if start >= current_end:
            # Compatible: keep this interval, advance boundary
            keep += 1
            current_end = end
        # else: overlap — skip this interval (implicitly remove it)

    return len(intervals) - keep


if __name__ == "__main__":
    # Basic cases from problem
    assert eraseOverlapIntervals([[1,2],[2,3],[3,4],[1,3]]) == 1
    assert eraseOverlapIntervals([[1,2],[1,2],[1,2]]) == 2
    assert eraseOverlapIntervals([[1,2],[2,3]]) == 0

    # Single interval — nothing to remove
    assert eraseOverlapIntervals([[5,10]]) == 0

    # All intervals identical
    assert eraseOverlapIntervals([[0,1],[0,1],[0,1],[0,1]]) == 3

    # No overlaps at all
    assert eraseOverlapIntervals([[1,2],[3,4],[5,6]]) == 0

    # All overlapping, chain
    assert eraseOverlapIntervals([[1,10],[2,3],[4,5],[6,7]]) == 1

    # Empty input
    assert eraseOverlapIntervals([]) == 0

    # Two fully overlapping
    assert eraseOverlapIntervals([[1,100],[2,3]]) == 1

    print("All tests passed for 435. Non-overlapping Intervals!")
