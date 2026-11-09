"""
Problem 818. Race Car
Difficulty: Hard
Topics: Dynamic Programming

Your car starts at position 0 with speed +1 on an infinite number line. It can
go into negative positions. The car drives automatically according to a
sequence of instructions 'A' (accelerate) and 'R' (reverse):
    - 'A': position += speed; speed *= 2
    - 'R': if speed > 0 then speed = -1, otherwise speed = 1 (position stays)
Given a target position, return the length of the shortest sequence of
instructions to reach it.

Example 1:
    Input: target = 3
    Output: 2     ("AA": 0 -> 1 -> 3)
Example 2:
    Input: target = 6
    Output: 5     ("AAARA": 0 -> 1 -> 3 -> 7 -> 7 -> 6)

Constraints:
    1 <= target <= 10^4

Approach (top-down DP):
    Let n be the smallest integer with 2^n - 1 >= t, so n 'A's reach 2^n - 1.
    dp[t] =
      * n                       if 2^n - 1 == t (exact hit).
      * Otherwise two options:
          1. Overshoot: n 'A's, one 'R', then dp[2^n - 1 - t]
             => n + 1 + dp[2^n - 1 - t].
          2. Stop before: use n-1 'A's (reach 2^(n-1) - 1), reverse, back up
             m 'A's (m in 0..n-2, reaching 2^m - 1 backwards), reverse again,
             then solve the rest:
             => (n-1) + 1 + m + 1 + dp[t - (2^(n-1) - 1) + (2^m - 1)].
    Reversing right after a long overshoot is never better than these cases,
    and the trailing 'R' is never needed at the end, which the definition
    already accounts for since dp counts only instructions to reach t.

Complexity:
    Time:  O(T log^2 T) - T states, each tries O(log T) m-values (memoised).
    Space: O(T) for the memo plus O(log T) recursion depth.

Alternative (BFS over (position, speed) states):
    Bound positions to [0, 2*target]. Simple and obviously correct, used here as
    the test oracle; O(T log T) states in practice.
"""
from collections import deque
from functools import lru_cache


class Solution:
    def racecar(self, target: int) -> int:
        @lru_cache(maxsize=None)
        def dp(t: int) -> int:
            n = t.bit_length()            # smallest n with 2^n > t
            if (1 << n) - 1 == t:
                return n
            # Overshoot, then reverse.
            best = n + 1 + dp((1 << n) - 1 - t)
            # Stop before: n-1 accelerations, reverse, m back, reverse.
            for m in range(n - 1):
                best = min(
                    best,
                    (n - 1) + 1 + m + 1 + dp(t - (1 << (n - 1)) + (1 << m)),
                )
            return best

        return dp(target)

    def racecarBFS(self, target: int) -> int:
        start = (0, 1)
        seen = {start}
        q = deque([(0, 1, 0)])
        limit = 2 * target
        while q:
            pos, speed, steps = q.popleft()
            if pos == target:
                return steps
            nxt = [(pos + speed, speed * 2), (pos, -1 if speed > 0 else 1)]
            for p, sp in nxt:
                if abs(p) <= limit and (p, sp) not in seen:
                    seen.add((p, sp))
                    q.append((p, sp, steps + 1))
        return -1


if __name__ == "__main__":
    s = Solution()
    assert s.racecar(1) == 1
    assert s.racecar(3) == 2
    assert s.racecar(6) == 5
    assert s.racecar(2) == 4      # "AARA"
    assert s.racecar(4) == 5
    assert s.racecar(7) == 3
    assert s.racecar(5) == 7
    # Cross-check DP against BFS oracle.
    for t in range(1, 301):
        assert s.racecar(t) == s.racecarBFS(t), t
    assert s.racecar(10000) == s.racecarBFS(10000)
    assert s.racecar(8191) == 13
    print("All tests passed.")
