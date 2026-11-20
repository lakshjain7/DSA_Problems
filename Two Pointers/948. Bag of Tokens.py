"""
948. Bag of Tokens
Difficulty: Medium
Topics: Array, Two Pointers, Greedy, Sorting

Problem:
You start with an initial power of `power`, an initial score of 0, and a bag of
tokens given as an integer array `tokens`, where each tokens[i] denotes the
value of token i.

Your goal is to maximize the total score by strategically playing these tokens.
In one move, you can play an unplayed token in one of the two ways (but not
both for the same token):
  - Face-up: If your current power is at least tokens[i], you may play token i,
    losing tokens[i] power and gaining 1 score.
  - Face-down: If your current score is at least 1, you may play token i,
    gaining tokens[i] power and losing 1 score.

Return the maximum possible score you can achieve after playing any number of
tokens.

Example 1:
    Input: tokens = [100], power = 50
    Output: 0
    Explanation: Cannot play face-up (50 < 100), cannot play face-down (score 0).

Example 2:
    Input: tokens = [200,100], power = 150
    Output: 1
    Explanation: Play token 1 (100) face-up: power 50, score 1.

Example 3:
    Input: tokens = [100,200,300,400], power = 200
    Output: 2
    Explanation:
      Play 100 face-up  -> power 100, score 1
      Play 400 face-down -> power 500, score 0
      Play 200 face-up  -> power 300, score 1
      Play 300 face-up  -> power 0,   score 2

Constraints:
    0 <= tokens.length <= 1000
    0 <= tokens[i], power < 10^4

Approach (Sort + Greedy Two Pointers):
    Sort the tokens. Each face-up play costs power and earns 1 point, so it
    should always use the *cheapest* remaining token (left pointer). Each
    face-down play spends 1 point for power, so it should always use the
    *most valuable* remaining token (right pointer) to get the most power per
    point spent.

    Loop while lo <= hi:
      - If we can afford tokens[lo], play it face-up, score += 1, track best.
      - Else if score > 0 and lo < hi, trade tokens[hi] face-down for power.
        (lo < hi matters: trading the very last token gains nothing usable.)
      - Else stop.

    We record the best score seen, since the final face-down trade could leave
    us lower than the peak. Exchange argument: any optimal sequence can be
    rearranged so face-up plays use the smallest tokens and face-down plays
    use the largest, without decreasing the score.

Complexity:
    Time:  O(n log n) for sorting; the two-pointer sweep is O(n).
    Space: O(1) extra (O(n) if sort copy counted / Timsort buffer).
"""

from collections import deque
from typing import List


class Solution:
    def bagOfTokensScore(self, tokens: List[int], power: int) -> int:
        tokens = sorted(tokens)
        lo, hi = 0, len(tokens) - 1
        score = best = 0
        while lo <= hi:
            if power >= tokens[lo]:
                power -= tokens[lo]
                lo += 1
                score += 1
                best = max(best, score)
            elif score > 0 and lo < hi:
                power += tokens[hi]
                hi -= 1
                score -= 1
            else:
                break
        return best


class SolutionDeque:
    """
    Alternative: same greedy, expressed with a deque (popleft = cheapest,
    pop = most expensive). Identical complexity; some find it more readable.
    """

    def bagOfTokensScore(self, tokens: List[int], power: int) -> int:
        dq = deque(sorted(tokens))
        score = best = 0
        while dq:
            if power >= dq[0]:
                power -= dq.popleft()
                score += 1
                best = max(best, score)
            elif score > 0 and len(dq) > 1:
                power += dq.pop()
                score -= 1
            else:
                break
        return best


def _brute(tokens: List[int], power: int) -> int:
    """Exhaustive search over all play orders (tiny inputs only)."""
    n = len(tokens)
    best = 0

    def dfs(used: int, pw: int, sc: int) -> None:
        nonlocal best
        best = max(best, sc)
        for i in range(n):
            if used >> i & 1:
                continue
            if pw >= tokens[i]:
                dfs(used | 1 << i, pw - tokens[i], sc + 1)
            if sc >= 1:
                dfs(used | 1 << i, pw + tokens[i], sc - 1)

    dfs(0, power, 0)
    return best


if __name__ == "__main__":
    import random

    for S in (Solution(), SolutionDeque()):
        f = S.bagOfTokensScore
        assert f([100], 50) == 0
        assert f([200, 100], 150) == 1
        assert f([100, 200, 300, 400], 200) == 2
        assert f([], 100) == 0                     # no tokens
        assert f([0, 0, 0], 0) == 3                # zero-cost tokens
        assert f([50], 50) == 1                    # exact power
        assert f([71, 55, 82], 54) == 0            # can't start
        assert f([25, 91], 99) == 1

    random.seed(948)
    for _ in range(300):
        n = random.randint(0, 6)
        toks = [random.randint(0, 50) for _ in range(n)]
        pw = random.randint(0, 60)
        exp = _brute(toks, pw)
        assert Solution().bagOfTokensScore(toks, pw) == exp, (toks, pw)
        assert SolutionDeque().bagOfTokensScore(toks, pw) == exp, (toks, pw)

    print("All tests passed for 948. Bag of Tokens")
