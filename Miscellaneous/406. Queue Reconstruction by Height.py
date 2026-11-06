"""
406. Queue Reconstruction by Height
Difficulty: Medium
Topics: Array, Greedy, Sorting

Problem:
You are given an array of people, people, which are the attributes of some
people in a queue (not necessarily in order). Each people[i] = [h_i, k_i]
represents the i-th person of height h_i with exactly k_i other people in
front who have a height greater than or equal to h_i.

Reconstruct and return the queue that is represented by the input array
people. The returned queue should be formatted as an array queue, where
queue[j] = [h_j, k_j] is the attributes of the j-th person in the queue
(queue[0] is the person at the front of the queue).

Example 1:
    Input: people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
    Output: [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]

Example 2:
    Input: people = [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]
    Output: [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]

Constraints:
    1 <= people.length <= 2000
    0 <= h_i <= 10^6
    0 <= k_i < people.length
    It is guaranteed that the queue can be reconstructed.

Approach (tallest first + insert):
    Sort by height descending, and by k ascending for equal heights. Process
    people in that order and insert each at index k. When a person is
    inserted, everyone already in the list is taller or equal, so exactly k
    people must precede them -> index k. Later (shorter) people never change
    the count of >= people in front of an already placed taller person, so
    earlier placements stay valid.

Complexity: O(n^2) time (list insert shifts), O(n) space.

Alternative (shortest first, fill k-th empty slot):
    Sort by height ascending, ties by k descending. Place each person in the
    (k+1)-th still-empty slot; empty slots are exactly the positions of
    people at least as tall that have not been placed yet. O(n^2) time.
"""
from typing import List


def reconstructQueue(people: List[List[int]]) -> List[List[int]]:
    res: List[List[int]] = []
    for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
        res.insert(k, [h, k])
    return res


def reconstructQueueSlots(people: List[List[int]]) -> List[List[int]]:
    n = len(people)
    res: List[List[int]] = [None] * n  # type: ignore
    for h, k in sorted(people, key=lambda p: (p[0], -p[1])):
        cnt = -1
        for i in range(n):
            if res[i] is None:
                cnt += 1
                if cnt == k:
                    res[i] = [h, k]
                    break
    return res


if __name__ == "__main__":
    import random

    e1 = [[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]]
    e2 = [[4, 0], [5, 0], [2, 2], [3, 2], [1, 4], [6, 0]]
    for f in (reconstructQueue, reconstructQueueSlots):
        assert f([[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]) == e1
        assert f([[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]]) == e2
        assert f([[1, 0]]) == [[1, 0]]
        assert f([[3, 1], [3, 0]]) == [[3, 0], [3, 1]]
        assert f([[2, 0], [2, 1], [2, 2]]) == [[2, 0], [2, 1], [2, 2]]
    # random: build a valid queue, derive people, reconstruct
    for _ in range(300):
        n = random.randint(1, 12)
        q = [random.randint(0, 6) for _ in range(n)]
        queue = [[h, sum(1 for x in q[:i] if x >= h)] for i, h in enumerate(q)]
        shuffled = queue[:]
        random.shuffle(shuffled)
        assert reconstructQueue(shuffled) == queue
        assert reconstructQueueSlots(shuffled) == queue
    print("All tests passed")
