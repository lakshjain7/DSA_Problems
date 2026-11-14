"""
1834. Single-Threaded CPU
Difficulty: Medium
Topics: Array, Sorting, Heap (Priority Queue), Simulation

Problem:
You are given n tasks labeled from 0 to n - 1 represented by a 2D integer array
`tasks`, where tasks[i] = [enqueueTime_i, processingTime_i] means that the i-th
task will be available to process at enqueueTime_i and will take
processingTime_i to finish processing.

You have a single-threaded CPU that can process at most one task at a time and
will act in the following way:
  - If the CPU is idle and there are no available tasks to process, the CPU
    remains idle.
  - If the CPU is idle and there are available tasks, the CPU will choose the one
    with the shortest processing time. If multiple tasks have the same shortest
    processing time, it will choose the task with the smallest index.
  - Once a task is started, the CPU will process the entire task without stopping.
  - The CPU can finish a task then start a new one instantly.

Return the order in which the CPU will process the tasks.

Example 1:
    Input: tasks = [[1,2],[2,4],[3,2],[4,1]]
    Output: [0,2,3,1]
    Explanation:
      t=1: task 0 available, start it (ends at 3).
      t=3: tasks 1,2 available; task 2 shorter -> run (ends at 5).
      t=5: tasks 1,3 available; task 3 shorter -> run (ends at 6).
      t=6: run task 1 (ends at 10).

Example 2:
    Input: tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]
    Output: [4,3,2,0,1]

Constraints:
    tasks.length == n
    1 <= n <= 10^5
    1 <= enqueueTime_i, processingTime_i <= 10^9

Approach (sort by arrival + min-heap of available tasks):
    1. Sort task indices by enqueue time.
    2. Keep a clock `time` and a min-heap keyed by (processingTime, index) of tasks
       that have arrived (enqueueTime <= time).
    3. Loop: push every task that has arrived by `time`. If the heap is empty the
       CPU is idle, so jump `time` forward to the next arrival. Otherwise pop the
       best task, record it, and advance `time` by its processing time.

    Why it works: the heap always contains exactly the set of tasks the CPU is
    allowed to choose from at the current decision moment, and its ordering
    (processingTime, index) is exactly the CPU's tie-breaking rule. Jumping the
    clock when idle avoids simulating empty time units (times are up to 1e9).

Complexity:
    Time:  O(n log n) - sorting plus n heap pushes/pops.
    Space: O(n) for the sorted order and heap.

Alternative:
    Same idea but pushing (enqueueTime, processingTime, index) into a second
    "pending" heap instead of sorting - shown below as `getOrder_two_heaps`.
"""
import heapq
from typing import List


def getOrder(tasks: List[List[int]]) -> List[int]:
    order = sorted(range(len(tasks)), key=lambda i: tasks[i][0])
    res: List[int] = []
    heap: List[tuple] = []
    time = 0
    i = 0
    n = len(tasks)
    while len(res) < n:
        if not heap and i < n and tasks[order[i]][0] > time:
            time = tasks[order[i]][0]  # CPU idle: fast-forward
        while i < n and tasks[order[i]][0] <= time:
            idx = order[i]
            heapq.heappush(heap, (tasks[idx][1], idx))
            i += 1
        proc, idx = heapq.heappop(heap)
        time += proc
        res.append(idx)
    return res


def getOrder_two_heaps(tasks: List[List[int]]) -> List[int]:
    """Alternative: a pending heap by arrival time feeding a ready heap."""
    pending = [(e, p, i) for i, (e, p) in enumerate(tasks)]
    heapq.heapify(pending)
    ready: List[tuple] = []
    time = 0
    res: List[int] = []
    while pending or ready:
        if not ready and pending[0][0] > time:
            time = pending[0][0]
        while pending and pending[0][0] <= time:
            _, p, i = heapq.heappop(pending)
            heapq.heappush(ready, (p, i))
        p, i = heapq.heappop(ready)
        time += p
        res.append(i)
    return res


def _brute(tasks: List[List[int]]) -> List[int]:
    done = [False] * len(tasks)
    time, res = 0, []
    while len(res) < len(tasks):
        avail = [(p, i) for i, (e, p) in enumerate(tasks) if not done[i] and e <= time]
        if not avail:
            time = min(e for i, (e, _) in enumerate(tasks) if not done[i])
            continue
        p, i = min(avail)
        done[i] = True
        res.append(i)
        time += p
    return res


if __name__ == "__main__":
    import random

    for fn in (getOrder, getOrder_two_heaps):
        assert fn([[1, 2], [2, 4], [3, 2], [4, 1]]) == [0, 2, 3, 1]
        assert fn([[7, 10], [7, 12], [7, 5], [7, 4], [7, 2]]) == [4, 3, 2, 0, 1]
        assert fn([[5, 3]]) == [0]                                   # single task
        assert fn([[1, 1], [100, 1], [1000, 1]]) == [0, 1, 2]        # idle gaps
        assert fn([[1, 5], [1, 5], [1, 5]]) == [0, 1, 2]             # ties by index
        assert fn([[10**9, 10**9], [1, 10**9]]) == [1, 0]            # large values

    random.seed(1)
    for _ in range(300):
        t = [[random.randint(1, 20), random.randint(1, 6)] for _ in range(random.randint(1, 12))]
        expected = _brute(t)
        assert getOrder(t) == expected
        assert getOrder_two_heaps(t) == expected
    print("All tests passed!")
