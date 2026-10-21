"""
765. Couples Holding Hands
Difficulty: Hard
Topics: Greedy, Depth-First Search, Breadth-First Search, Union Find, Graph

Problem:
There are n couples sitting in 2n seats arranged in a row and want to hold
hands. The people and seats are represented by an integer array row where
row[i] is the ID of the person sitting in the i-th seat. The couples are
numbered in order: the first couple is (0, 1), the second is (2, 3), ..., and
the last is (2n - 2, 2n - 1). Return the minimum number of swaps so that every
couple is sitting side by side. A swap consists of choosing any two people,
then they stand up and switch seats.

Examples:
  Input: row = [0,2,1,3] -> 1
  Input: row = [3,2,0,1] -> 0

Constraints:
  2n == row.length
  2 <= n <= 30
  0 <= row[i] < 2n
  All the elements of row are unique.

Approach (union-find on couples):
  Treat each couple ID (person // 2) as a node. Each pair of adjacent seats
  (2i, 2i+1) links the two couples sitting there. Every node has degree 2, so
  the graph splits into cycles. A cycle containing c couples needs exactly
  c - 1 swaps (each swap fixes one couple and shrinks the cycle by one), so
  the total is n - (number of connected components).

Complexity:
  Time:  O(n * alpha(n))
  Space: O(n)
"""
from typing import List


def min_swaps_couples(row: List[int]) -> int:
    n = len(row) // 2
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    components = n
    for i in range(0, len(row), 2):
        a, b = find(row[i] // 2), find(row[i + 1] // 2)
        if a != b:
            parent[a] = b
            components -= 1
    return n - components


def min_swaps_couples_greedy(row: List[int]) -> int:
    """Alternative: greedy, fix each seat pair by swapping the partner in."""
    row = row[:]
    pos = {p: i for i, p in enumerate(row)}
    swaps = 0
    for i in range(0, len(row), 2):
        partner = row[i] ^ 1
        if row[i + 1] != partner:
            j = pos[partner]
            other = row[i + 1]
            row[i + 1], row[j] = partner, other
            pos[partner], pos[other] = i + 1, j
            swaps += 1
    return swaps


if __name__ == "__main__":
    import random

    assert min_swaps_couples([0, 2, 1, 3]) == 1
    assert min_swaps_couples([3, 2, 0, 1]) == 0
    assert min_swaps_couples([0, 1]) == 0
    assert min_swaps_couples([1, 0]) == 0
    assert min_swaps_couples([0, 2, 4, 6, 7, 1, 3, 5]) == 3
    assert min_swaps_couples([5, 4, 2, 6, 3, 1, 0, 7]) == 2
    random.seed(3)
    for _ in range(1000):
        n = random.randint(1, 30)
        r = list(range(2 * n))
        random.shuffle(r)
        assert min_swaps_couples(r) == min_swaps_couples_greedy(r), r
    print("All tests passed.")
