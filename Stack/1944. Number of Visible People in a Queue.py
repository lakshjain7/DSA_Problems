"""
1944. Number of Visible People in a Queue
Difficulty: Hard
Topics: Array, Stack, Monotonic Stack

Problem:
There are n people standing in a queue, numbered 0 to n - 1 from left to right.
Given an array heights of distinct integers where heights[i] is the height of
the i-th person. A person can see another person to their right if everybody
between them is shorter than both of them. More formally, the i-th person can
see the j-th person if i < j and min(heights[i], heights[j]) >
max(heights[i+1], ..., heights[j-1]).

Return an array answer of length n where answer[i] is the number of people the
i-th person can see to their right in the queue.

Example 1:
    Input: heights = [10,6,8,5,11,9]
    Output: [3,1,2,1,1,0]
Example 2:
    Input: heights = [5,1,2,3,10]
    Output: [4,1,1,1,0]

Constraints:
    n == heights.length
    1 <= n <= 10^5
    1 <= heights[i] <= 10^5
    All values of heights are unique.

Approach (monotonic stack, right to left):
Keep a stack of heights to the right that are still "visible candidates",
strictly decreasing from bottom to top (top is nearest). For person i:
- Every stack element shorter than heights[i] is visible to i; pop each and
  count it (nobody left of i can see past i to those, since i is taller).
- If the stack is non-empty afterwards, the new top is taller than i and is
  also visible (everyone between is shorter than both) -> count one more.
- Push heights[i].
Each element is pushed and popped once.

Complexity: Time O(n), Space O(n).

Alternative: brute force scanning right while tracking the running max, O(n^2).
"""
from typing import List


def can_see_persons_count(heights: List[int]) -> List[int]:
    n = len(heights)
    ans = [0] * n
    stack: List[int] = []
    for i in range(n - 1, -1, -1):
        h = heights[i]
        cnt = 0
        while stack and stack[-1] < h:
            stack.pop()
            cnt += 1
        if stack:
            cnt += 1
        ans[i] = cnt
        stack.append(h)
    return ans


def can_see_persons_count_brute(heights: List[int]) -> List[int]:
    n = len(heights)
    ans = [0] * n
    for i in range(n):
        mx = 0
        for j in range(i + 1, n):
            if min(heights[i], heights[j]) > mx:
                ans[i] += 1
            mx = max(mx, heights[j])
    return ans


if __name__ == "__main__":
    import random

    for f in (can_see_persons_count, can_see_persons_count_brute):
        assert f([10, 6, 8, 5, 11, 9]) == [3, 1, 2, 1, 1, 0]
        assert f([5, 1, 2, 3, 10]) == [4, 1, 1, 1, 0]
        assert f([1]) == [0]
        assert f([1, 2]) == [1, 0]
        assert f([2, 1]) == [1, 0]
        assert f([4, 3, 2, 1]) == [1, 1, 1, 0]
        assert f([1, 2, 3, 4]) == [1, 1, 1, 0]

    random.seed(7)
    for _ in range(500):
        n = random.randint(1, 12)
        h = random.sample(range(1, 50), n)
        assert can_see_persons_count(h) == can_see_persons_count_brute(h), h
    print("All tests passed.")
