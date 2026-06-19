

from collections import deque
from typing import List
class Solution:
    """
    Finds the minimum effort required to travel from the top-left to the bottom-right cell in a 2D grid.
    Each cell in the grid has a height value. The effort of a path is defined as the maximum absolute difference in heights between two consecutive cells along the path. The function computes the minimum possible effort required to reach the bottom-right cell from the top-left cell.
    Args:
        arr (List[List[int]]): A 2D grid of integers representing the heights of each cell.
    Returns:
        int: The minimum effort required to reach the bottom-right cell.
    """
    def minimumEffortPath(self, arr: List[List[int]]) -> int:
        rows, cols = len(arr), len(arr[0])
        dirs = [(0,1),(1,0),(-1,0),(0,-1)]

        # store the minimum effort to reach each cell
        effort = [[float('inf')] * cols for _ in range(rows)]
        effort[0][0] = 0

        q = deque([(0, 0, 0)])  # (r, c, effort_so_far)

        while q:
            r, c, mf = q.popleft()
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    new_effort = max(mf, abs(arr[nr][nc] - arr[r][c]))
                    if new_effort < effort[nr][nc]:
                        effort[nr][nc] = new_effort
                        q.append((nr, nc, new_effort))

        return int(effort[rows-1][cols-1])
