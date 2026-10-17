"""
768. Max Chunks To Make Sorted II
Difficulty: Hard
Topics: Array, Stack, Greedy, Sorting, Monotonic Stack

Problem Statement:
You are given an integer array arr. We split arr into some number of chunks
(i.e., partitions), and individually sort each chunk. After concatenating them,
the result should equal the sorted array. Return the largest number of chunks
we can make to sort the array.

Example 1:
    Input: arr = [5,4,3,2,1]   Output: 1
Example 2:
    Input: arr = [2,1,3,4,4]   Output: 4
    Explanation: [2,1],[3],[4],[4]

Constraints:
- 1 <= arr.length <= 2000
- 0 <= arr[i] <= 10^8

Approach (monotonic stack):
Each stack entry is the maximum of a chunk. Maxima in the stack are
non-decreasing. For a new value x: if x >= top, it starts its own chunk. Else
it must merge with previous chunks whose max exceeds x; remember the largest
max (the first popped) and push it back as the merged chunk's max. The stack
size at the end is the number of chunks.

Complexity:
Time: O(n). Space: O(n).

Alternative approach (prefix max vs suffix min):
A cut after index i is valid iff max(arr[:i+1]) <= min(arr[i+1:]). Count the
valid cuts (the final position always counts). Time O(n), space O(n).
"""
from typing import List


class Solution:
    def maxChunksToSorted(self, arr: List[int]) -> int:
        stack: List[int] = []
        for x in arr:
            if not stack or x >= stack[-1]:
                stack.append(x)
            else:
                top = stack.pop()
                while stack and stack[-1] > x:
                    stack.pop()
                stack.append(top)
        return len(stack)

    def maxChunksToSortedPrefixSuffix(self, arr: List[int]) -> int:
        n = len(arr)
        suffix_min = [0] * (n + 1)
        suffix_min[n] = float("inf")
        for i in range(n - 1, -1, -1):
            suffix_min[i] = min(arr[i], suffix_min[i + 1])
        chunks, cur_max = 0, float("-inf")
        for i in range(n):
            cur_max = max(cur_max, arr[i])
            if cur_max <= suffix_min[i + 1]:
                chunks += 1
        return chunks


def brute(arr: List[int]) -> int:
    """Count valid cut positions via sorted comparison (reference)."""
    s = sorted(arr)
    best, start = 0, 0
    for i in range(len(arr)):
        if sorted(arr[start:i + 1]) == s[start:i + 1]:
            best += 1
            start = i + 1
    return best


if __name__ == "__main__":
    import random
    sol = Solution()
    for f in (sol.maxChunksToSorted, sol.maxChunksToSortedPrefixSuffix):
        assert f([5, 4, 3, 2, 1]) == 1
        assert f([2, 1, 3, 4, 4]) == 4
        assert f([1]) == 1
        assert f([1, 1, 1]) == 3
        assert f([1, 2, 3]) == 3
        assert f([2, 1, 3, 4, 4]) == 4
        assert f([0, 0, 1, 1, 0]) == 3
        assert f([3, 2, 1, 4, 5]) == 3
    random.seed(1)
    for _ in range(500):
        a = [random.randint(0, 5) for _ in range(random.randint(1, 9))]
        exp = brute(a)
        assert sol.maxChunksToSorted(a) == exp, a
        assert sol.maxChunksToSortedPrefixSuffix(a) == exp, a
    print("All tests passed.")
