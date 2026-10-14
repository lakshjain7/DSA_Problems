"""
363. Max Sum of Rectangle No Larger Than K
Difficulty: Hard
Topics: Array, Binary Search, Matrix, Prefix Sum, Ordered Set

Problem:
    Given an m x n matrix and an integer k, return the max sum of a rectangle
    in the matrix such that its sum is no larger than k. It is guaranteed that
    there will be a rectangle with a sum no larger than k.

Example 1:
    Input: matrix = [[1,0,1],[0,-2,3]], k = 2
    Output: 2
    Explanation: Rectangle [[0,1],[-2,3]] has sum 2.

Example 2:
    Input: matrix = [[2,2,-1]], k = 3
    Output: 3

Constraints:
    - m == matrix.length, n == matrix[i].length
    - 1 <= m, n <= 100
    - -100 <= matrix[i][j] <= 100
    - -10^5 <= k <= 10^5
    Follow up: what if the number of rows is much larger than columns?

Approach (compress rows + prefix sums + binary search):
    Fix a pair of columns (left..right) and collapse each row into the sum of
    its cells in that range, giving a 1D array. We need the max subarray sum
    <= k. With prefix sums P, a subarray sum is P[j] - P[i]; for each j we want
    the smallest P[i] >= P[j] - k among earlier prefixes. Keep earlier prefixes
    in a sorted list and use bisect_left to find it.
    Iterate over the smaller dimension for column pairs (transpose if needed),
    which handles the follow-up.

Complexity:
    Time:  O(min(m,n)^2 * max(m,n) * log(max(m,n))) (plus list insertion cost)
    Space: O(max(m,n))

Alternative (brute force with 2D prefix sums):
    Enumerate all rectangles in O(m^2 n^2) using a 2D prefix sum. Used here as
    a cross-check.
"""
from bisect import bisect_left, insort
from typing import List


class Solution:
    def maxSumSubmatrix(self, matrix: List[List[int]], k: int) -> int:
        m, n = len(matrix), len(matrix[0])
        if m < n:  # make columns the smaller dimension
            matrix = [list(r) for r in zip(*matrix)]
            m, n = n, m
        best = float("-inf")
        for left in range(n):
            row_sums = [0] * m
            for right in range(left, n):
                for i in range(m):
                    row_sums[i] += matrix[i][right]
                prefixes = [0]
                cur = 0
                for v in row_sums:
                    cur += v
                    idx = bisect_left(prefixes, cur - k)
                    if idx < len(prefixes):
                        best = max(best, cur - prefixes[idx])
                        if best == k:
                            return k
                    insort(prefixes, cur)
        return int(best)


def brute(matrix: List[List[int]], k: int) -> int:
    m, n = len(matrix), len(matrix[0])
    P = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            P[i + 1][j + 1] = matrix[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    best = float("-inf")
    for r1 in range(m):
        for r2 in range(r1, m):
            for c1 in range(n):
                for c2 in range(c1, n):
                    t = P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]
                    if t <= k:
                        best = max(best, t)
    return best


if __name__ == "__main__":
    import random

    s = Solution()
    assert s.maxSumSubmatrix([[1, 0, 1], [0, -2, 3]], 2) == 2
    assert s.maxSumSubmatrix([[2, 2, -1]], 3) == 3
    assert s.maxSumSubmatrix([[5]], 5) == 5
    assert s.maxSumSubmatrix([[-5]], -2) == -5
    assert s.maxSumSubmatrix([[2], [2], [-1]], 3) == 3  # tall matrix
    assert s.maxSumSubmatrix([[-1, -2], [-3, -4]], -1) == -1
    random.seed(7)
    for _ in range(300):
        m, n = random.randint(1, 5), random.randint(1, 5)
        mat = [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
        k = random.randint(-30, 30)
        exp = brute(mat, k)
        if exp == float("-inf"):
            continue  # problem guarantees a valid rectangle
        assert s.maxSumSubmatrix(mat, k) == exp, (mat, k)
    print("All tests passed")
