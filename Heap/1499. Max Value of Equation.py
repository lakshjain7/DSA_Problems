"""
1499. Max Value of Equation
Difficulty: Hard
Topics: Array, Queue, Sliding Window, Heap (Priority Queue), Monotonic Queue

Problem:
You are given an array points containing the coordinates of points on a 2D
plane, sorted by the x-values, where points[i] = [xi, yi] such that
xi < xj for all 1 <= i < j <= points.length. You are also given an integer k.

Return the maximum value of the equation yi + yj + |xi - xj| where
|xi - xj| <= k and 1 <= i < j <= points.length.

It is guaranteed that there exists at least one pair of points that satisfy
the constraint |xi - xj| <= k.

Example 1:
    Input: points = [[1,3],[2,0],[5,10],[6,-10]], k = 1
    Output: 4
    Explanation: The first two points satisfy |xi - xj| <= 1 giving
    3 + 0 + |1 - 2| = 4. The third and fourth also qualify giving
    10 + -10 + |5 - 6| = 1. No other pairs qualify, so the answer is 4.

Example 2:
    Input: points = [[0,0],[3,0],[9,2]], k = 3
    Output: 3
    Explanation: Only the first two points qualify: 0 + 0 + |0 - 3| = 3.

Constraints:
    2 <= points.length <= 10^5
    points[i].length == 2
    -10^8 <= xi, yi <= 10^8
    0 <= k <= 2 * 10^8
    xi < xj for all 1 <= i < j <= points.length
    xi form a strictly increasing sequence.

Approach (monotonic deque over a sliding x-window):
    Since x is strictly increasing and i < j, |xi - xj| = xj - xi, so
        yi + yj + xj - xi = (xj + yj) + (yi - xi).
    For each j we want the maximum (yi - xi) among earlier points with
    xj - xi <= k. That is a "sliding window maximum" where the window is
    defined by x-distance rather than index count.

    Keep a deque of (yi - xi, xi), with values strictly decreasing from front
    to back:
      1. Pop from the front while xj - front.x > k (out of range forever,
         because later j only have larger x).
      2. If non-empty, the front is the best partner: update the answer.
      3. Push (yj - xj, xj) at the back, first popping any back entries with
         value <= yj - xj - they are older AND no better, so they can never
         be the answer for any future j.

Complexity:
    Time:  O(n)  - each point enters and leaves the deque at most once.
    Space: O(n)  - deque in the worst case.

Alternative (max-heap with lazy deletion):
    Push (-(yi - xi), xi) into a heap; for each j, pop the top while its x is
    out of range, then use it. O(n log n) time, O(n) space - simpler to
    reason about but slower than the deque.
"""

import heapq
from collections import deque
from typing import List


def findMaxValueOfEquation(points: List[List[int]], k: int) -> int:
    dq: deque = deque()  # (y - x, x), values strictly decreasing
    best = float("-inf")
    for x, y in points:
        while dq and x - dq[0][1] > k:
            dq.popleft()
        if dq:
            best = max(best, x + y + dq[0][0])
        val = y - x
        while dq and dq[-1][0] <= val:
            dq.pop()
        dq.append((val, x))
    return best


def findMaxValueOfEquation_heap(points: List[List[int]], k: int) -> int:
    heap: List[tuple] = []  # (-(y - x), x)
    best = float("-inf")
    for x, y in points:
        while heap and x - heap[0][1] > k:
            heapq.heappop(heap)
        if heap:
            best = max(best, x + y - heap[0][0])
        heapq.heappush(heap, (-(y - x), x))
    return best


def _brute(points: List[List[int]], k: int) -> int:
    best = float("-inf")
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            xi, yi = points[i]
            xj, yj = points[j]
            if abs(xi - xj) <= k:
                best = max(best, yi + yj + abs(xi - xj))
    return best


if __name__ == "__main__":
    import random

    for fn in (findMaxValueOfEquation, findMaxValueOfEquation_heap):
        assert fn([[1, 3], [2, 0], [5, 10], [6, -10]], 1) == 4
        assert fn([[0, 0], [3, 0], [9, 2]], 3) == 3
        assert fn([[1, 1], [2, 2]], 1) == 4
        assert fn([[-19, 9], [-15, -19], [-5, -8]], 10) == -6
        assert fn([[-10**8, -10**8], [10**8, -10**8]], 2 * 10**8) == 0
        assert fn([[0, 5], [1, -100], [2, 5]], 2) == 12

    random.seed(1499)
    for _ in range(800):
        n = random.randint(2, 10)
        xs = sorted(random.sample(range(-30, 30), n))
        pts = [[x, random.randint(-20, 20)] for x in xs]
        gaps = [xs[i + 1] - xs[i] for i in range(n - 1)]
        k = random.randint(min(gaps), xs[-1] - xs[0])  # guarantees a valid pair
        exp = _brute(pts, k)
        assert findMaxValueOfEquation(pts, k) == exp, (pts, k)
        assert findMaxValueOfEquation_heap(pts, k) == exp, (pts, k)

    print("All tests passed for 1499. Max Value of Equation")
