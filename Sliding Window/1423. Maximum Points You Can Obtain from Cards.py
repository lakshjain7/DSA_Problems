"""
1423. Maximum Points You Can Obtain from Cards
Difficulty: Medium
Topics: Array, Prefix Sum, Sliding Window

Problem:
There are several cards arranged in a row, and each card has an associated
number of points. The points are given in the integer array cardPoints.

In one step, you can take one card from the beginning or from the end of the
row. You have to take exactly k cards.

Your score is the sum of the points of the cards you have taken.

Given the integer array cardPoints and the integer k, return the maximum score
you can obtain.

Example 1:
    Input: cardPoints = [1,2,3,4,5,6,1], k = 3
    Output: 12
    Explanation: Take the three cards on the right: 1 + 6 + 5 = 12.

Example 2:
    Input: cardPoints = [2,2,2], k = 2
    Output: 4

Example 3:
    Input: cardPoints = [9,7,7,9,7,7,9], k = 7
    Output: 55
    Explanation: You have to take all the cards.

Constraints:
    1 <= cardPoints.length <= 10^5
    1 <= cardPoints[i] <= 10^4
    1 <= k <= cardPoints.length

Approach (complement sliding window):
    Whatever cards we take from the two ends, the cards we LEAVE form one
    contiguous block of length n - k in the middle. Maximising the taken sum
    is therefore the same as minimising the sum of a contiguous window of
    length n - k. Slide a fixed-size window across the array, track the
    minimum window sum, and answer total - min_window.

    Why it works: every choice of (i cards from the left, k - i from the
    right) corresponds one-to-one to a window [i, i + n - k) that is left
    behind, so scanning all windows covers all choices.

Complexity:
    Time:  O(n)  - single pass over the array.
    Space: O(1)  - a few running sums.

Alternative (direct rotation):
    Start by taking all k cards from the left; then repeatedly swap the
    rightmost left card for the next card from the right end, tracking the
    best sum. Also O(k) time, O(1) space, and touches only 2k elements.
"""

from typing import List


def maxScore(cardPoints: List[int], k: int) -> int:
    n = len(cardPoints)
    window = n - k
    total = sum(cardPoints)
    if window == 0:
        return total

    cur = sum(cardPoints[:window])
    best = cur
    for i in range(window, n):
        cur += cardPoints[i] - cardPoints[i - window]
        best = min(best, cur)
    return total - best


def maxScore_rotate(cardPoints: List[int], k: int) -> int:
    """Take k from the left, then shift one card at a time to the right end."""
    cur = sum(cardPoints[:k])
    best = cur
    for i in range(1, k + 1):
        cur += cardPoints[-i] - cardPoints[k - i]
        best = max(best, cur)
    return best


def _brute(cardPoints: List[int], k: int) -> int:
    n = len(cardPoints)
    return max(sum(cardPoints[:i]) + sum(cardPoints[n - (k - i):]) for i in range(k + 1))


if __name__ == "__main__":
    import random

    for fn in (maxScore, maxScore_rotate):
        assert fn([1, 2, 3, 4, 5, 6, 1], 3) == 12
        assert fn([2, 2, 2], 2) == 4
        assert fn([9, 7, 7, 9, 7, 7, 9], 7) == 55
        assert fn([1, 1000, 1], 1) == 1
        assert fn([1, 79, 80, 1, 1, 1, 200, 1], 3) == 202
        assert fn([5], 1) == 5
        assert fn([100, 40, 17, 9, 73, 75], 3) == 248

    random.seed(1423)
    for _ in range(500):
        n = random.randint(1, 12)
        arr = [random.randint(1, 50) for _ in range(n)]
        k = random.randint(1, n)
        exp = _brute(arr, k)
        assert maxScore(arr, k) == exp
        assert maxScore_rotate(arr, k) == exp

    print("All tests passed for 1423. Maximum Points You Can Obtain from Cards")
