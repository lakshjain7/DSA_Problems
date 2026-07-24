"""
904. Fruit Into Baskets
Difficulty: Medium
Topics: Array, Hash Table, Sliding Window

Problem Statement
-----------------
You are visiting a farm that has a single row of fruit trees arranged from left
to right. The trees are represented by an integer array `fruits` where
`fruits[i]` is the type of fruit the i-th tree produces.

You want to collect as much fruit as possible. However, the owner has some strict
rules that you must follow:

  - You only have two baskets, and each basket can only hold a single type of
    fruit. There is no limit on the amount of fruit each basket can hold.
  - Starting from any tree of your choice, you must pick exactly one fruit from
    every tree (including the start tree) while moving to the right. The picked
    fruits must fit in one of your baskets.
  - Once you reach a tree with fruit that cannot fit in your baskets, you must
    stop.

Given the integer array `fruits`, return the maximum number of fruits you can
pick.

In other words: find the length of the longest contiguous subarray that contains
at most two distinct values.

Examples
--------
Example 1:
    Input:  fruits = [1, 2, 1]
    Output: 3
    Explanation: We can pick from all 3 trees.

Example 2:
    Input:  fruits = [0, 1, 2, 2]
    Output: 3
    Explanation: We can pick from trees [1, 2, 2]. Starting at the first tree
                 would only allow picking [0, 1].

Example 3:
    Input:  fruits = [1, 2, 3, 2, 2]
    Output: 4
    Explanation: We can pick from trees [2, 3, 2, 2].

Constraints
-----------
  - 1 <= fruits.length <= 10^5
  - 0 <= fruits[i] < fruits.length

Approach
--------
This is the classic "longest subarray with at most K distinct elements" problem
with K = 2. We use a variable-size sliding window.

We expand the window to the right one tree at a time, tracking the count of each
fruit type currently inside the window with a hash map. Whenever the window holds
more than two distinct fruit types, we shrink it from the left — decrementing (and
removing) counts — until only two distinct types remain. After each expansion the
window is valid, so we record its length as a candidate answer.

Why it works: every valid window (at most two types) is considered, and because
the left pointer only ever moves forward, we never miss a longer valid window.
The moment adding a third type breaks validity, we advance left just enough to
restore it, which preserves the invariant "window always has <= 2 types" after
the shrink step.

Complexity
----------
Time:  O(n). Each pointer (left and right) advances at most n times.
Space: O(1). The hash map holds at most three keys at any moment.
"""

from collections import defaultdict
from typing import Dict, List


def totalFruit(fruits: List[int]) -> int:
    """Return the length of the longest subarray with at most two distinct values."""
    count: Dict[int, int] = defaultdict(int)
    left = 0
    best = 0

    for right, fruit in enumerate(fruits):
        count[fruit] += 1

        # Shrink while we have more than two distinct fruit types.
        while len(count) > 2:
            left_fruit = fruits[left]
            count[left_fruit] -= 1
            if count[left_fruit] == 0:
                del count[left_fruit]
            left += 1

        best = max(best, right - left + 1)

    return best


def totalFruit_two_var(fruits: List[int]) -> int:
    """
    Alternative: track only the two basket types and the length of the current
    run of the most recent fruit. Uses O(1) explicit variables instead of a map.

    `last` and `second_last` are the two currently-held fruit types (the two most
    recent distinct values). `run_last` is the length of the trailing block of
    consecutive `last` fruits. When a brand-new type appears, the valid window
    restarts as that trailing block plus the new fruit.
    """
    last = second_last = -1         # the two fruit types (-1 = empty)
    run_last = 0                    # length of trailing run of `last`
    cur_len = 0                     # length of current valid window
    best = 0

    for fruit in fruits:
        if fruit == last or fruit == second_last:
            cur_len += 1
        else:
            # New type: window restarts as (trailing run of `last`) + this one.
            cur_len = run_last + 1

        if fruit == last:
            run_last += 1
        else:
            run_last = 1
            second_last = last
            last = fruit

        best = max(best, cur_len)

    return best


if __name__ == "__main__":
    # Example cases
    assert totalFruit([1, 2, 1]) == 3
    assert totalFruit([0, 1, 2, 2]) == 3
    assert totalFruit([1, 2, 3, 2, 2]) == 4

    # Edge: single tree
    assert totalFruit([5]) == 1

    # Edge: all same fruit
    assert totalFruit([3, 3, 3, 3]) == 4

    # Edge: exactly two types throughout
    assert totalFruit([1, 2, 1, 2, 1, 2]) == 6

    # Edge: every tree a new type -> best window is 2
    assert totalFruit([0, 1, 2, 3, 4]) == 2

    # Longer mixed case
    assert totalFruit([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]) == 5

    # Cross-check the alternative implementation against the primary one.
    test_cases = [
        [1, 2, 1],
        [0, 1, 2, 2],
        [1, 2, 3, 2, 2],
        [5],
        [3, 3, 3, 3],
        [1, 2, 1, 2, 1, 2],
        [0, 1, 2, 3, 4],
        [3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4],
        [1, 0, 1, 4, 1, 4, 1, 2, 3],
    ]
    for tc in test_cases:
        assert totalFruit(tc) == totalFruit_two_var(tc), tc

    print("All tests passed for 904. Fruit Into Baskets")
