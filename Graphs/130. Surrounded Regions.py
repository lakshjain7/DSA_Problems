"""
130. Surrounded Regions
Difficulty: Medium
Topics: Array, Depth-First Search, Breadth-First Search, Union Find, Matrix

Problem Statement:
------------------
You are given an m x n matrix `board` containing letters 'X' and 'O',
capture regions that are surrounded:

- Connect: A cell is connected to adjacent cells horizontally or
  vertically.
- Region: To form a region, connect every 'O' cell.
- Surround: A region is surrounded if it is not connected to any 'O'
  cell that touches the border of the `board`.

To capture a surrounded region, replace all 'O's with 'X's in-place
within that region.

Examples:
---------
Example 1:
    Input: board = [["X","X","X","X"],
                     ["X","O","O","X"],
                     ["X","X","O","X"],
                     ["X","O","X","X"]]
    Output: [["X","X","X","X"],
             ["X","X","X","X"],
             ["X","X","X","X"],
             ["X","O","X","X"]]
    Explanation: In the above diagram, the bottom region is not captured
    because it is on the border of the board and is therefore not
    surrounded.

Example 2:
    Input: board = [["X"]]
    Output: [["X"]]

Constraints:
-------------
- m == board.length
- n == board[i].length
- 1 <= m, n <= 200
- board[i][j] is 'X' or 'O'.

Approach:
---------
Approach 1 - Border-first DFS/Flood-fill (implemented as the primary
solution):
    Any 'O' that is connected (directly or transitively, via horizontal
    or vertical neighbors) to an 'O' on the border of the board can never
    be surrounded, so it must survive. Every other 'O' is surrounded and
    must become 'X'.

    1. Scan the four borders of the board. For every 'O' found on a
       border, run a DFS/BFS flood-fill marking every connected 'O' with
       a temporary sentinel (e.g. '#') so we remember "this one is safe".
    2. After all border-connected regions are marked, scan the whole
       board: any remaining 'O' was never reached from a border, so it is
       fully surrounded -> flip it to 'X'.
    3. Finally, convert every '#' sentinel back to 'O' (these are the
       safe, border-connected cells).

    This avoids the classic bug of flipping regions and then being unable
    to tell "was this always X" apart from "this was flipped" - the
    sentinel marks exactly the cells that must be restored.

Approach 2 (alternative) - Union-Find (Disjoint Set Union):
    Create a DSU over all m*n cells plus one extra virtual "border" node.
    Union every border 'O' with the virtual node, and union every pair of
    adjacent 'O' cells with each other. At the end, any 'O' cell whose
    root is NOT the virtual node's root is surrounded and gets flipped to
    'X'. This is useful when repeated/incremental connectivity queries are
    needed, though for a single pass DFS/BFS is simpler and equally
    efficient.

Complexity Analysis:
---------------------
Approach 1 (border DFS):
    Time:  O(m * n) - each cell is visited a constant number of times
           (once during border scan/flood fill, once during final sweep).
    Space: O(m * n) - worst case recursion/stack depth for the flood
           fill (an iterative stack-based DFS is used here to avoid
           Python recursion-limit issues on large boards).

Approach 2 (Union-Find):
    Time:  O(m * n * alpha(m*n)) - alpha is the inverse Ackermann
           function, effectively constant.
    Space: O(m * n) - parent/rank arrays for the DSU.
"""

from typing import List


def solve(board: List[List[str]]) -> None:
    """Capture surrounded regions in-place using border-first flood fill."""
    if not board or not board[0]:
        return

    rows, cols = len(board), len(board[0])
    SAFE = "#"

    def flood_fill(start_r: int, start_c: int) -> None:
        stack = [(start_r, start_c)]
        board[start_r][start_c] = SAFE
        while stack:
            r, c = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O":
                    board[nr][nc] = SAFE
                    stack.append((nr, nc))

    # Step 1: flood fill from every 'O' on the border.
    for r in range(rows):
        for c in (0, cols - 1):
            if board[r][c] == "O":
                flood_fill(r, c)
    for c in range(cols):
        for r in (0, rows - 1):
            if board[r][c] == "O":
                flood_fill(r, c)

    # Step 2 & 3: flip surrounded 'O's to 'X', restore safe cells to 'O'.
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == SAFE:
                board[r][c] = "O"


def solve_union_find(board: List[List[str]]) -> None:
    """Alternative approach using Union-Find with a virtual border node."""
    if not board or not board[0]:
        return

    rows, cols = len(board), len(board[0])
    border_node = rows * cols  # virtual node representing "connected to border"
    parent = list(range(rows * cols + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    def index(r: int, c: int) -> int:
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != "O":
                continue
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                union(index(r, c), border_node)
            for dr, dc in ((1, 0), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O":
                    union(index(r, c), index(nr, nc))

    border_root = find(border_node)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O" and find(index(r, c)) != border_root:
                board[r][c] = "X"


if __name__ == "__main__":
    # Example 1
    board1 = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"],
    ]
    expected1 = [
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "O", "X", "X"],
    ]
    solve(board1)
    assert board1 == expected1, f"Got {board1}"

    # Example 2: single cell, no 'O' present
    board2 = [["X"]]
    expected2 = [["X"]]
    solve(board2)
    assert board2 == expected2

    # Single 'O' cell on the border stays 'O'
    board3 = [["O"]]
    expected3 = [["O"]]
    solve(board3)
    assert board3 == expected3

    # Entire board is 'O' -> nothing surrounded (all touch the border in a
    # small grid, or are connected to something that does).
    board4 = [
        ["O", "O", "O"],
        ["O", "O", "O"],
        ["O", "O", "O"],
    ]
    expected4 = [
        ["O", "O", "O"],
        ["O", "O", "O"],
        ["O", "O", "O"],
    ]
    solve(board4)
    assert board4 == expected4

    # All surrounded region gets captured entirely
    board5 = [
        ["X", "X", "X"],
        ["X", "O", "X"],
        ["X", "X", "X"],
    ]
    expected5 = [
        ["X", "X", "X"],
        ["X", "X", "X"],
        ["X", "X", "X"],
    ]
    solve(board5)
    assert board5 == expected5

    # Re-run all cases through the Union-Find alternative implementation.
    board1b = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"],
    ]
    solve_union_find(board1b)
    assert board1b == expected1

    board4b = [
        ["O", "O", "O"],
        ["O", "O", "O"],
        ["O", "O", "O"],
    ]
    solve_union_find(board4b)
    assert board4b == expected4

    board5b = [
        ["X", "X", "X"],
        ["X", "O", "X"],
        ["X", "X", "X"],
    ]
    solve_union_find(board5b)
    assert board5b == expected5

    print("All tests passed!")
