"""
Problem 322: Coin Change
Difficulty: Medium
Topics: Array, Dynamic Programming, Breadth-First Search

Bottom-up DP (unbounded knapsack): dp[i] = min coins for amount i.
Complexity: O(amount * len(coins)) time, O(amount) space.
"""

from typing import List
from collections import deque


def coinChange(coins: List[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


def coinChange_bfs(coins: List[int], amount: int) -> int:
    if amount == 0:
        return 0
    visited = {0}
    queue = deque([0])
    steps = 0
    while queue:
        steps += 1
        for _ in range(len(queue)):
            curr = queue.popleft()
            for coin in coins:
                nxt = curr + coin
                if nxt == amount:
                    return steps
                if nxt < amount and nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
    return -1


if __name__ == "__main__":
    assert coinChange([1, 2, 5], 11) == 3
    assert coinChange([2], 3) == -1
    assert coinChange([1], 0) == 0
    assert coinChange([1], 1) == 1
    assert coinChange([1], 2) == 2
    assert coinChange([2], 4) == 2
    assert coinChange([1, 3, 4, 5], 7) == 2
    assert coinChange([5], 10) == 2
    assert coinChange([5], 3) == -1
    assert coinChange([7], 7) == 1
    assert coinChange([1], 100) == 100
    test_cases = [([1, 2, 5], 11), ([2], 3), ([1, 3, 4, 5], 7), ([186, 419, 83, 408], 6249)]
    for coins, amount in test_cases:
        assert coinChange(coins, amount) == coinChange_bfs(coins, amount)
    print("All tests passed!")
