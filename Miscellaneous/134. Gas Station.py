"""
134. Gas Station
Difficulty: Medium
Topics: Array, Greedy

Problem:
There are n gas stations along a circular route, where the amount of gas at the
i-th station is gas[i]. You have a car with an unlimited gas tank and it costs
cost[i] of gas to travel from the i-th station to its next (i + 1)-th station.
You begin the journey with an empty tank at one of the gas stations.

Given two integer arrays gas and cost, return the starting gas station's index
if you can travel around the circuit once in the clockwise direction, otherwise
return -1. If there exists a solution, it is guaranteed to be unique.

Example 1:
    Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
    Output: 3
Example 2:
    Input: gas = [2,3,4], cost = [3,4,3]
    Output: -1

Constraints:
    n == gas.length == cost.length
    1 <= n <= 10^5
    0 <= gas[i], cost[i] <= 10^4

Approach (one-pass greedy):
- If sum(gas) < sum(cost), no start works -> -1.
- Otherwise a start exists. Scan, keeping the running tank. If the tank goes
  negative at station i, no station in [start, i] can be a valid start (each
  prefix of a failing run has a non-negative tank on arrival, so starting later
  inside the run only has less gas). So reset start = i + 1 and tank = 0.
- The surviving start is the answer because total surplus is >= 0.

Complexity: Time O(n), Space O(1).
"""
from typing import List


def can_complete_circuit(gas: List[int], cost: List[int]) -> int:
    total = tank = start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total += diff
        tank += diff
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1


# Alternative: brute-force simulation from every start. O(n^2) time, O(1) space.
def can_complete_circuit_brute(gas: List[int], cost: List[int]) -> int:
    n = len(gas)
    for s in range(n):
        tank = 0
        ok = True
        for k in range(n):
            j = (s + k) % n
            tank += gas[j] - cost[j]
            if tank < 0:
                ok = False
                break
        if ok:
            return s
    return -1


if __name__ == "__main__":
    import random

    for f in (can_complete_circuit, can_complete_circuit_brute):
        assert f([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
        assert f([2, 3, 4], [3, 4, 3]) == -1
        assert f([5], [4]) == 0
        assert f([4], [5]) == -1
        assert f([0], [0]) == 0
        assert f([3, 1, 1], [1, 2, 2]) == 0
        assert f([2, 0, 0, 5], [1, 3, 3, 0]) == 3

    random.seed(1)
    for _ in range(500):
        n = random.randint(1, 8)
        g = [random.randint(0, 6) for _ in range(n)]
        c = [random.randint(0, 6) for _ in range(n)]
        a, b = can_complete_circuit(g, c), can_complete_circuit_brute(g, c)
        # Solution is unique when it exists only if tank never ties; compare validity
        assert (a == -1) == (b == -1), (g, c, a, b)
    print("All tests passed.")
