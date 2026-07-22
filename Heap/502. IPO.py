"""
502. IPO
Difficulty: Hard
Topics: Array, Greedy, Sorting, Heap (Priority Queue)

PROBLEM STATEMENT
-----------------
Suppose LeetCode will start its IPO soon. In order to sell a good price of its
shares to Venture Capital, LeetCode would like to work on some projects to
increase its capital before the IPO. Since it has limited resources, it can
only finish at most k distinct projects before the IPO. Help LeetCode design
the best way to maximize its total capital after finishing at most k distinct
projects.

You are given n projects where the i-th project has a pure profit profits[i]
and a minimum capital of capital[i] is needed to start it.

Initially, you have w capital. When you finish a project, you will obtain its
pure profit and the profit will be added to your total capital.

Pick a list of at most k distinct projects from given projects to maximize your
final capital, and return the final maximized capital.

The answer is guaranteed to fit in a 32-bit signed integer.

Examples
--------
Example 1:
    Input:  k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]
    Output: 4
    Explanation: Since your initial capital is 0, you can only start project 0.
                 After finishing it you will obtain profit 1 and capital becomes 1.
                 With capital 1, you can either start project 1 or project 2.
                 Since you can choose at most 2 projects, finish the most
                 profitable one (project 2) to get final capital 0+1+3 = 4.

Example 2:
    Input:  k = 3, w = 0, profits = [1,2,3], capital = [0,1,2]
    Output: 6

Constraints
-----------
- 1 <= k <= 10^5
- 0 <= w <= 10^9
- n == profits.length == capital.length
- 1 <= n <= 10^5
- 0 <= profits[i] <= 10^4
- 0 <= capital[i] <= 10^9


APPROACH  (Greedy: sort by capital + max-heap on profit)
--------------------------------------------------------
At every step we may pick any *affordable* project (capital[i] <= current w).
Because all profits are non-negative, finishing a project never reduces our
capital, so the set of affordable projects only grows over time. Given that,
the greedy choice is provably optimal: among all currently affordable projects
pick the one with the MAXIMUM profit. Doing so maximizes the capital available
for every future pick, which can only unlock more (never fewer) options.

Implementation:
1. Pair up (capital[i], profits[i]) and sort ascending by required capital.
2. Use a max-heap of profits (Python's heapq is a min-heap, so push -profit).
3. Repeat up to k times:
     - Push into the heap every project whose required capital <= w
       (advance a pointer over the sorted array; each project is added once).
     - If the heap is empty, no affordable project remains -> stop early.
     - Pop the largest profit and add it to w.
4. Return w.

Why it works:
- Sorting by capital lets us add newly-affordable projects incrementally in
  O(n) total across all iterations.
- The heap always exposes the best affordable option in O(log n).

COMPLEXITY
----------
Time:  O(n log n) -- sorting plus at most n pushes and k pops on the heap.
Space: O(n) -- the heap and the sorted pairing.
"""

import heapq
from typing import List


def findMaximizedCapital(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    """Maximize final capital after finishing at most k projects."""
    n = len(profits)
    # Sort projects by the capital required to start them.
    projects = sorted(zip(capital, profits))  # ascending by capital

    max_profit_heap: List[int] = []  # max-heap via negated profits
    i = 0  # pointer into the sorted `projects`

    for _ in range(k):
        # Add every project we can now afford.
        while i < n and projects[i][0] <= w:
            heapq.heappush(max_profit_heap, -projects[i][1])
            i += 1

        # Nothing affordable -> we can do no better.
        if not max_profit_heap:
            break

        # Take the most profitable affordable project.
        w += -heapq.heappop(max_profit_heap)

    return w


# ---------------------------------------------------------------------------
# Alternative (brute-force reference): at each of the k rounds, linearly scan
# all not-yet-used projects and take the affordable one with the highest
# profit. This is O(k*n) and only practical for small inputs, so we use it to
# validate the heap-based solution.
# ---------------------------------------------------------------------------
def findMaximizedCapital_bruteforce(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    n = len(profits)
    used = [False] * n
    for _ in range(k):
        best_idx = -1
        best_profit = -1
        for j in range(n):
            if not used[j] and capital[j] <= w and profits[j] > best_profit:
                best_profit = profits[j]
                best_idx = j
        if best_idx == -1:
            break
        used[best_idx] = True
        w += profits[best_idx]
    return w


if __name__ == "__main__":
    # Provided examples
    assert findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
    assert findMaximizedCapital(3, 0, [1, 2, 3], [0, 1, 2]) == 6

    # Edge cases
    assert findMaximizedCapital(1, 0, [5], [0]) == 5           # single affordable
    assert findMaximizedCapital(1, 0, [5], [3]) == 0           # nothing affordable
    assert findMaximizedCapital(10, 0, [1, 2, 3], [0, 1, 2]) == 6  # k exceeds n
    assert findMaximizedCapital(0, 7, [1, 2], [0, 0]) == 7     # k = 0, keep w
    assert findMaximizedCapital(2, 2, [1, 2, 3], [5, 6, 7]) == 2  # all too expensive
    assert findMaximizedCapital(3, 1, [3, 1, 2], [1, 0, 1]) == 7

    # Cross-check heap vs brute force on random inputs.
    import random
    for _ in range(3000):
        n = random.randint(1, 8)
        profits = [random.randint(0, 20) for _ in range(n)]
        capital = [random.randint(0, 20) for _ in range(n)]
        w0 = random.randint(0, 20)
        kk = random.randint(0, n + 2)
        assert findMaximizedCapital(kk, w0, profits, capital) == \
            findMaximizedCapital_bruteforce(kk, w0, profits, capital), \
            (kk, w0, profits, capital)

    print("All tests passed for 502. IPO")
