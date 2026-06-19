"""
739. Daily Temperatures
Difficulty: Medium
Topics: Array, Stack, Monotonic Stack

Given temperatures array, return answer[i] = days to wait for warmer temperature.

Approach: Monotonic Decreasing Stack — O(n) time, O(n) space
Alternative: Backwards scan with answer-jumping
"""

from typing import List


def daily_temperatures(temperatures: List[int]) -> List[int]:
    n = len(temperatures)
    answer = [0] * n
    stack: List[int] = []
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer


def daily_temperatures_backwards(temperatures: List[int]) -> List[int]:
    n = len(temperatures)
    answer = [0] * n
    for i in range(n - 2, -1, -1):
        j = i + 1
        while j < n and temperatures[j] <= temperatures[i]:
            if answer[j] == 0:
                j = n
            else:
                j += answer[j]
        if j < n:
            answer[i] = j - i
    return answer


if __name__ == "__main__":
    for solve in (daily_temperatures, daily_temperatures_backwards):
        assert solve([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
        assert solve([30, 40, 50, 60]) == [1, 1, 1, 0]
        assert solve([30, 60, 90]) == [1, 1, 0]
        assert solve([50]) == [0]
        assert solve([90, 80, 70, 60]) == [0, 0, 0, 0]
        assert solve([70, 70, 70]) == [0, 0, 0]
        assert solve([30, 100]) == [1, 0]
        assert solve([55, 38, 53, 81, 61, 93, 97, 32, 43, 78]) == [3, 1, 1, 2, 1, 1, 0, 1, 1, 0]
    print("All tests passed for 739. Daily Temperatures")
