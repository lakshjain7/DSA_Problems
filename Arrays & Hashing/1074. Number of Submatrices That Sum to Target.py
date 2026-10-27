"""
1074. Number of Submatrices That Sum to Target
Difficulty: Hard
Topics: Array, Hash Table, Matrix, Prefix Sum

Problem:
Given a matrix and a target, return the number of non-empty submatrices that sum
to target. A submatrix x1, y1, x2, y2 is the set of all cells matrix[x][y] with
x1 <= x <= x2 and y1 <= y <= y2. Two submatrices are different if they have some
coordinate that is different.

Example 1:
    Input: matrix = [[0,1,0],[1,1,1],[0,1,0]], target = 0   Output: 4
Example 2:
    Input: matrix = [[1,-1],[-1,1]], target = 0             Output: 5
Example 3:
    Input: matrix = [[904]], target = 0                     Output: 0

Constraints:
- 1 <= matrix.length <= 100
- 1 <= matrix[0].length <= 100
- -1000 <= matrix[i][j] <= 1000
- -10^8 <= target <= 10^8

Approach (reduce to 1D subarray sum = K):
Fix a pair of rows (r1, r2). Collapsing columns between them into a 1D array of
column sums turns the problem into "count subarrays with sum == target", solved
with prefix sums and a hash map (as in LeetCode 560). Maintain the column sums
incrementally as r2 grows, so the work for each (r1, r2) is O(cols).

Complexity:
- Time: O(rows^2 * cols)
- Space: O(cols)

Alternative: brute force with a 2D prefix-sum table over all four corners,
O(rows^2 * cols^2); used here as a checker.
"""
from typing import List
from collections import defaultdict
import random


def numSubmatrixSumTarget(matrix: List[List[int]], target: int) -> int:
    rows, cols = len(matrix), len(matrix[0])
    ans = 0
    for r1 in range(rows):
        col_sum = [0] * cols
        for r2 in range(r1, rows):
            for c in range(cols):
                col_sum[c] += matrix[r2][c]
            seen = defaultdict(int)
            seen[0] = 1
            pref = 0
            for c in range(cols):
                pref += col_sum[c]
                ans += seen[pref - target]
                seen[pref] += 1
    return ans


def bruteForce(matrix: List[List[int]], target: int) -> int:
    R, C = len(matrix), len(matrix[0])
    P = [[0] * (C + 1) for _ in range(R + 1)]
    for i in range(R):
        for j in range(C):
            P[i + 1][j + 1] = matrix[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    cnt = 0
    for x1 in range(R):
        for x2 in range(x1, R):
            for y1 in range(C):
                for y2 in range(y1, C):
                    s = P[x2 + 1][y2 + 1] - P[x1][y2 + 1] - P[x2 + 1][y1] + P[x1][y1]
                    if s == target:
                        cnt += 1
    return cnt


if __name__ == "__main__":
    assert numSubmatrixSumTarget([[0, 1, 0], [1, 1, 1], [0, 1, 0]], 0) == 4
    assert numSubmatrixSumTarget([[1, -1], [-1, 1]], 0) == 5
    assert numSubmatrixSumTarget([[904]], 0) == 0
    assert numSubmatrixSumTarget([[904]], 904) == 1
    assert numSubmatrixSumTarget([[1, 1, 1]], 2) == 2
    random.seed(7)
    for _ in range(200):
        R, C = random.randint(1, 6), random.randint(1, 6)
        m = [[random.randint(-3, 3) for _ in range(C)] for _ in range(R)]
        t = random.randint(-4, 4)
        assert numSubmatrixSumTarget(m, t) == bruteForce(m, t), (m, t)
    print("All tests passed.")
