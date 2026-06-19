"""
Finds the shortest path in a binary matrix from the top-left to the bottom-right cell.
Uses Breadth-First Search (BFS) to traverse the matrix, considering 8 possible directions (including diagonals).
Cells with value 0 are open, and cells with value 1 are blocked.
Returns the length of the shortest path if one exists, otherwise returns -1.
Args:
    arr (List[List[int]]): A square binary matrix where 0 represents open cells and 1 represents blocked cells.
Returns:
    int: The length of the shortest path from (0, 0) to (n-1, n-1), or -1 if no such path exists.
"""

from collections import deque
from typing import List
class Solution:
    def shortestPathBinaryMatrix(self, arr: List[List[int]]) -> int:
        dir = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
        n = len(arr)
        if(arr[0][0]==1 or arr[n-1][n-1]==1):
            return -1
        q=deque([(0,0,1)])
        visited=set()
        visited.add((0,0))
        while q:
            r,c,d = q.popleft()
            if(r==n-1 and c==n-1):
                return d
            for dr,dc in dir:
                nr,nc = r+dr,c+dc
                if(0<=nr<n and 0<=nc<n and arr[nr][nc]==0):
                    if((nr,nc) not in visited):
                        q.append((nr,nc,d+1))
                        visited.add((nr,nc))
        return -1

