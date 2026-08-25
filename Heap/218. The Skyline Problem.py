"""
218. The Skyline Problem
Difficulty: Hard
Topics: Heap (Priority Queue), Sweep Line, Divide and Conquer, Sorting, Array

Problem Statement
-----------------
A city's skyline is the outer contour of the silhouette formed by all the
buildings in that city when viewed from a distance. Given the locations and
heights of all the buildings, return the skyline formed by these buildings
collectively.

The geometric information of each building is given in the array buildings where
buildings[i] = [left_i, right_i, height_i]:
- left_i is the x coordinate of the left edge of the ith building.
- right_i is the x coordinate of the right edge of the ith building.
- height_i is the height of the ith building.

You may assume all buildings are perfect rectangles grounded on an absolutely
flat surface at height 0.

The skyline should be represented as a list of "key points" sorted by their x
coordinate in the form [[x1,y1],[x2,y2],...]. Each key point is the left endpoint
of some horizontal segment in the skyline except the last point in the list,
which always has a y coordinate 0 and is used to mark the skyline's termination
where the rightmost building ends. Any ground between the leftmost and rightmost
buildings should be part of the skyline's contour.

Note: There must be no consecutive horizontal lines of equal height in the output
skyline. For instance, [...,[2 3],[4 5],[7 5],[11 5],[12 7],...] is not
acceptable; the three lines of height 5 should be merged into one:
[...,[2 3],[4 5],[12 7],...].

Examples
--------
Example 1:
    Input: buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
    Output: [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]

Example 2:
    Input: buildings = [[0,2,3],[2,5,3]]
    Output: [[0,3],[5,0]]

Constraints
-----------
- 1 <= buildings.length <= 10^4
- 0 <= left_i < right_i <= 2^31 - 1
- 1 <= height_i <= 2^31 - 1
- buildings is sorted by left_i in non-decreasing order.

Approach (Sweep Line + Max-Heap)
--------------------------------
We process "critical x coordinates" from left to right. At each such x, the
current skyline height equals the tallest building that currently covers x. When
that maximum height changes as we sweep, we record a key point.

Build a list of events, one per building edge:
- Left edge  (x = left,  height = -h): a building starts. We encode start
  heights as negative so that, after sorting by (x, height), starts are
  processed before ends at the same x, and taller starts before shorter ones.
- Right edge (x = right, height = +h): a building ends.

Sort all events by (x, height). Sweep through them maintaining a max-heap of
"active" building heights (implemented with a min-heap of negatives). For a
start event, push its height. For an end event, we mark the height for lazy
removal (removing from the middle of a heap is expensive, so we defer). After
updating the active set at a given x, the current max active height (0 if none)
is compared against the previous max; if it changed, x with the new height is a
key point.

Lazy deletion detail: we keep a counter of heights pending removal. When the top
of the heap is a height scheduled for removal, we pop it and decrement its
pending count, repeating until the top is a genuinely active height.

Why it works
------------
The skyline only changes at building edges. Between consecutive events the
covering set of buildings is constant, so the height is constant. Tracking the
running maximum of active heights and emitting a point whenever it changes
produces exactly the contour, and the start-before-end / tall-before-short
ordering correctly handles buildings that touch or overlap at a single x, while
preventing duplicate equal-height segments.

Complexity
----------
Time:  O(n log n) - sorting the 2n events dominates; each event does O(log n)
       heap work (with amortized lazy deletion).
Space: O(n) - events list, heap, and the lazy-removal bookkeeping.

Alternative Approach (Divide and Conquer)
-----------------------------------------
Split the buildings into two halves, compute each half's skyline recursively,
then merge the two skylines much like merge sort (sweeping both left to right and
taking, at each x, the max of the two current heights). This is also O(n log n)
time. Included below as `get_skyline_divide_conquer`.
"""

import heapq
from collections import defaultdict
from typing import List


def get_skyline(buildings: List[List[int]]) -> List[List[int]]:
    """Sweep line + lazy-deletion max-heap. O(n log n) time."""
    # Build events: start -> (x, -h), end -> (x, +h)
    events = []
    for left, right, height in buildings:
        events.append((left, -height))
        events.append((right, height))
    events.sort()

    result: List[List[int]] = []
    # Max-heap via negatives; sentinel 0 for ground level.
    live = [0]
    prev_max = 0
    to_remove = defaultdict(int)  # height -> count pending removal

    for x, h in events:
        if h < 0:
            # Building start: push its height.
            heapq.heappush(live, h)
        else:
            # Building end: schedule lazy removal of -h (stored as negative).
            to_remove[-h] += 1

        # Clean the top of the heap of any heights already ended.
        while live and to_remove[live[0]] > 0:
            to_remove[live[0]] -= 1
            heapq.heappop(live)

        curr_max = -live[0]
        if curr_max != prev_max:
            result.append([x, curr_max])
            prev_max = curr_max

    return result


def get_skyline_divide_conquer(buildings: List[List[int]]) -> List[List[int]]:
    """Divide and conquer (merge-sort style). O(n log n) time."""
    if not buildings:
        return []
    if len(buildings) == 1:
        left, right, height = buildings[0]
        return [[left, height], [right, 0]]

    mid = len(buildings) // 2
    left_sky = get_skyline_divide_conquer(buildings[:mid])
    right_sky = get_skyline_divide_conquer(buildings[mid:])
    return _merge_skylines(left_sky, right_sky)


def _merge_skylines(left: List[List[int]],
                    right: List[List[int]]) -> List[List[int]]:
    merged: List[List[int]] = []
    i = j = 0
    h_left = h_right = 0
    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0]:
            x = left[i][0]
            h_left = left[i][1]
            i += 1
        elif left[i][0] > right[j][0]:
            x = right[j][0]
            h_right = right[j][1]
            j += 1
        else:
            x = left[i][0]
            h_left = left[i][1]
            h_right = right[j][1]
            i += 1
            j += 1
        max_h = max(h_left, h_right)
        if not merged or merged[-1][1] != max_h:
            merged.append([x, max_h])

    while i < len(left):
        if not merged or merged[-1][1] != left[i][1]:
            merged.append(left[i])
        i += 1
    while j < len(right):
        if not merged or merged[-1][1] != right[j][1]:
            merged.append(right[j])
        j += 1

    return merged


if __name__ == "__main__":
    # Example 1
    b1 = [[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]
    expected1 = [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]
    assert get_skyline(b1) == expected1
    assert get_skyline_divide_conquer(b1) == expected1

    # Example 2
    b2 = [[0, 2, 3], [2, 5, 3]]
    expected2 = [[0, 3], [5, 0]]
    assert get_skyline(b2) == expected2
    assert get_skyline_divide_conquer(b2) == expected2

    # Single building
    assert get_skyline([[1, 5, 4]]) == [[1, 4], [5, 0]]
    assert get_skyline_divide_conquer([[1, 5, 4]]) == [[1, 4], [5, 0]]

    # Two identical footprints, different heights -> taller wins throughout
    assert get_skyline([[0, 4, 3], [0, 4, 5]]) == [[0, 5], [4, 0]]

    # Fully nested building (small building inside a taller one)
    nested = [[1, 10, 5], [3, 6, 3]]
    assert get_skyline(nested) == [[1, 5], [10, 0]]
    assert get_skyline_divide_conquer(nested) == [[1, 5], [10, 0]]

    # Adjacent non-overlapping buildings of different heights
    adj = [[1, 3, 4], [3, 6, 2]]
    assert get_skyline(adj) == [[1, 4], [3, 2], [6, 0]]
    assert get_skyline_divide_conquer(adj) == [[1, 4], [3, 2], [6, 0]]

    # Two buildings same height with a gap between them
    gap = [[1, 2, 3], [5, 6, 3]]
    assert get_skyline(gap) == [[1, 3], [2, 0], [5, 3], [6, 0]]
    assert get_skyline_divide_conquer(gap) == [[1, 3], [2, 0], [5, 3], [6, 0]]

    # Cross-check heap vs divide-and-conquer on a moderately complex case
    b3 = [[0, 5, 7], [5, 10, 7], [2, 3, 9], [4, 8, 3], [7, 12, 10]]
    assert get_skyline(b3) == get_skyline_divide_conquer(b3)

    print("All tests passed for 218. The Skyline Problem")
