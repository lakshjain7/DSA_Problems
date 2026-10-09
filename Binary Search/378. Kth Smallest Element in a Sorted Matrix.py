"""
378. Kth Smallest Element in a Sorted Matrix
Difficulty: Medium
Topics: Array, Binary Search, Matrix, Heap (Priority Queue)

Problem:
Given an n x n matrix where each of the rows and columns is sorted in
ascending order, return the kth smallest element in the matrix.
Note that it is the kth smallest element in the sorted order, not the kth
distinct element. You must find a solution with a memory complexity better
than O(n^2).

Example 1:
    Input: matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
    Output: 13
    Explanation: The elements are [1,5,9,10,11,12,13,13,15]; the 8th is 13.

Example 2:
    Input: matrix = [[-5]], k = 1
    Output: -5

Constraints:
    n == matrix.length == matrix[i].length
    1 <= n <= 300
    -10^9 <= matrix[i][j] <= 10^9
    All rows and columns are sorted in non-decreasing order.
    1 <= k <= n^2

Approach (Binary search on the answer space):
    The answer lies in [matrix[0][0], matrix[n-1][n-1]]. For a candidate value
    mid, count how many elements are <= mid using a staircase walk from the
    bottom-left corner: if matrix[r][c] <= mid, the whole column segment above
    (r+1 elements) is <= mid, so move right; otherwise move up. This is O(n).
    The smallest mid whose count >= k is the answer (it must be an element of
    the matrix, since counts only change at matrix values).

Complexity:
    Time:  O(n * log(max - min))
    Space: O(1)

Alternative (Min-heap):
    Push the first element of each row, pop k-1 times, pushing the next element
    of the popped row. Time O(k log n), space O(n).
"""
import heapq
from typing import List


def kth_smallest(matrix: List[List[int]], k: int) -> int:
    n = len(matrix)

    def count_le(x: int) -> int:
        r, c, cnt = n - 1, 0, 0
        while r >= 0 and c < n:
            if matrix[r][c] <= x:
                cnt += r + 1
                c += 1
            else:
                r -= 1
        return cnt

    lo, hi = matrix[0][0], matrix[-1][-1]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_smallest_heap(matrix: List[List[int]], k: int) -> int:
    n = len(matrix)
    heap = [(matrix[r][0], r, 0) for r in range(n)]
    heapq.heapify(heap)
    for _ in range(k - 1):
        _, r, c = heapq.heappop(heap)
        if c + 1 < n:
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
    return heap[0][0]


if __name__ == "__main__":
    import random

    for fn in (kth_smallest, kth_smallest_heap):
        m = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
        assert fn(m, 8) == 13
        assert fn(m, 1) == 1
        assert fn(m, 9) == 15
        assert fn([[-5]], 1) == -5
        assert fn([[1, 2], [1, 3]], 2) == 1  # duplicates count separately
        assert fn([[2, 2], [2, 2]], 3) == 2
        assert fn([[-10**9, 10**9], [-10**9, 10**9]], 3) == 10**9

    # randomized cross-check against brute force
    random.seed(1)
    for _ in range(300):
        n = random.randint(1, 6)
        rows = [sorted(random.randint(-20, 20) for _ in range(n)) for _ in range(n)]
        # make columns sorted too: sort the flat list and fill diagonally-safe (row-major)
        flat = sorted(v for row in rows for v in row)
        mat = [flat[i * n:(i + 1) * n] for i in range(n)]
        k = random.randint(1, n * n)
        assert kth_smallest(mat, k) == flat[k - 1]
        assert kth_smallest_heap(mat, k) == flat[k - 1]
    print("All tests passed.")
