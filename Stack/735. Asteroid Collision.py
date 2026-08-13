"""
735. Asteroid Collision
Difficulty: Medium
Topics: Array, Stack, Simulation

Problem Statement
-----------------
We are given an array `asteroids` of integers representing asteroids in a row.
The indices of the asteroid in the array represent their relative position in
space.

For each asteroid, the absolute value represents its size, and the sign
represents its direction (positive meaning right, negative meaning left). Each
asteroid moves at the same speed.

Find out the state of the asteroids after all collisions. If two asteroids meet,
the smaller one will explode. If both are the same size, both will explode. Two
asteroids moving in the same direction will never meet.

Examples
--------
Example 1:
    Input:  asteroids = [5, 10, -5]
    Output: [5, 10]
    Explanation: The 10 and -5 collide resulting in 10. The 5 and 10 never collide.

Example 2:
    Input:  asteroids = [8, -8]
    Output: []
    Explanation: The 8 and -8 collide exploding each other.

Example 3:
    Input:  asteroids = [10, 2, -5]
    Output: [10]
    Explanation: The 2 and -5 collide resulting in -5. The 10 and -5 collide
                 resulting in 10.

Constraints
-----------
    2 <= asteroids.length <= 10^4
    -1000 <= asteroids[i] <= 1000
    asteroids[i] != 0

Approach
--------
A collision can only happen when a right-moving asteroid (positive) is
immediately followed by a left-moving asteroid (negative). This is a classic
use case for a stack.

We scan left to right and keep a stack of surviving asteroids. For each new
asteroid `a`:
  - It only threatens the stack when `a < 0` (moving left) and the top of the
    stack is `> 0` (moving right). Otherwise it simply survives and is pushed.
  - While the collision condition holds, compare sizes:
      * If the top is smaller than |a|, the top explodes (pop) and we keep
        checking `a` against the new top.
      * If the top equals |a|, both explode (pop the top, and `a` is gone).
      * If the top is larger, `a` explodes and the top survives.
  - If `a` survives all comparisons (stack empty, top negative, or top blown
    away), push it.

Why it works: a negative asteroid can only ever collide with the contiguous run
of positive asteroids directly to its left, and the stack always holds exactly
that run at its top, in order. Each asteroid is pushed and popped at most once.

Complexity
----------
Time:  O(n) - each asteroid is pushed and popped at most once.
Space: O(n) - the stack in the worst case (e.g. all positive).
"""

from typing import List


def asteroid_collision(asteroids: List[int]) -> List[int]:
    """Return the surviving asteroids after all collisions resolve."""
    stack: List[int] = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            top = stack[-1]
            if top < -a:
                stack.pop()          # top explodes, a keeps moving
                continue
            elif top == -a:
                stack.pop()          # both explode
            alive = False            # a explodes (top > -a) or was equal
        if alive:
            stack.append(a)
    return stack


# ---------------------------------------------------------------------------
# Alternative approach: explicit "survives" flag instead of the inline `alive`
# short-circuit. Same stack logic and complexity, spelled out step by step.
# ---------------------------------------------------------------------------
def asteroid_collision_verbose(asteroids: List[int]) -> List[int]:
    stack: List[int] = []
    for a in asteroids:
        survives = True
        # Only a left-mover can collide, and only with right-movers on top.
        while stack and a < 0 and stack[-1] > 0:
            top = stack[-1]
            if abs(top) < abs(a):
                stack.pop()            # top loses, a continues checking
            elif abs(top) == abs(a):
                stack.pop()            # both destroyed
                survives = False
                break
            else:
                survives = False       # a loses
                break
        if survives:
            stack.append(a)
    return stack


if __name__ == "__main__":
    for fn in (asteroid_collision, asteroid_collision_verbose):
        assert fn([5, 10, -5]) == [5, 10]
        assert fn([8, -8]) == []
        assert fn([10, 2, -5]) == [10]
        assert fn([-2, -1, 1, 2]) == [-2, -1, 1, 2]   # never collide
        assert fn([1, -2, -2, -2]) == [-2, -2, -2]     # 1 destroyed
        assert fn([-1]) == [-1]
        assert fn([1, 1, -1]) == [1]                    # rightmost 1 survives
        assert fn([1, -1, 1, -1]) == []                # cascade to empty
        assert fn([10, 2, -5, -20]) == [-20]           # chain reaction
        assert fn([-2, 2]) == [-2, 2]                   # move apart, no collision

    print("All tests passed.")
