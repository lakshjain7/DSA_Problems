from typing import List


class Solution:
    """
    Determine whether a given word can be formed by a path of adjacent cells in a 2D board.
    Parameters
    ----------
    board : List[List[str]]
        2D grid of single-character strings representing the board in which to search.
    word : str
        The target word to find in the board.
    Returns
    -------
    bool
        True if the word can be constructed by sequentially adjacent cells
        (horizontally or vertically) without revisiting the same cell; False otherwise.
    Behavior
    --------
    - Uses depth-first search (DFS) with backtracking.
    - Starts DFS from every cell that matches the first character of the word.
    - From a cell, explores its four orthogonal neighbors (up, down, left, right).
    - Marks visited cells temporarily (in-place) to prevent revisiting during the
      current path and restores them when backtracking.
    - Terminates early and returns True as soon as the full word is matched.
    Complexity
    ----------
    Let m be the number of rows, n the number of columns, and L the length of the word.
    - Time complexity (worst case): O(m * n * 4^L) — each cell can be a start and the
      DFS may branch up to 4 ways for each character in the word.
    - Space complexity: O(L) for the recursion stack (plus O(1) extra space if marking visited cells in-place).
    Examples
    --------
    >>> Solution().exist([['A','B','C','E'],
    ...                   ['S','F','C','S'],
    ...                   ['A','D','E','E']], "ABCCED")
    True
    Notes
    -----
    - The search considers only horizontal and vertical neighbors; diagonal moves are not allowed.
    - The implementation temporarily modifies the board to mark visited cells but restores it before returning.
    """
    def exist(self, board: List[List[str]], word: str) -> bool:
        n = len(board[0])
        m = len(board)
        l = len(word)
        start = word[0]
        direction = [(1,0),(0,1),(-1,0),(0,-1)]
        def solve(r,c,i):
            if(i==l):
                return True
            if(r>=m or c>=n or r<0 or c<0 or board[r][c]!=word[i]):
                return False
            temp = board[r][c]
            board[r][c] = '#'
            for dr,dc in direction:
                if(solve(r+dr,c+dc,i+1)):
                    return True
            board[r][c] = temp
            return False
                
        for r in range(m):
            for c in range(n):
                if(board[r][c]==start):
                    if(solve(r,c,0)):
                        return True
        return False
