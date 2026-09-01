"""
253. Meeting Rooms II
Difficulty: Medium
Topics: Arrays, Two Pointers, Greedy, Sorting, Heap (Priority Queue), Prefix Sum

PROBLEM STATEMENT
-----------------
Given an array of meeting time intervals `intervals` where
intervals[i] = [start_i, end_i], return the minimum number of conference rooms
required.

A meeting occupies a room during the half-open interval [start, end): a meeting
ending exactly when another begins does NOT create a conflict, so the two can
share a room.

Example 1:
    Input:  intervals = [[0, 30], [5, 10], [15, 20]]
    Output: 2
    Explanation:
        Room 1: [0, 30]
        Room 2: [5, 10], then [15, 20]

Example 2:
    Input:  intervals = [[7, 10], [2, 4]]
    Output: 1
    Explanation: The two meetings never overlap, so one room suffices.

Constraints:
    1 <= intervals.length <= 10^4
    0 <= start_i < end_i <= 10^6


APPROACH 1 — Min-heap of end times (primary solution)
------------------------------------------------------
Sort the meetings by start time. Maintain a min-heap holding the end times of
meetings currently occupying rooms. For each new meeting:
    - If the earliest-ending ongoing meeting (heap top) finishes at or before the
      new meeting's start, that room has freed up: pop it and reuse the room.
    - Push the new meeting's end time.
The heap's size at any moment equals the number of rooms in simultaneous use;
the answer is the maximum size the heap ever reaches, which is simply its size
after processing all meetings in sorted order (since we only ever pop one when a
room frees, the heap never shrinks below the true concurrency).

Why it works: processing meetings in start order guarantees that when we look at
a meeting, every room that could possibly have freed before it has an end time
already in the heap. Popping the minimum end time that is <= current start
greedily recycles a room, so the heap only grows when a genuinely concurrent
meeting appears. Thus the final heap size is the peak concurrency = min rooms.

Time Complexity:  O(n log n) — sorting plus n heap operations of O(log n).
Space Complexity: O(n) — the heap can hold up to n end times.


APPROACH 2 — Chronological event sweep / two-pointer (alternative)
------------------------------------------------------------------
Separate and sort all start times and all end times independently. Sweep a
pointer through starts; for each start, advance the end pointer past every
meeting that has already ended (end <= start), freeing rooms. Track the running
count of active meetings and its maximum. This is the classic "sort starts and
ends separately" trick and avoids a heap.

    rooms = 0, max_rooms = 0, e = 0
    for each start index s (in sorted order):
        while ends[e] <= starts[s]: e += 1   # a room freed up
        rooms = s - e + 1                    # active meetings so far
        max_rooms = max(max_rooms, rooms)

Time Complexity:  O(n log n) — two sorts.
Space Complexity: O(n) — the two arrays of times.

Both approaches are implemented and cross-checked below.
"""

from __future__ import annotations

import heapq
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """Min-heap of end times. See APPROACH 1."""
        if not intervals:
            return 0

        intervals.sort(key=lambda iv: iv[0])

        # Min-heap holding end times of meetings occupying rooms.
        end_times: List[int] = []
        for start, end in intervals:
            # If the earliest-ending meeting is done, reuse its room.
            if end_times and end_times[0] <= start:
                heapq.heapreplace(end_times, end)  # pop min, push end
            else:
                heapq.heappush(end_times, end)

        return len(end_times)

    def minMeetingRoomsSweep(self, intervals: List[List[int]]) -> int:
        """Chronological event sweep with two pointers. See APPROACH 2."""
        if not intervals:
            return 0

        starts = sorted(iv[0] for iv in intervals)
        ends = sorted(iv[1] for iv in intervals)

        n = len(intervals)
        max_rooms = 0
        e = 0
        for s in range(n):
            # Free every room whose meeting ended at or before this start.
            while e < n and ends[e] <= starts[s]:
                e += 1
            rooms = s - e + 1
            max_rooms = max(max_rooms, rooms)
        return max_rooms


if __name__ == "__main__":
    sol = Solution()

    def check(intervals: List[List[int]], expected: int) -> None:
        # Copy because the heap approach sorts in place.
        got_heap = sol.minMeetingRooms([iv[:] for iv in intervals])
        got_sweep = sol.minMeetingRoomsSweep([iv[:] for iv in intervals])
        assert got_heap == expected, f"heap: {intervals} -> {got_heap}, want {expected}"
        assert got_sweep == expected, f"sweep: {intervals} -> {got_sweep}, want {expected}"

    # Provided examples.
    check([[0, 30], [5, 10], [15, 20]], 2)
    check([[7, 10], [2, 4]], 1)

    # Single meeting.
    check([[1, 5]], 1)

    # Meetings that touch at endpoints share a room (half-open intervals).
    check([[1, 5], [5, 10], [10, 15]], 1)

    # Fully nested meetings all overlap.
    check([[1, 10], [2, 9], [3, 8], [4, 7]], 4)

    # Identical meetings all need their own room.
    check([[2, 4], [2, 4], [2, 4]], 3)

    # Staggered overlaps: peak concurrency is 2.
    check([[1, 4], [2, 5], [7, 9]], 2)

    # Unsorted input with a mix.
    check([[13, 15], [1, 13], [6, 9]], 2)

    # Large chain of non-overlapping meetings -> 1 room.
    check([[i, i + 1] for i in range(0, 20, 1)], 1)

    # All start at 0 -> n rooms.
    check([[0, 5], [0, 6], [0, 7], [0, 8], [0, 9]], 5)

    print("All 253. Meeting Rooms II tests passed!")
