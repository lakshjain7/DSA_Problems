"""
135. Candy
Difficulty: Hard
Topics: Array, Greedy

Problem Statement
-----------------
There are n children standing in a line. Each child is assigned a rating value
given in the integer array ratings.

You are giving candies to these children subjected to the following
requirements:
    - Each child must have at least one candy.
    - Children with a higher rating get more candies than their neighbors.

Return the minimum number of candies you need to have to distribute the candies
to the children.

Example 1:
    Input:  ratings = [1,0,2]
    Output: 5
    Explanation: You can allocate to the first, second and third child with
                 2, 1, 2 candies respectively.

Example 2:
    Input:  ratings = [1,2,2]
    Output: 4
    Explanation: You can allocate to the first, second and third child with
                 1, 2, 1 candies respectively. The third child gets 1 candy
                 because it satisfies the two conditions above.

Constraints:
    - n == ratings.length
    - 1 <= n <= 2 * 10^4
    - 0 <= ratings[i] <= 2 * 10^4

Approach (Two passes, O(n) time, O(n) space)
--------------------------------------------
The higher-rating-than-neighbor rule has two directions. Handle them separately:

Left-to-right pass: if ratings[i] > ratings[i-1], child i must have more candies
than child i-1, so candies[i] = candies[i-1] + 1. This satisfies every "greater
than left neighbor" constraint.

Right-to-left pass: if ratings[i] > ratings[i+1], child i must have more than
child i+1, so candies[i] = max(candies[i], candies[i+1] + 1). Taking the max
preserves the constraint already satisfied from the left pass.

After both passes every local constraint holds and each value is as small as
possible, so the sum is the minimum total. Every child starts with 1, honoring
the "at least one candy" rule.

Alternative (O(1) extra space): a single scan that tracks the lengths of the
current increasing and decreasing runs (slope method), adding candies based on
run lengths. Included below as SolutionOnePass.

Complexity
----------
Two-pass:  Time O(n), Space O(n).
One-pass:  Time O(n), Space O(1).
"""

from __future__ import annotations

from typing import List


class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        if n == 0:
            return 0
        candies = [1] * n

        # Left-to-right: satisfy "greater than left neighbor".
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        # Right-to-left: satisfy "greater than right neighbor" without breaking
        # the left constraint (take the max).
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)

        return sum(candies)


class SolutionOnePass:
    """O(1) extra space using the increasing/decreasing slope technique."""

    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        if n <= 1:
            return n

        total = 1          # first child gets 1
        up = down = 0      # lengths of current increasing / decreasing runs
        peak = 0           # candies given at the last peak

        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                up += 1
                down = 0
                peak = up + 1
                total += peak
            elif ratings[i] == ratings[i - 1]:
                up = down = peak = 0
                total += 1
            else:
                up = 0
                down += 1
                # If the descending run outgrows the peak, the peak needs a
                # bump too, accounted for by adding 1 when down >= peak.
                total += down + (1 if down >= peak else 0)

        return total


if __name__ == "__main__":
    for SolClass in (Solution, SolutionOnePass):
        sol = SolClass()

        # Provided examples
        assert sol.candy([1, 0, 2]) == 5, SolClass.__name__
        assert sol.candy([1, 2, 2]) == 4, SolClass.__name__

        # Single child
        assert sol.candy([5]) == 1, SolClass.__name__

        # All equal -> everyone gets 1
        assert sol.candy([3, 3, 3, 3]) == 4, SolClass.__name__

        # Strictly increasing -> 1+2+3+4+5
        assert sol.candy([1, 2, 3, 4, 5]) == 15, SolClass.__name__

        # Strictly decreasing -> 5+4+3+2+1
        assert sol.candy([5, 4, 3, 2, 1]) == 15, SolClass.__name__

        # Valley then plateau
        assert sol.candy([1, 3, 2, 2, 1]) == 7, SolClass.__name__

        # Long descent after a peak (checks peak bump logic)
        assert sol.candy([1, 2, 3, 1, 0]) == 9, SolClass.__name__

        # Two children ascending / descending
        assert sol.candy([1, 2]) == 3, SolClass.__name__
        assert sol.candy([2, 1]) == 3, SolClass.__name__

    # Cross-check the two implementations agree on random inputs.
    import random
    for _ in range(2000):
        arr = [random.randint(0, 5) for _ in range(random.randint(1, 12))]
        assert Solution().candy(arr) == SolutionOnePass().candy(arr), arr

    print("All tests passed for 135. Candy")
