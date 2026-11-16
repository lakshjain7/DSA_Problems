"""
1383. Maximum Performance of a Team
Difficulty: Hard
Topics: Array, Greedy, Sorting, Heap (Priority Queue)

Problem
-------
You are given two integers `n` and `k` and two integer arrays `speed` and
`efficiency` both of length n. There are n engineers numbered from 1 to n.
speed[i] and efficiency[i] represent the speed and efficiency of the i-th
engineer respectively.

Choose at most k different engineers out of the n engineers to form a team
with the maximum performance.

The performance of a team is the sum of its engineers' speeds multiplied by
the minimum efficiency among its engineers.

Return the maximum performance of this team. Since the answer can be a huge
number, return it modulo 10^9 + 7.

Example 1:
    Input: n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 2
    Output: 60
    Explanation: Pick engineer 2 (speed=10, efficiency=4) and engineer 5
    (speed=5, efficiency=7). Performance = (10 + 5) * min(4, 7) = 60.

Example 2:
    Input: n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 3
    Output: 68
    Explanation: Same as example 1 but also pick engineer 1. Performance =
    (2 + 10 + 5) * min(5, 4, 7) = 68.

Example 3:
    Input: n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 4
    Output: 72

Constraints:
    1 <= k <= n <= 10^5
    speed.length == n
    efficiency.length == n
    1 <= speed[i] <= 10^5
    1 <= efficiency[i] <= 10^8

Approach (fix the minimum efficiency + min-heap of speeds)
----------------------------------------------------------
Every team has some member whose efficiency is the minimum. Sort engineers by
efficiency descending and sweep. When we reach engineer i with efficiency e,
treat e as the team's minimum: every engineer seen so far has efficiency >= e,
so any of them may join without lowering the minimum. To maximise the product
we want the largest total speed among at most k of them (including i).

Maintain a min-heap of the speeds chosen so far plus their running sum. Push
the current speed; if the heap exceeds k, pop the smallest speed. Then
candidate = speed_sum * e. Taking the max over all i covers every possible
"minimum-efficiency member", so the optimum is found.

Why including engineer i is fine even if i's speed is popped: then the heap
holds k engineers with efficiency >= e, whose true minimum is >= e, and that
team was (or will be) evaluated with a min efficiency >= e as well -- the
candidate is a lower bound of a real team's performance, never an overestimate.

Important: take the max on the raw integer, and apply the modulo only at the
end (taking the modulo inside the max would compare wrong values).

Complexity
----------
Time:  O(n log n) for sorting + O(n log k) for heap operations.
Space: O(n) for the sorted pairs, O(k) for the heap.

Alternative
-----------
Brute force over all subsets of size <= k -- O(2^n) -- used below as a test
oracle. A sorted-list variant (keeping the top-k speeds in a balanced BST)
works too but the heap is simpler and strictly sufficient.
"""

import heapq
from typing import List

MOD = 10**9 + 7


class Solution:
    def maxPerformance(self, n: int, speed: List[int], efficiency: List[int], k: int) -> int:
        engineers = sorted(zip(efficiency, speed), reverse=True)
        heap: List[int] = []
        speed_sum = 0
        best = 0
        for eff, spd in engineers:
            heapq.heappush(heap, spd)
            speed_sum += spd
            if len(heap) > k:
                speed_sum -= heapq.heappop(heap)
            best = max(best, speed_sum * eff)
        return best % MOD

    def maxPerformanceBrute(self, n: int, speed: List[int], efficiency: List[int], k: int) -> int:
        from itertools import combinations

        best = 0
        for size in range(1, k + 1):
            for team in combinations(range(n), size):
                perf = sum(speed[i] for i in team) * min(efficiency[i] for i in team)
                best = max(best, perf)
        return best % MOD


if __name__ == "__main__":
    sol = Solution()
    sp, ef = [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2]
    assert sol.maxPerformance(6, sp, ef, 2) == 60
    assert sol.maxPerformance(6, sp, ef, 3) == 68
    assert sol.maxPerformance(6, sp, ef, 4) == 72
    assert sol.maxPerformance(1, [7], [3], 1) == 21               # single engineer
    assert sol.maxPerformance(3, [1, 1, 1], [5, 5, 5], 3) == 15   # all equal efficiency
    assert sol.maxPerformance(3, [100, 1, 1], [1, 50, 50], 1) == 100  # speed beats efficiency
    assert sol.maxPerformance(3, [1, 1, 100], [100, 100, 1], 3) == 200

    # modulo applied after max: large values
    n = 10**5
    big = sol.maxPerformance(n, [10**5] * n, [10**8] * n, n)
    assert big == (10**5 * n * 10**8) % MOD

    import random

    random.seed(1383)
    for _ in range(300):
        n = random.randint(1, 8)
        k = random.randint(1, n)
        sp = [random.randint(1, 20) for _ in range(n)]
        ef = [random.randint(1, 20) for _ in range(n)]
        assert sol.maxPerformance(n, sp, ef, k) == sol.maxPerformanceBrute(n, sp, ef, k), (sp, ef, k)
    print("All tests passed for 1383. Maximum Performance of a Team")
