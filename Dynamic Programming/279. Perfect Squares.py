"""
279. Perfect Squares
Difficulty: Medium
Topics: Math, Dynamic Programming, Breadth-First Search

PROBLEM STATEMENT
-----------------
Given an integer n, return the least number of perfect square numbers that sum
to n.

A perfect square is an integer that is the square of an integer; in other words,
it is the product of some integer with itself. For example, 1, 4, 9, and 16 are
perfect squares while 3 and 11 are not.

Example 1:
    Input:  n = 12
    Output: 3
    Explanation: 12 = 4 + 4 + 4.

Example 2:
    Input:  n = 13
    Output: 2
    Explanation: 13 = 4 + 9.

Constraints:
    1 <= n <= 10^4

APPROACH — Bottom-Up Dynamic Programming
----------------------------------------
This is an unbounded-coin-change problem where the "coins" are the perfect
squares 1, 4, 9, 16, ... up to n. Let dp[i] be the minimum count of perfect
squares that sum to i. The recurrence is:

    dp[0] = 0
    dp[i] = 1 + min(dp[i - sq]) for every square sq <= i

We build dp from 1 up to n. For each i we try subtracting each square not larger
than i and take the best (fewest squares) result, adding 1 for the square we just
used.

WHY IT WORKS
------------
Every optimal decomposition of i must end with *some* square sq. Removing that
last square leaves i - sq, which must itself be decomposed optimally (otherwise
we could swap in a better sub-decomposition and improve i). Because we compute
all smaller subproblems before i, dp[i - sq] is already final when we need it, so
taking the minimum over all valid last squares yields the optimum for i.

COMPLEXITY
----------
    Time:  O(n * sqrt(n)) — for each of the n states we iterate over the
           O(sqrt(n)) squares that are <= i.
    Space: O(n) for the dp array.

ALTERNATIVE — BFS (shortest path in a graph of remainders)
----------------------------------------------------------
Model each integer 0..n as a node; there is an edge from x to x - sq for every
perfect square sq. The answer is the shortest path (fewest edges) from n to 0,
which BFS finds level by level. The first time we reach 0, the current level is
the minimum number of squares. This is included below as `num_squares_bfs`.

There is also a closed-form O(sqrt(n)) solution via Lagrange's four-square
theorem and Legendre's three-square theorem, provided as `num_squares_math`.
"""

from typing import List
from collections import deque
from math import isqrt


def num_squares(n: int) -> int:
    """Bottom-up dynamic programming. O(n * sqrt(n)) time, O(n) space."""
    dp: List[int] = [0] + [float("inf")] * n  # type: ignore[list-item]
    squares = []
    k = 1
    while k * k <= n:
        squares.append(k * k)
        k += 1

    for i in range(1, n + 1):
        for sq in squares:
            if sq > i:
                break
            if dp[i - sq] + 1 < dp[i]:
                dp[i] = dp[i - sq] + 1
    return dp[n]


def num_squares_bfs(n: int) -> int:
    """BFS shortest path from n down to 0. O(n * sqrt(n)) worst case."""
    squares = [k * k for k in range(1, isqrt(n) + 1)]
    visited = {n}
    queue = deque([(n, 0)])
    while queue:
        remaining, steps = queue.popleft()
        if remaining == 0:
            return steps
        for sq in squares:
            if sq > remaining:
                break
            nxt = remaining - sq
            if nxt not in visited:
                if nxt == 0:
                    return steps + 1
                visited.add(nxt)
                queue.append((nxt, steps + 1))
    return 0  # unreachable for n >= 1


def num_squares_math(n: int) -> int:
    """
    O(sqrt(n)) closed form.
    Legendre's three-square theorem: n is a sum of three squares unless it is of
    the form 4^a * (8b + 7). Combined with Lagrange's four-square theorem, the
    answer is always 1, 2, 3, or 4.
    """
    def is_square(x: int) -> bool:
        r = isqrt(x)
        return r * r == x

    if is_square(n):
        return 1

    # Check whether n is a sum of two squares.
    a = 1
    while a * a <= n:
        if is_square(n - a * a):
            return 2
        a += 1

    # Check the 4^a * (8b + 7) form -> answer is 4.
    m = n
    while m % 4 == 0:
        m //= 4
    if m % 8 == 7:
        return 4

    return 3


if __name__ == "__main__":
    # Provided examples.
    assert num_squares(12) == 3
    assert num_squares(13) == 2

    # Small edge cases.
    assert num_squares(1) == 1      # 1
    assert num_squares(2) == 2      # 1 + 1
    assert num_squares(3) == 3      # 1 + 1 + 1
    assert num_squares(4) == 1      # 4
    assert num_squares(7) == 4      # 4 + 1 + 1 + 1  (form 4^0 * (8*0 + 7))
    assert num_squares(48) == 3     # 16 + 16 + 16
    assert num_squares(100) == 1    # 10^2

    # Cross-check all three implementations agree over a range.
    for x in range(1, 1001):
        expected = num_squares(x)
        assert num_squares_bfs(x) == expected, f"BFS mismatch at {x}"
        assert num_squares_math(x) == expected, f"math mismatch at {x}"

    # Larger value within constraints.
    assert num_squares(9999) == num_squares_math(9999)

    print("All tests passed!")
