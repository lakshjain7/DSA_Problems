"""
909. Snakes and Ladders
Difficulty: Medium
Topics: Array, Breadth-First Search, Matrix, Graphs

Problem:
You are given an n x n integer matrix `board` where the cells are labeled from 1
to n^2 in a Boustrophedon style starting from the bottom left of the board
(i.e. board[n - 1][0]) and alternating direction each row.

You start on square 1 of the board. In each move, starting from square curr:
  - Choose a destination square next with a label in the range
    [curr + 1, min(curr + 6, n^2)]. (This simulates a standard 6-sided die roll.)
  - If next has a snake or ladder (board[r][c] != -1), you must move to the
    destination of that snake or ladder. Otherwise, you move to next.
  - The game ends when you reach square n^2.

A board square on row r and column c has a snake or ladder if board[r][c] != -1.
The destination of that snake or ladder is board[r][c]. Squares 1 and n^2 never
have a snake or ladder.

Note that you only take a snake or ladder at most once per dice roll: if the
destination of a snake or ladder is the start of another snake or ladder, you do
NOT follow the subsequent snake or ladder.

Return the least number of dice rolls required to reach square n^2. If it is not
possible to reach the square, return -1.

Example 1:
    Input: board = [[-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1],
                    [-1,35,-1,-1,13,-1],
                    [-1,-1,-1,-1,-1,-1],
                    [-1,15,-1,-1,-1,-1]]
    Output: 4
    Explanation: 1 -> 2 (ladder to 15) -> 17 (snake to 13) -> 14 (ladder to 35) -> 36.

Example 2:
    Input: board = [[-1,-1],[-1,3]]
    Output: 1

Constraints:
    n == board.length == board[i].length
    2 <= n <= 20
    board[i][j] is either -1 or in the range [1, n^2].
    The squares labeled 1 and n^2 do not have any ladders or snakes.

Approach (BFS on squares):
    Every square is a node; each roll is an unweighted edge to one of up to six
    successors (after applying at most one snake/ladder jump). The minimum number
    of rolls is therefore the shortest path in an unweighted graph -> BFS from
    square 1. First flatten the board into a 1-indexed array `jump` so that the
    Boustrophedon label -> (row, col) conversion happens once.

    Why BFS is correct: BFS explores nodes in non-decreasing distance order, so
    the first time we pop/see n^2 we've used the fewest rolls. Marking a square
    visited when enqueued guarantees each square is processed once.

Complexity:
    Time:  O(n^2) - each of the n^2 squares is enqueued at most once and has <= 6 edges.
    Space: O(n^2) for the flattened board, visited set and queue.

Alternative:
    Dijkstra with all weights 1 (works but unnecessary), or a level-by-level
    BFS (shown below) which processes one "roll" per layer.
"""
from collections import deque
from typing import List


def _flatten(board: List[List[int]]) -> List[int]:
    n = len(board)
    jump = [0] * (n * n + 1)
    label = 1
    left_to_right = True
    for r in range(n - 1, -1, -1):
        cols = range(n) if left_to_right else range(n - 1, -1, -1)
        for c in cols:
            jump[label] = board[r][c]
            label += 1
        left_to_right = not left_to_right
    return jump


def snakesAndLadders(board: List[List[int]]) -> int:
    n = len(board)
    target = n * n
    jump = _flatten(board)
    dist = [-1] * (target + 1)
    dist[1] = 0
    q = deque([1])
    while q:
        cur = q.popleft()
        if cur == target:
            return dist[cur]
        for nxt in range(cur + 1, min(cur + 6, target) + 1):
            dest = jump[nxt] if jump[nxt] != -1 else nxt
            if dist[dest] == -1:
                dist[dest] = dist[cur] + 1
                q.append(dest)
    return -1


def snakesAndLadders_levels(board: List[List[int]]) -> int:
    """Alternative: explicit level-order BFS, counting rolls per frontier."""
    n = len(board)
    target = n * n
    jump = _flatten(board)
    seen = {1}
    frontier = [1]
    rolls = 0
    while frontier:
        if target in frontier:
            return rolls
        nxt_frontier = []
        for cur in frontier:
            for nxt in range(cur + 1, min(cur + 6, target) + 1):
                dest = jump[nxt] if jump[nxt] != -1 else nxt
                if dest not in seen:
                    seen.add(dest)
                    nxt_frontier.append(dest)
        frontier = nxt_frontier
        rolls += 1
    return -1


if __name__ == "__main__":
    b1 = [[-1, -1, -1, -1, -1, -1],
          [-1, -1, -1, -1, -1, -1],
          [-1, -1, -1, -1, -1, -1],
          [-1, 35, -1, -1, 13, -1],
          [-1, -1, -1, -1, -1, -1],
          [-1, 15, -1, -1, -1, -1]]
    b2 = [[-1, -1], [-1, 3]]
    # Snakes everywhere reachable -> impossible
    b3 = [[-1, 1, 1, 1],
          [1, 1, 1, 1],
          [1, 1, 1, 1],
          [-1, 1, 1, 1]]
    b4 = [[-1, -1, -1], [-1, 9, 8], [-1, 8, 9]]  # ladder 3 -> 9 wins in one roll
    b5 = [[-1] * 3 for _ in range(3)]            # plain 3x3: 1 -> 7 -> 9
    b6 = [[1, 1, -1], [1, 1, 1], [-1, 1, 1]]     # every reachable square snakes back to 1
    for fn in (snakesAndLadders, snakesAndLadders_levels):
        assert fn(b1) == 4
        assert fn(b2) == 1
        assert fn(b3) == -1
        assert fn(b4) == 1
        assert fn(b5) == 2
        assert fn(b6) == -1
    print("All tests passed!")
