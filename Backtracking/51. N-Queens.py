"""
51. N-Queens
Difficulty: Hard
Topics: Backtracking, Recursion

PROBLEM STATEMENT
-----------------
The n-queens puzzle is the problem of placing n queens on an n x n chessboard
such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. You may
return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement,
where 'Q' and '.' both indicate a queen and an empty space, respectively.

EXAMPLES
--------
Example 1:
  Input:  n = 4
  Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
  Explanation: There exist two distinct solutions to the 4-queens puzzle.

Example 2:
  Input:  n = 1
  Output: [["Q"]]

CONSTRAINTS
-----------
  - 1 <= n <= 9

APPROACH (Backtracking with O(1) Conflict Sets)
-----------------------------------------------
Place one queen per row, choosing a column for each row. A partial placement is
valid as long as no two queens share a column or a diagonal (queens in different
rows can never share a row by construction).

Two cells (r1, c1) and (r2, c2) attack diagonally when:
  - r1 - c1 == r2 - c2  (same '\' diagonal), or
  - r1 + c1 == r2 + c2  (same '/' diagonal).

So we track three sets for O(1) conflict checks:
  - cols:     occupied columns
  - diag1:    occupied values of (row - col)   ->  the '\' diagonals
  - diag2:    occupied values of (row + col)   ->  the '/' diagonals

Algorithm (recurse over rows):
  1. If row == n, every row has a queen: record the board.
  2. For each column c in 0..n-1:
       - Skip if c in cols, or (row - c) in diag1, or (row + c) in diag2.
       - Otherwise place the queen: add to all three sets, recurse on row+1,
         then remove from the sets (backtrack) and try the next column.

We store only the chosen column per row during recursion and materialize the
'.'/'Q' string board when a full solution is found.

Why it works: exhaustively trying every non-conflicting column in every row
explores all valid placements; the conflict sets prune branches that can never
lead to a valid board, which is what makes it tractable.

COMPLEXITY
----------
  Time:  O(n!) in the worst case - the first row has n choices, the next at most
         n-1 viable columns, and so on, with O(1) pruning checks per candidate.
  Space: O(n) for the recursion stack and conflict sets (excluding the output).
         Output size is O(number_of_solutions * n).
"""

from typing import List


def solve_n_queens(n: int) -> List[List[str]]:
    """Return all distinct board configurations solving the n-queens puzzle."""
    results: List[List[str]] = []
    cols: set[int] = set()
    diag1: set[int] = set()  # row - col
    diag2: set[int] = set()  # row + col
    placement: List[int] = []  # placement[r] = column of the queen in row r

    def backtrack(row: int) -> None:
        if row == n:
            board = [
                "".join("Q" if col == placement[r] else "." for col in range(n))
                for r in range(n)
            ]
            results.append(board)
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            placement.append(col)

            backtrack(row + 1)

            placement.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return results


def _is_valid_board(board: List[str]) -> bool:
    """Independently verify a board has exactly n non-attacking queens."""
    n = len(board)
    queens = [(r, c) for r in range(n) for c in range(n) if board[r][c] == "Q"]
    if len(queens) != n:
        return False
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            (r1, c1), (r2, c2) = queens[i], queens[j]
            if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


if __name__ == "__main__":
    # Known count of distinct solutions to the n-queens puzzle for small n.
    expected_counts = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}

    for n, count in expected_counts.items():
        solutions = solve_n_queens(n)
        # Correct number of solutions
        assert len(solutions) == count, f"n={n}: expected {count}, got {len(solutions)}"
        # Every returned board is genuinely valid
        for board in solutions:
            assert len(board) == n and all(len(row) == n for row in board)
            assert _is_valid_board(board)
        # All solutions are distinct
        assert len({tuple(b) for b in solutions}) == count

    # n = 1 spot check
    assert solve_n_queens(1) == [["Q"]]

    # n = 4 spot check of the two canonical solutions
    sols4 = {tuple(b) for b in solve_n_queens(4)}
    assert (".Q..", "...Q", "Q...", "..Q.") in sols4
    assert ("..Q.", "Q...", "...Q", ".Q..") in sols4

    print("All tests passed for 51. N-Queens")
