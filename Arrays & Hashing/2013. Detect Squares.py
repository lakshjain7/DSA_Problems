"""
2013. Detect Squares
Difficulty: Medium
Topics: Array, Hash Table, Design, Counting

Problem:
You are given a stream of points on the X-Y plane. Design an algorithm that:
  - Adds new points from the stream into a data structure. Duplicate points are
    allowed and should be treated as different points.
  - Given a query point, counts the number of ways to choose three points from
    the data structure such that the three points and the query point form an
    axis-aligned square with positive area.

An axis-aligned square is a square whose edges are all the same length and are
either parallel or perpendicular to the x-axis and y-axis.

Implement the DetectSquares class:
  - DetectSquares() Initializes the object with an empty data structure.
  - void add(int[] point) Adds a new point point = [x, y] to the data structure.
  - int count(int[] point) Counts the number of ways to form axis-aligned
    squares with point point = [x, y] as described above.

Example 1:
  Input:
    ["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
    [[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]
  Output:
    [null, null, null, null, 1, 0, null, 2]
  Explanation:
    count([11, 10]) -> 1 using [3,10], [11,2], [3,2]
    count([14, 8])  -> 0
    After adding a duplicate [11, 2], count([11, 10]) -> 2

Constraints:
  - point.length == 2
  - 0 <= x, y <= 1000
  - At most 3000 calls in total will be made to add and count.

Approach (diagonal enumeration with a point counter):
  Keep a Counter of (x, y) -> multiplicity, plus a list of distinct points.
  For a query (qx, qy), any valid square has a point diagonally opposite the
  query: (px, py) with |px - qx| == |py - qy| != 0. Enumerate every stored
  distinct point as the diagonal candidate; if it qualifies, the other two
  corners are fixed: (qx, py) and (px, qy). The number of squares contributed
  is cnt[diag] * cnt[(qx, py)] * cnt[(px, qy)] — multiplicities multiply
  because duplicate points are distinct choices.
  Every square is counted exactly once, because its diagonal corner is unique.

Complexity:
  add:   O(1) time.
  count: O(D) time, D = number of distinct points stored (<= 3000).
  Space: O(D).

Alternative approach (row index by x):
  Store, for each x, a Counter of y's. For a query, iterate over all y in column
  qx (points directly above/below the query), derive side length d = y - qy,
  and check both possible squares (to the left and to the right). This is
  O(points in the query's column) per count — often faster in practice.
"""
from collections import Counter, defaultdict
from typing import List


class DetectSquares:
    def __init__(self) -> None:
        self.cnt: Counter = Counter()
        self.points: List[tuple] = []  # distinct points

    def add(self, point: List[int]) -> None:
        p = (point[0], point[1])
        if self.cnt[p] == 0:
            self.points.append(p)
        self.cnt[p] += 1

    def count(self, point: List[int]) -> int:
        qx, qy = point
        res = 0
        for px, py in self.points:
            if abs(px - qx) != abs(py - qy) or px == qx:
                continue
            res += (self.cnt[(px, py)]
                    * self.cnt.get((qx, py), 0)
                    * self.cnt.get((px, qy), 0))
        return res


class DetectSquaresByColumn:
    """Alternative: index points by x-coordinate, enumerate the query's column."""

    def __init__(self) -> None:
        self.cols = defaultdict(Counter)  # x -> Counter of y

    def add(self, point: List[int]) -> None:
        self.cols[point[0]][point[1]] += 1

    def count(self, point: List[int]) -> int:
        qx, qy = point
        if qx not in self.cols:
            return 0
        res = 0
        for y, c in self.cols[qx].items():
            d = y - qy
            if d == 0:
                continue
            for x in (qx + d, qx - d):
                if x in self.cols:
                    col = self.cols[x]
                    res += c * col.get(y, 0) * col.get(qy, 0)
        return res


if __name__ == "__main__":
    for cls in (DetectSquares, DetectSquaresByColumn):
        ds = cls()
        ds.add([3, 10]); ds.add([11, 2]); ds.add([3, 2])
        assert ds.count([11, 10]) == 1
        assert ds.count([14, 8]) == 0
        ds.add([11, 2])
        assert ds.count([11, 10]) == 2

        # Empty structure
        e = cls()
        assert e.count([0, 0]) == 0

        # Zero-area square must not count (query point equal to stored point)
        z = cls()
        z.add([5, 5]); z.add([5, 5]); z.add([5, 5])
        assert z.count([5, 5]) == 0

        # Squares on both sides of the query + duplicates multiply
        m = cls()
        for p in ([0, 1], [1, 0], [1, 1], [-1, 0], [-1, 1], [1, 1]):
            m.add(p)
        # right square: (0,1),(1,0),(1,1)x2 -> 2 ; left: (0,1),(-1,0),(-1,1) -> 1
        assert m.count([0, 0]) == 3

        # Rectangle (not square) must not count
        r = cls()
        r.add([0, 2]); r.add([3, 0]); r.add([3, 2])
        assert r.count([0, 0]) == 0

    # Randomized cross-check between both implementations
    import random
    random.seed(7)
    a, b = DetectSquares(), DetectSquaresByColumn()
    for _ in range(2000):
        p = [random.randint(0, 6), random.randint(0, 6)]
        if random.random() < 0.6:
            a.add(p); b.add(p)
        else:
            assert a.count(p) == b.count(p)
    print("All tests passed for 2013. Detect Squares")
