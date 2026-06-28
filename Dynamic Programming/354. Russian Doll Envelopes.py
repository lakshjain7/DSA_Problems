"""
Problem: 354. Russian Doll Envelopes
Difficulty: Hard
Topics: Dynamic Programming, Binary Search, Sorting

Problem Statement:
    You are given a 2D array of integers envelopes where envelopes[i] = [wi, hi]
    represents the width and height of an envelope. One envelope can fit into
    another if and only if both the width and height of one envelope are strictly
    greater than the width and height of the other envelope.

    Return the maximum number of envelopes you can Russian doll (i.e., put one
    inside the other).

    Note: You cannot rotate an envelope.

Examples:
    Input: envelopes = [[5,4],[6,4],[6,7],[2,3]]
    Output: 3
    Explanation: [2,3] => [5,4] => [6,7]

    Input: envelopes = [[1,1],[1,1],[1,1]]
    Output: 1

Constraints:
    - 1 <= envelopes.length <= 10^5
    - envelopes[i].length == 2
    - 1 <= wi, hi <= 10^5

Approach (Sort + LIS with Binary Search):
    This reduces to Longest Increasing Subsequence (LIS) on heights, but with
    a crucial sorting trick to handle equal widths.

    Step 1 — Sort: Sort by width ascending. For equal widths, sort by height
    DESCENDING. This prevents using two envelopes of the same width: since
    heights are descending within the same width, the LIS algorithm can only
    pick one envelope per width group (you can never pick an increasing sequence
    from a descending subsequence).

    Step 2 — LIS on heights: Apply patience sorting (binary search on a
    "tails" array) to find LIS length in O(n log n).

    Why height descending for equal widths?
    Example: width=6 has heights [7, 4]. If we sorted ascending, LIS might
    pick both 4 and 7 (since 4 < 7), falsely suggesting two width-6 envelopes
    can nest. Descending sort prevents this — from [7, 4], LIS picks at most 1.

Complexity:
    Time:  O(n log n) — sorting + LIS with binary search
    Space: O(n) — tails array for LIS

Alternative (DP):
    dp[i] = max envelopes ending with envelope i.
    For each i, check all j < i where w[j] < w[i] and h[j] < h[i], dp[i] = max(dp[j]+1).
    Time: O(n^2) — too slow for n=10^5 but conceptually simpler.
"""

import bisect
from typing import List


def maxEnvelopes(envelopes: List[List[int]]) -> int:
    if not envelopes:
        return 0

    # Sort: width ascending, height DESCENDING for equal widths
    envelopes.sort(key=lambda x: (x[0], -x[1]))

    # LIS on heights using patience sorting (O(n log n))
    tails: List[int] = []  # tails[i] = smallest tail of all LIS of length i+1

    for _, h in envelopes:
        pos = bisect.bisect_left(tails, h)
        if pos == len(tails):
            tails.append(h)
        else:
            tails[pos] = h  # replace with smaller value to allow longer future sequences

    return len(tails)


# Alternative O(n^2) DP — for understanding
def maxEnvelopes_dp(envelopes: List[List[int]]) -> int:
    if not envelopes:
        return 0
    envelopes.sort()
    n = len(envelopes)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if envelopes[j][0] < envelopes[i][0] and envelopes[j][1] < envelopes[i][1]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


if __name__ == "__main__":
    # Problem examples
    assert maxEnvelopes([[5,4],[6,4],[6,7],[2,3]]) == 3
    assert maxEnvelopes([[1,1],[1,1],[1,1]]) == 1

    # Single envelope
    assert maxEnvelopes([[1,2]]) == 1

    # All same width — can only pick 1
    assert maxEnvelopes([[3,1],[3,2],[3,3],[3,4]]) == 1

    # All same height — can only pick 1
    assert maxEnvelopes([[1,5],[2,5],[3,5],[4,5]]) == 1

    # Strictly increasing both dimensions
    assert maxEnvelopes([[1,1],[2,2],[3,3],[4,4]]) == 4

    # Interleaved sizes
    assert maxEnvelopes([[2,100],[3,200],[4,300],[5,500],[5,400],[5,250],[6,370],[6,380]]) == 4

    # Verify DP gives same answers
    assert maxEnvelopes_dp([[5,4],[6,4],[6,7],[2,3]]) == 3
    assert maxEnvelopes_dp([[1,1],[1,1],[1,1]]) == 1
    assert maxEnvelopes_dp([[1,1],[2,2],[3,3],[4,4]]) == 4

    print("All tests passed for 354. Russian Doll Envelopes!")
