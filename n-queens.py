def n_queens(n):
    """Solve N-Queens problem using backtracking, print coordinates and all solutions."""
    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
        return True

    def solve(board, row):
        if row == n:
            # Format solution as list of coordinates (row, col)
            solution = [(r, board[r]) for r in range(n)]
            solutions.append(solution)
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solve(board, row + 1)
                board[row] = -1  # Reset for backtracking

    solutions = []
    solve([-1] * n, 0)

    if not solutions:
        print(f"No solutions for {n}-Queens problem.")
    else:
        print(f"Number of solutions for {n}-Queens: {len(solutions)}")
        for idx, sol in enumerate(solutions, 1):
            print(f"\nSolution {idx}:")
            for coord in sol:
                print(f"Queen at row {coord[0]}, column {coord[1]}")

    return solutions

# Example usage:
n_queens(4)
