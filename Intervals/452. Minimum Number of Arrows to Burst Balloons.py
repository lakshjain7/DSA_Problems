"""
452. Minimum Number of Arrows to Burst Balloons
Difficulty: Medium
Topics: Array, Greedy, Sorting, Intervals

Problem Statement:
    There are some spherical balloons taped onto a flat wall that represents the
    XY-plane. The balloons are represented as a 2D integer array `points` where
    points[i] = [x_start, x_end] denotes a balloon whose horizontal diameter
    stretches between x_start and x_end. You do not know the exact y-coordinates
    of the balloons.

    Arrows can be shot up directly vertically (in the positive y-direction) from
    different points along the x-axis. A balloon with x_start and x_end is burst
    by an arrow shot at x if x_start <= x <= x_end. There is no limit to the
    number of arrows that can be shot. A shot arrow keeps traveling up infinitely,
    bursting any balloons in its path.

    Given the array `points`, return the minimum number of arrows that must be
    shot to burst all balloons.

Examples:
    Example 1:
        Input:  points = [[10,16],[2,8],[1,6],[7,12]]
        Output: 2
        Explanation: One arrow at x=6 bursts [2,8] and [1,6]; another at x=11
                     bursts [10,16] and [7,12].

    Example 2:
        Input:  points = [[1,2],[3,4],[5,6],[7,8]]
        Output: 4
        Explanation: No balloons overlap; one arrow each.

    Example 3:
        Input:  points = [[1,2],[2,3],[3,4],[4,5]]
        Output: 2

Constraints:
    - 1 <= points.length <= 10^5
    - points[i].length == 2
    - -2^31 <= x_start < x_end <= 2^31 - 1


Approach (Greedy on interval end points):
    This is the classic "maximum number of non-overlapping intervals" idea turned
    around: the minimum number of arrows equals the number of groups of mutually
    overlapping balloons, where one arrow serves each group.

    1. Sort balloons by their END coordinate (x_end).
    2. Shoot the first arrow at the end of the first balloon. Greedily, placing
       the arrow as far right as possible (at the current group's smallest end)
       maximizes how many later balloons it can also pierce.
    3. Walk through the remaining balloons. If a balloon's start is <= the current
       arrow position, it is already burst — skip it. Otherwise it starts after
       the arrow, so we need a new arrow; place it at this balloon's end.

    Why it works (exchange argument): sorting by end and always firing at the
    earliest end is optimal because any balloon overlapping the current group must
    contain that earliest end point; firing there bursts the maximal set, and no
    alternative arrow placement can cover strictly more of the sorted balloons.

Complexity:
    Time:  O(n log n) — dominated by the sort; the sweep is O(n).
    Space: O(1) auxiliary (ignoring the sort's overhead / O(n) if the sort is
           not in place).


Alternative Approach (Sort by start):
    One may instead sort by start coordinate and track the smallest end seen in
    the current overlapping group, shrinking the arrow position to
    min(current_end, balloon_end) while balloons keep overlapping. It yields the
    same count; the end-sort version is included below as a cross-check in tests.
"""

from typing import List


class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        """Greedy, sorting by end coordinate. Time O(n log n), space O(1)."""
        if not points:
            return 0

        points.sort(key=lambda p: p[1])
        arrows = 1
        arrow_x = points[0][1]

        for start, end in points[1:]:
            if start > arrow_x:
                # Current balloon starts after the last arrow -> need a new one.
                arrows += 1
                arrow_x = end
        return arrows

    def findMinArrowShotsByStart(self, points: List[List[int]]) -> int:
        """Alternative: sort by start, shrink group end. Same result."""
        if not points:
            return 0

        points.sort(key=lambda p: p[0])
        arrows = 1
        cur_end = points[0][1]

        for start, end in points[1:]:
            if start <= cur_end:
                # Still overlapping the current group; tighten the reachable end.
                cur_end = min(cur_end, end)
            else:
                arrows += 1
                cur_end = end
        return arrows


if __name__ == "__main__":
    sol = Solution()

    def check(points, expected):
        # Copy because both methods sort in place.
        assert sol.findMinArrowShots([p[:] for p in points]) == expected
        assert sol.findMinArrowShotsByStart([p[:] for p in points]) == expected

    # Example cases
    check([[10, 16], [2, 8], [1, 6], [7, 12]], 2)
    check([[1, 2], [3, 4], [5, 6], [7, 8]], 4)
    check([[1, 2], [2, 3], [3, 4], [4, 5]], 2)

    # Edge: single balloon
    check([[5, 9]], 1)

    # Edge: all balloons identical -> one arrow
    check([[1, 6], [1, 6], [1, 6]], 1)

    # Edge: fully nested balloons -> one arrow
    check([[1, 10], [2, 9], [3, 8], [4, 7]], 1)

    # Touching endpoints count as overlap (x_start <= x <= x_end)
    check([[1, 2], [2, 3]], 1)

    # Negative coordinates and large range: the huge balloon spans everything,
    # so a single arrow at x=0 bursts all three.
    check([[-2147483648, 2147483647], [-1, 0], [0, 1]], 1)

    # Chain where every other pair overlaps
    check([[1, 3], [2, 4], [5, 7], [6, 8]], 2)

    print("All tests passed for 452. Minimum Number of Arrows to Burst Balloons")
