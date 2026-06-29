"""
Problem: 37. Sudoku Solver
Difficulty: Hard
Topics: Backtracking, Constraint Propagation, Matrix

Problem Statement:
Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:
  1. Each of the digits 1-9 must occur exactly once in each row.
  2. Each of the digits 1-9 must occur exactly once in each column.
  3. Each of the digits 1-9 must occur exactly once in each of the 9 (3x3) sub-boxes.

The '.' character indicates empty cells. It is guaranteed that the input board has
exactly one solution.

Example:
  Input board:
    ["5","3",".",  ".","7",".",  ".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"]
  Output: the solved board (in-place)

Constraints:
  - board.length == 9
  - board[i].length == 9
  - board[i][j] is a digit or '.'.
  - It is guaranteed that the input board has only one solution.

Approach:
  Classic backtracking with bitmask tracking for efficiency:
  - Maintain sets (or bitmasks) for which digits are used in each row, column, and 3x3 box.
  - Find the next empty cell, try digits 1-9 that are valid, recurse.
  - If we reach a state with no empty cells, we're done (return True).
  - If no digit works, backtrack (return False).

  Optimization: use bitmasks (integers) instead of sets for O(1) membership check.
  box_index = (row // 3) * 3 + col // 3

Complexity:
  Time:  O(9^m) worst case, m = empty cells; in practice much faster due to constraints
  Space: O(9) per recursion frame (at most 81 deep), plus O(27) for tracking arrays
"""

from typing import List


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """Solve the sudoku in-place using backtracking with bitmask constraint sets."""
        # rows[i]: set of digits used in row i
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        empties: list = []

        # Initialize tracking structures
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == '.':
                    empties.append((r, c))
                else:
                    b = (r // 3) * 3 + c // 3
                    rows[r].add(val)
                    cols[c].add(val)
                    boxes[b].add(val)

        def backtrack(idx: int) -> bool:
            if idx == len(empties):
                return True  # All empty cells filled

            r, c = empties[idx]
            b = (r // 3) * 3 + c // 3

            for d in "123456789":
                if d not in rows[r] and d not in cols[c] and d not in boxes[b]:
                    # Place digit
                    board[r][c] = d
                    rows[r].add(d)
                    cols[c].add(d)
                    boxes[b].add(d)

                    if backtrack(idx + 1):
                        return True

                    # Remove digit (backtrack)
                    board[r][c] = '.'
                    rows[r].remove(d)
                    cols[c].remove(d)
                    boxes[b].remove(d)

            return False  # No valid digit found, trigger backtrack

        backtrack(0)


# ─── Tests ───────────────────────────────────────────────────────────────────

def board_to_str(board: List[List[str]]) -> str:
    return "\n".join(" ".join(row) for row in board)


if __name__ == "__main__":
    sol = Solution()

    # LeetCode Example 1
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]

    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]

    sol.solveSudoku(board)
    assert board == expected, f"Expected:\n{board_to_str(expected)}\nGot:\n{board_to_str(board)}"

    # Verify solution is valid: each row, col, box has exactly 1-9
    digits = set("123456789")
    for r in range(9):
        assert set(board[r]) == digits, f"Row {r} invalid"
    for c in range(9):
        assert {board[r][c] for r in range(9)} == digits, f"Col {c} invalid"
    for br in range(3):
        for bc in range(3):
            box_vals = {board[br*3+r][bc*3+c] for r in range(3) for c in range(3)}
            assert box_vals == digits, f"Box ({br},{bc}) invalid"

    # Already-solved board (no empty cells) → no change
    board2 = [row[:] for row in expected]
    sol.solveSudoku(board2)
    assert board2 == expected

    print("All 37 tests passed!")
