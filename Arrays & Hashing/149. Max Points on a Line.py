"""
149. Max Points on a Line
Difficulty: Hard
Topics: Array, Hash Table, Math, Geometry

Problem Statement
-----------------
Given an array of `points` where points[i] = [xi, yi] represents a point on the
X-Y plane, return the maximum number of points that lie on the same straight
line.

Example 1:
    Input:  points = [[1,1],[2,2],[3,3]]
    Output: 3

Example 2:
    Input:  points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]
    Output: 4

Constraints:
    - 1 <= points.length <= 300
    - points[i].length == 2
    - -10^4 <= xi, yi <= 10^4
    - All the points are unique.

Approach (anchor point + slope counting with exact integer slopes)
------------------------------------------------------------------
Any line through 2+ points is determined by a slope and an anchor. Fix each
point `i` as an anchor, then look at the slope of the line from `i` to every
other point `j > i`. Points sharing the same slope relative to `i` are collinear
with `i`. The largest such group (plus the anchor itself) is a candidate answer.

Key detail - represent slope EXACTLY to avoid floating-point error:
    dx = xj - xi,  dy = yj - yi
Reduce (dx, dy) by g = gcd(dx, dy) and canonicalize the sign so that equal
slopes map to identical keys:
    - vertical line (dx == 0)   -> sentinel (0, 1)  (reduced slopes never have dx == 0)
    - horizontal line (dy == 0) -> sentinel (1, 0)  (reduced slopes never have dy == 0)
    - otherwise force dx > 0; if dx < 0 negate both dx and dy.
Using the reduced (dx, dy) integer pair as a dict key is exact.

For anchor `i`, count how many points share each slope key; the best local
count + 1 (for the anchor) updates the global maximum. We only need j > i
because any line is discovered from its earliest anchor.

Special case: if there is a single point, the answer is 1.

Complexity
----------
Time:  O(n^2 * log(C))  - for each of the n anchors we look at O(n) other points
                          and do a gcd (log of coordinate magnitude C).
Space: O(n)             - the slope dictionary per anchor.
"""

from collections import defaultdict
from math import gcd
from typing import List, Tuple


class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 2:
            return n

        best = 1
        for i in range(n):
            xi, yi = points[i]
            slopes = defaultdict(int)
            for j in range(i + 1, n):
                xj, yj = points[j]
                key = self._slope_key(xj - xi, yj - yi)
                slopes[key] += 1
                if slopes[key] + 1 > best:
                    best = slopes[key] + 1
        return best

    @staticmethod
    def _slope_key(dx: int, dy: int) -> Tuple[int, int]:
        """Canonical exact-integer slope key for the vector (dx, dy)."""
        if dx == 0:            # vertical line (reduced slopes never have dx == 0)
            return (0, 1)
        if dy == 0:            # horizontal line (reduced slopes never have dy == 0)
            return (1, 0)
        g = gcd(dx, dy)
        dx //= g
        dy //= g
        if dx < 0:             # force a consistent sign so equal slopes match
            dx, dy = -dx, -dy
        return (dx, dy)


# ---------------------------------------------------------------------------
# Brute-force reference (O(n^3)) used only to cross-check the fast solution.
# ---------------------------------------------------------------------------
def _brute_max_points(points: List[List[int]]) -> int:
    n = len(points)
    if n <= 2:
        return n
    best = 1
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            count = 2
            for k in range(n):
                if k == i or k == j:
                    continue
                x3, y3 = points[k]
                # Collinear iff cross product is zero (exact integer test).
                if (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) == 0:
                    count += 1
            best = max(best, count)
    return best


if __name__ == "__main__":
    sol = Solution()

    # Examples
    assert sol.maxPoints([[1, 1], [2, 2], [3, 3]]) == 3
    assert sol.maxPoints([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]) == 4

    # Edge cases
    assert sol.maxPoints([[0, 0]]) == 1
    assert sol.maxPoints([[0, 0], [1, 1]]) == 2

    # Vertical line
    assert sol.maxPoints([[1, 1], [1, 2], [1, 3], [2, 5]]) == 3
    # Horizontal line
    assert sol.maxPoints([[1, 4], [2, 4], [3, 4], [3, 9]]) == 3
    # Negative coordinates, steep negative slope
    assert sol.maxPoints([[-1, -1], [-2, -2], [-3, -3], [0, 1]]) == 3
    # Two separate lines; the bigger one wins
    assert sol.maxPoints([[0, 0], [1, 1], [2, 2], [3, 3], [0, 5], [1, 5]]) == 4

    # Duplicate-free stress check against brute force
    import random
    random.seed(7)
    for _ in range(300):
        m = random.randint(1, 8)
        pts = set()
        while len(pts) < m:
            pts.add((random.randint(-4, 4), random.randint(-4, 4)))
        pts = [list(p) for p in pts]
        assert sol.maxPoints([p[:] for p in pts]) == _brute_max_points(pts), pts

    print("All tests passed for 149. Max Points on a Line")
