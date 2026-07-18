"""
36. Valid Sudoku
Difficulty: Medium
Topics: Arrays, Hash Table, Matrix

------------------------------------------------------------------------
PROBLEM STATEMENT
------------------------------------------------------------------------
Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to
be validated according to the following rules:

1. Each row must contain the digits 1-9 without repetition.
2. Each column must contain the digits 1-9 without repetition.
3. Each of the nine 3 x 3 sub-boxes of the grid must contain the digits
   1-9 without repetition.

Note:
- A Sudoku board (partially filled) could be valid but is not necessarily
  solvable.
- Only the filled cells need to be validated according to the rules above.
- Empty cells are represented by the character '.'.

------------------------------------------------------------------------
EXAMPLES
------------------------------------------------------------------------
Example 1:
Input: board =
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true

Example 2:
Input: board =
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: false
Explanation: Same as Example 1, except the top-left cell is modified from
5 to 8. Since there are two 8's in the top-left 3x3 sub-box, it is invalid.

------------------------------------------------------------------------
CONSTRAINTS
------------------------------------------------------------------------
- board.length == 9
- board[i].length == 9
- board[i][j] is a digit 1-9 or '.'.

------------------------------------------------------------------------
APPROACH
------------------------------------------------------------------------
We need to ensure no digit repeats within any row, any column, or any of
the nine 3x3 sub-boxes. We make a single pass over the 81 cells and, for
each filled cell, record the digit in three sets:

    - rows[r]      -> digits seen so far in row r
    - cols[c]      -> digits seen so far in column c
    - boxes[b]     -> digits seen so far in box b

The box index is computed as b = (r // 3) * 3 + (c // 3), which maps each
cell to exactly one of the nine 3x3 boxes.

If we ever try to insert a digit that is already present in the relevant
row / column / box set, the board is invalid and we return False.

Why it works: a valid Sudoku board (per the rules) requires all three
constraints to hold simultaneously. Sets give O(1) membership checks, so
we detect the first duplicate the instant it appears.

------------------------------------------------------------------------
COMPLEXITY
------------------------------------------------------------------------
Time:  O(1) for a fixed 9x9 board (exactly 81 cells, constant work each).
       In general terms for an n x n board it is O(n^2).
Space: O(1) for a fixed board (at most 9*9*3 entries); O(n^2) in general.
"""

from typing import List
from collections import defaultdict


def isValidSudoku(board: List[List[str]]) -> bool:
    rows = defaultdict(set)   # row index -> set of digits
    cols = defaultdict(set)   # col index -> set of digits
    boxes = defaultdict(set)  # box index -> set of digits

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == ".":
                continue
            b = (r // 3) * 3 + (c // 3)
            if val in rows[r] or val in cols[c] or val in boxes[b]:
                return False
            rows[r].add(val)
            cols[c].add(val)
            boxes[b].add(val)

    return True


# ----------------------------------------------------------------------
# ALTERNATIVE APPROACH: single set of encoded string keys
# ----------------------------------------------------------------------
# Instead of three dictionaries, encode each observation as a unique
# string and store them all in one set. If insertion finds a collision
# (i.e. the key already exists), the board is invalid.
def isValidSudoku_singleSet(board: List[List[str]]) -> bool:
    seen = set()
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == ".":
                continue
            keys = (
                f"row{r}-{val}",
                f"col{c}-{val}",
                f"box{r // 3}-{c // 3}-{val}",
            )
            for k in keys:
                if k in seen:
                    return False
                seen.add(k)
    return True


if __name__ == "__main__":
    valid_board = [
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

    invalid_board = [
        ["8", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]

    # Example 1: valid board
    assert isValidSudoku(valid_board) is True
    assert isValidSudoku_singleSet(valid_board) is True

    # Example 2: duplicate 8 in the top-left box -> invalid
    assert isValidSudoku(invalid_board) is False
    assert isValidSudoku_singleSet(invalid_board) is False

    # Edge case: completely empty board is trivially valid
    empty = [["." for _ in range(9)] for _ in range(9)]
    assert isValidSudoku(empty) is True
    assert isValidSudoku_singleSet(empty) is True

    # Edge case: duplicate within a single row
    row_dup = [["." for _ in range(9)] for _ in range(9)]
    row_dup[0][0] = "5"
    row_dup[0][8] = "5"
    assert isValidSudoku(row_dup) is False
    assert isValidSudoku_singleSet(row_dup) is False

    # Edge case: duplicate within a single column
    col_dup = [["." for _ in range(9)] for _ in range(9)]
    col_dup[0][0] = "3"
    col_dup[8][0] = "3"
    assert isValidSudoku(col_dup) is False
    assert isValidSudoku_singleSet(col_dup) is False

    # Edge case: same digit in different boxes/rows/cols is fine
    spread = [["." for _ in range(9)] for _ in range(9)]
    spread[0][0] = "1"
    spread[3][3] = "1"
    spread[6][6] = "1"
    assert isValidSudoku(spread) is True
    assert isValidSudoku_singleSet(spread) is True

    print("36. Valid Sudoku: all tests passed!")
