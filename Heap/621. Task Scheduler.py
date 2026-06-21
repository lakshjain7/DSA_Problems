"""
Problem #621: Task Scheduler
Difficulty: Medium
Topics: Heap, Greedy, Array, Counting

Problem Statement:
    You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n.
    Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in
    any order, but there is a cooling interval of n intervals between two tasks with the same label.
    Return the minimum number of CPU intervals required to complete all the tasks.

Examples:
    Example 1:
        Input: tasks = ["A","A","A","B","B","B"], n = 2
        Output: 8
        Explanation: A -> B -> idle -> A -> B -> idle -> A -> B
                     There is at least 2 intervals between identical tasks.

    Example 2:
        Input: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2
        Output: 16
        Explanation: One of the possible solutions is:
                     A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A

    Example 3:
        Input: tasks = ["A","A","A","B","B","B"], n = 0
        Output: 6

Constraints:
    - 1 <= tasks.length <= 10^4
    - tasks[i] is an uppercase English letter.
    - 0 <= n <= 100

Approach (Greedy with Max-Heap + Cooldown Queue):
    1. Count frequency of each task.
    2. Use a max-heap (negate counts for Python's min-heap) to always process the most frequent task.
    3. Use a cooldown queue: after processing a task, if it still has remaining count, add it to
       the queue as (count - 1, available_time = current_time + n + 1).
    4. At each time step, if the heap is empty but queue has tasks not yet ready, advance time
       to the next available task (skip idles efficiently).
    5. Pop the cooldown queue into the heap when their available time is reached.

    Why greedy with max-heap works: always scheduling the most frequent task minimizes idle time
    because the most constrained task is placed as early as possible.

Complexity:
    Time:  O(t * n) in the worst case, but O(t log 26) = O(t) effectively since at most 26 tasks
    Space: O(26) = O(1) for the heap and queue

Alternative Approach (Math Formula):
    max_count = max frequency of any task
    max_count_tasks = number of tasks with that max frequency
    result = max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)

    Explanation: the most frequent task creates a "frame" of size (n+1). We fill frames with
    other tasks. If tasks fill all frames, no idle time needed -> result = len(tasks).
"""

import heapq
from collections import Counter, deque
from typing import List


def leastInterval(tasks: List[str], n: int) -> int:
    count = Counter(tasks)
    # Max-heap: negate counts
    max_heap = [-c for c in count.values()]
    heapq.heapify(max_heap)

    time = 0
    cooldown = deque()  # (remaining_count, available_at)

    while max_heap or cooldown:
        time += 1

        if max_heap:
            remaining = heapq.heappop(max_heap) + 1  # decrement (negated)
            if remaining < 0:  # still has tasks left
                cooldown.append((remaining, time + n))
        else:
            # Heap empty, skip time to next available task
            time = cooldown[0][1]

        if cooldown and cooldown[0][1] == time:
            heapq.heappush(max_heap, cooldown.popleft()[0])

    return time


def leastInterval_math(tasks: List[str], n: int) -> int:
    """O(1) math formula approach."""
    count = Counter(tasks)
    max_count = max(count.values())
    max_count_tasks = sum(1 for c in count.values() if c == max_count)
    return max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)


if __name__ == "__main__":
    # Both approaches should agree on all test cases
    def check(tasks, n, expected):
        r1 = leastInterval(tasks, n)
        r2 = leastInterval_math(tasks, n)
        assert r1 == expected, f"Heap approach: got {r1}, expected {expected}"
        assert r2 == expected, f"Math approach: got {r2}, expected {expected}"

    check(["A","A","A","B","B","B"], 2, 8)
    check(["A","A","A","A","A","A","B","C","D","E","F","G"], 2, 16)
    check(["A","A","A","B","B","B"], 0, 6)

    # No cooling needed, all unique tasks
    check(["A","B","C","D"], 2, 4)

    # Single task type with large n
    check(["A","A","A"], 2, 7)  # A -> idle -> idle -> A -> idle -> idle -> A

    # All same tasks, n=0
    check(["A","A","A"], 0, 3)

    # Large n, two task types
    check(["A","A","B","B"], 2, 5)  # A->B->idle->A->B

    # One task
    check(["A"], 10, 1)

    print("All tests passed!")
