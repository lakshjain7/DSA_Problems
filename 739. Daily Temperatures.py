"""
739. Daily Temperatures
Difficulty: Medium
Topics: Array, Stack, Monotonic Stack

Problem Statement:
Given an array of integers `temperatures` representing the daily temperatures,
return an array `answer` such that `answer[i]` is the number of days you have
to wait after the i-th day to get a warmer temperature. If there is no future
day for which this is possible, keep `answer[i] == 0` instead.

Examples:
    Input:  temperatures = [73,74,75,71,69,72,76,73]
    Output: [1,1,4,2,1,1,0,0]

    Input:  temperatures = [30,40,50,60]
    Output: [1,1,1,0]

    Input:  temperatures = [30,60,90]
    Output: [1,1,0]

Constraints:
    1 <= temperatures.length <= 10^5
    30 <= temperatures[i] <= 100

Approach (Monotonic Decreasing Stack):
Maintain a stack of indices whose temperatures are strictly decreasing from
bottom to top. For each new day i, pop every index j on the stack whose
temperature is lower than temperatures[i] — day i is the first warmer day for
each of those, so answer[j] = i - j. Then push i. Each index is pushed and
popped at most once, so the total work is linear. The stack invariant
guarantees that anything still on the stack never saw a warmer day.

Complexity:
    Time:  O(n) — each index pushed/popped at most once.
    Space: O(n) — stack in the worst case (strictly decreasing input).

Alternative (Backwards scan, O(1) extra space besides output):
Iterate from right to left. For day i, jump through answer[] like a linked
list: start at j = i+1; while temperatures[j] <= temperatures[i] and
answer[j] > 0, jump j += answer[j]. Exploits already-computed answers to skip
runs of colder days. Worst case still O(n) amortized because jumps reuse
previous work.
"""

from typing import List


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """Monotonic stack solution."""
    n = len(temperatures)
    answer = [0] * n
    stack: List[int] = []  # indices with strictly decreasing temperatures
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer


def daily_temperatures_backwards(temperatures: List[int]) -> List[int]:
    """Alternative: right-to-left scan with answer-jumping."""
    n = len(temperatures)
    answer = [0] * n
    for i in range(n - 2, -1, -1):
        j = i + 1
        while j < n and temperatures[j] <= temperatures[i]:
            if answer[j] == 0:
                j = n  # no warmer day ahead of j, so none for i either
            else:
                j += answer[j]
        if j < n:
            answer[i] = j - i
    return answer


if __name__ == "__main__":
    for solve in (daily_temperatures, daily_temperatures_backwards):
        # Provided examples
        assert solve([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
        assert solve([30, 40, 50, 60]) == [1, 1, 1, 0]
        assert solve([30, 60, 90]) == [1, 1, 0]
        # Edge cases
        assert solve([50]) == [0]                          # single element
        assert solve([90, 80, 70, 60]) == [0, 0, 0, 0]     # strictly decreasing
        assert solve([70, 70, 70]) == [0, 0, 0]            # all equal (need strictly warmer)
        assert solve([30, 100]) == [1, 0]                  # extremes of range
        assert solve([55, 38, 53, 81, 61, 93, 97, 32, 43, 78]) == [3, 1, 1, 2, 1, 1, 0, 1, 1, 0]
    print("All tests passed for 739. Daily Temperatures")
