"""
289. Game of Life
Difficulty: Medium
Topics: Array, Matrix, Simulation

Problem:
According to Wikipedia's article: "The Game of Life, also known simply as Life,
is a cellular automaton devised by the British mathematician John Horton Conway
in 1970."

The board is an m x n grid of cells, each with an initial state: live (1) or
dead (0). Each cell interacts with its eight neighbors (horizontal, vertical,
diagonal) using these rules:
  1. A live cell with fewer than two live neighbors dies (under-population).
  2. A live cell with two or three live neighbors lives on.
  3. A live cell with more than three live neighbors dies (over-population).
  4. A dead cell with exactly three live neighbors becomes live (reproduction).

The next state is created by applying the rules simultaneously to every cell.
Given the current board, update it in place to the next state.

Example 1:
  Input:  board = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]
  Output:        [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]

Example 2:
  Input:  board = [[1,1],[1,0]]
  Output:        [[1,1],[1,1]]

Constraints:
  m == board.length, n == board[i].length
  1 <= m, n <= 25
  board[i][j] is 0 or 1.

Follow up: solve in place; also think about an infinite board.

Approach (in-place state encoding):
  Updating in place breaks because a changed cell corrupts neighbor counts of
  cells processed later. Encode transitions with extra values so the ORIGINAL
  state is still recoverable from each cell:
      0 -> 0 : stays 0 (dead -> dead)
      1 -> 1 : stays 1 (live -> live)
      1 -> 0 : encoded as 2 (live -> dead)
      0 -> 1 : encoded as 3 (dead -> live)
  A cell was originally live iff its value is 1 or 2. After the first pass
  computes all transitions, a second pass maps 1 and 3 -> 1 and 0 and 2 -> 0.

Complexity:
  Time:  O(m * n * 8) = O(m * n)
  Space: O(1) extra (in place)

Alternative: copy the board and compute from the copy: O(m*n) extra space,
simpler but does not satisfy the in-place follow-up.
"""
from typing import List


class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """Modify board in place."""
        m, n = len(board), len(board[0])

        for i in range(m):
            for j in range(n):
                live = 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        # original liveness: 1 (stay live) or 2 (live -> dead)
                        if 0 <= ni < m and 0 <= nj < n and board[ni][nj] in (1, 2):
                            live += 1
                if board[i][j] == 1 and (live < 2 or live > 3):
                    board[i][j] = 2
                elif board[i][j] == 0 and live == 3:
                    board[i][j] = 3

        for i in range(m):
            for j in range(n):
                board[i][j] = 1 if board[i][j] in (1, 3) else 0

    def gameOfLifeCopy(self, board: List[List[int]]) -> None:
        """Alternative: O(m*n) extra space using a copy."""
        m, n = len(board), len(board[0])
        old = [row[:] for row in board]
        for i in range(m):
            for j in range(n):
                live = sum(
                    old[i + di][j + dj]
                    for di in (-1, 0, 1)
                    for dj in (-1, 0, 1)
                    if (di or dj) and 0 <= i + di < m and 0 <= j + dj < n
                )
                if old[i][j] == 1:
                    board[i][j] = 1 if live in (2, 3) else 0
                else:
                    board[i][j] = 1 if live == 3 else 0


if __name__ == "__main__":
    import random

    s = Solution()
    for fn in (s.gameOfLife, s.gameOfLifeCopy):
        b = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
        fn(b)
        assert b == [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]

        b = [[1, 1], [1, 0]]
        fn(b)
        assert b == [[1, 1], [1, 1]]

        b = [[1]]  # single cell dies
        fn(b)
        assert b == [[0]]

        b = [[0, 0], [0, 0]]  # empty stays empty
        fn(b)
        assert b == [[0, 0], [0, 0]]

        b = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]  # blinker oscillates
        fn(b)
        assert b == [[0, 0, 0], [1, 1, 1], [0, 0, 0]]

    # randomized cross-check of the two approaches
    random.seed(1)
    for _ in range(200):
        m, n = random.randint(1, 8), random.randint(1, 8)
        g = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
        a = [r[:] for r in g]
        c = [r[:] for r in g]
        s.gameOfLife(a)
        s.gameOfLifeCopy(c)
        assert a == c
    print("All tests passed!")
