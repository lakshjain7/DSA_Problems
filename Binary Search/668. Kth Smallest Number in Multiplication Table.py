"""
668. Kth Smallest Number in Multiplication Table
Difficulty: Hard
Topics: Binary Search

Problem:
Nearly everyone has used the multiplication table. The multiplication table of
size m x n is an integer matrix mat where mat[i][j] == i * j (1-indexed).
Given three integers m, n, and k, return the kth smallest element in the
m x n multiplication table.

Examples:
    Input: m = 3, n = 3, k = 5   Output: 3   (table: 1 2 3 / 2 4 6 / 3 6 9)
    Input: m = 2, n = 3, k = 6   Output: 6

Constraints:
    1 <= m, n <= 3 * 10^4
    1 <= k <= m * n

Approach (binary search on the answer):
    The table is never built. For a candidate value x, the count of entries
    <= x in row i is min(n, x // i). The count function is monotonic in x,
    so binary search for the smallest x with count(x) >= k. That x is
    guaranteed to be in the table (smallest such x must be a table value).

Complexity: Time O(m * log(m*n)), Space O(1).
"""


def findKthNumber(m: int, n: int, k: int) -> int:
    if m > n:
        m, n = n, m  # iterate over the smaller dimension

    def count_le(x: int) -> int:
        return sum(min(n, x // i) for i in range(1, m + 1))

    lo, hi = 1, m * n
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


# Alternative: heap-based k-way merge of rows. O(k log m) time -- too slow for
# large k but useful as a cross-check.
def findKthNumberHeap(m: int, n: int, k: int) -> int:
    import heapq

    heap = [(i * 1, i, 1) for i in range(1, m + 1)]
    heapq.heapify(heap)
    val = 0
    for _ in range(k):
        val, i, j = heapq.heappop(heap)
        if j < n:
            heapq.heappush(heap, (i * (j + 1), i, j + 1))
    return val


if __name__ == "__main__":
    assert findKthNumber(3, 3, 5) == 3
    assert findKthNumber(2, 3, 6) == 6
    assert findKthNumber(1, 1, 1) == 1
    assert findKthNumber(1, 10, 7) == 7
    assert findKthNumber(10, 1, 10) == 10
    assert findKthNumber(30000, 30000, 30000 * 30000) == 30000 * 30000
    for m in range(1, 7):
        for n in range(1, 7):
            vals = sorted(i * j for i in range(1, m + 1) for j in range(1, n + 1))
            for k in range(1, m * n + 1):
                assert findKthNumber(m, n, k) == vals[k - 1] == findKthNumberHeap(m, n, k)
    print("All tests passed")
