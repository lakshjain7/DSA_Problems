"""
857. Minimum Cost to Hire K Workers
Difficulty: Hard
Topics: Array, Greedy, Sorting, Heap (Priority Queue)

Problem:
    There are n workers. quality[i] is the quality of the i-th worker and
    wage[i] is their minimum wage expectation. Hire exactly k workers into a
    paid group under: (1) every worker is paid in proportion to their quality
    relative to the others in the group; (2) every worker is paid at least
    their minimum wage expectation. Return the least amount of money needed
    to form a paid group. Answers within 1e-5 of the real answer are accepted.

Examples:
    Input: quality = [10,20,5], wage = [70,50,30], k = 2
    Output: 105.00000
    Input: quality = [3,1,10,10,1], wage = [4,8,2,2,7], k = 3
    Output: 30.66667

Constraints:
    n == quality.length == wage.length; 1 <= k <= n <= 10^4
    1 <= quality[i], wage[i] <= 10^4

Approach:
    Pay rate r (money per unit quality) must be >= wage[i]/quality[i] for each
    hired worker, so the group's rate is the maximum ratio in the group, and
    cost = rate * sum(quality). Sort workers by ratio ascending; when worker i
    is the one with the max ratio, every earlier worker is eligible at that
    rate, so we want the k-1 smallest qualities among them plus i's quality.
    Maintain a max-heap of qualities (size k) with its sum; once size > k pop
    the largest quality. At size k, candidate = ratio_i * sum.

Complexity:
    Time O(n log n). Space O(n).
"""
import heapq
from typing import List


def mincostToHireWorkers(quality: List[int], wage: List[int], k: int) -> float:
    workers = sorted(zip(quality, wage), key=lambda w: w[1] / w[0])
    heap: List[int] = []  # max-heap via negation
    q_sum = 0
    best = float("inf")
    for q, w in workers:
        heapq.heappush(heap, -q)
        q_sum += q
        if len(heap) > k:
            q_sum += heapq.heappop(heap)  # popped value is negative
        if len(heap) == k:
            best = min(best, q_sum * w / q)
    return best


def mincostToHireWorkers_bruteforce(quality: List[int], wage: List[int], k: int) -> float:
    """Alternative / oracle: try every group of size k (exponential)."""
    from itertools import combinations
    best = float("inf")
    for grp in combinations(range(len(quality)), k):
        rate = max(wage[i] / quality[i] for i in grp)
        best = min(best, rate * sum(quality[i] for i in grp))
    return best


if __name__ == "__main__":
    import random
    approx = lambda a, b: abs(a - b) < 1e-5
    assert approx(mincostToHireWorkers([10, 20, 5], [70, 50, 30], 2), 105.0)
    assert approx(mincostToHireWorkers([3, 1, 10, 10, 1], [4, 8, 2, 2, 7], 3), 30.66667)
    assert approx(mincostToHireWorkers([5], [10], 1), 10.0)
    assert approx(mincostToHireWorkers([1, 1, 1], [5, 5, 5], 3), 15.0)
    random.seed(7)
    for _ in range(300):
        n = random.randint(1, 8)
        k = random.randint(1, n)
        qu = [random.randint(1, 20) for _ in range(n)]
        wg = [random.randint(1, 20) for _ in range(n)]
        assert approx(mincostToHireWorkers(qu, wg, k),
                      mincostToHireWorkers_bruteforce(qu, wg, k))
    print("All tests passed.")
