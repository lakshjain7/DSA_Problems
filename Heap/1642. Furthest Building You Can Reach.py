"""
1642. Furthest Building You Can Reach
Difficulty: Medium
Topics: Array, Greedy, Heap (Priority Queue)

Problem:
You are given an integer array `heights` representing the heights of buildings,
some `bricks`, and some `ladders`.

You start your journey from building 0 and move to the next building by
possibly using bricks or ladders.

While moving from building i to building i+1 (0-indexed):
  - If the current building's height is greater than or equal to the next
    building's height, you do not need a ladder or bricks.
  - If the current building's height is less than the next building's height,
    you can either use one ladder or (h[i+1] - h[i]) bricks.

Return the furthest building index (0-indexed) you can reach if you use the
given ladders and bricks optimally.

Example 1:
    Input: heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1
    Output: 4
    Explanation: 0->1 free, 1->2 5 bricks, 2->3 free, 3->4 ladder.
    4->5 needs 5 bricks or a ladder, none left.

Example 2:
    Input: heights = [4,12,2,7,3,18,20,3,19], bricks = 10, ladders = 2
    Output: 7

Example 3:
    Input: heights = [14,3,19,3], bricks = 17, ladders = 0
    Output: 3

Constraints:
    1 <= heights.length <= 10^5
    1 <= heights[i] <= 10^6
    0 <= bricks <= 10^9
    0 <= ladders <= heights.length

Approach (Greedy + min-heap of the climbs assigned to ladders):
    Ladders are "free" regardless of climb size, so they should cover the
    LARGEST climbs seen so far; bricks pay for the rest. Walk left to right and
    push each positive climb into a min-heap. While the heap has at most
    `ladders` items, all those climbs are (tentatively) on ladders. Once it
    exceeds `ladders`, pop the smallest climb and pay for it with bricks.
    If bricks go negative, we cannot reach building i+1, so answer is i.

    Why it works: for any prefix, the cheapest way to cover it is to put
    ladders on its `ladders` largest climbs and bricks on the rest. The heap
    always holds exactly those largest climbs, and the bricks spent equal the
    sum of the remaining ones — the minimum possible — so the first prefix
    whose minimum brick cost exceeds `bricks` is exactly where we stop.

Complexity:
    Time:  O(n log L), L = ladders (heap size bounded by ladders + 1).
    Space: O(L).

Alternative (Binary search on the answer):
    Reachability is monotone in the target index. For a candidate index m,
    sort the climbs in heights[0..m], give ladders to the largest `ladders`
    climbs, and check the rest sum <= bricks. O(n log^2 n) — slower, but a
    nice illustration of "binary search on answer space".
"""
import heapq
from typing import List


class Solution:
    def furthestBuilding(self, heights: List[int], bricks: int, ladders: int) -> int:
        ladder_climbs: List[int] = []  # min-heap of climbs currently using ladders
        for i in range(len(heights) - 1):
            climb = heights[i + 1] - heights[i]
            if climb <= 0:
                continue
            heapq.heappush(ladder_climbs, climb)
            if len(ladder_climbs) > ladders:
                bricks -= heapq.heappop(ladder_climbs)
                if bricks < 0:
                    return i
        return len(heights) - 1

    def furthestBuildingBinarySearch(self, heights: List[int], bricks: int, ladders: int) -> int:
        def can_reach(m: int) -> bool:
            climbs = sorted(
                (heights[i + 1] - heights[i] for i in range(m) if heights[i + 1] > heights[i]),
                reverse=True,
            )
            return sum(climbs[ladders:]) <= bricks

        lo, hi = 0, len(heights) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can_reach(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([4, 2, 7, 6, 9, 14, 12], 5, 1, 4),
        ([4, 12, 2, 7, 3, 18, 20, 3, 19], 10, 2, 7),
        ([14, 3, 19, 3], 17, 0, 3),
        ([5], 0, 0, 0),                    # single building
        ([1, 2], 0, 0, 0),                 # can't make first climb
        ([1, 2], 1, 0, 1),                 # exactly enough bricks
        ([5, 4, 3, 2, 1], 0, 0, 4),        # all downhill, free
        ([1, 5, 1, 2, 3, 4, 10000], 4, 1, 5),  # ladder should move to the big jump
        ([1, 13, 1, 1, 13, 5, 10, 20], 10, 1, 3),
    ]
    for h, b, l, expected in cases:
        assert s.furthestBuilding(h, b, l) == expected, (h, b, l)
        assert s.furthestBuildingBinarySearch(h, b, l) == expected, (h, b, l)

    rng = random.Random(1642)
    for _ in range(500):
        n = rng.randint(1, 25)
        h = [rng.randint(1, 30) for _ in range(n)]
        b = rng.randint(0, 60)
        l = rng.randint(0, 4)
        assert s.furthestBuilding(h, b, l) == s.furthestBuildingBinarySearch(h, b, l), (h, b, l)

    print("All tests passed for 1642. Furthest Building You Can Reach")
