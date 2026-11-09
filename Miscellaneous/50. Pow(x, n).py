"""
Problem 50. Pow(x, n)
Difficulty: Medium
Topics: Math, Recursion, Divide and Conquer

Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).

Example 1:
    Input: x = 2.00000, n = 10
    Output: 1024.00000
Example 2:
    Input: x = 2.10000, n = 3
    Output: 9.26100
Example 3:
    Input: x = 2.00000, n = -2
    Output: 0.25000   (2^-2 = 1/2^2 = 1/4)

Constraints:
    -100.0 < x < 100.0
    -2^31 <= n <= 2^31 - 1
    n is an integer.
    Either x is not zero or n > 0.
    -10^4 <= x^n <= 10^4

Approach (iterative binary exponentiation):
    Write n in binary. x^n is the product of x^(2^i) for every set bit i of n.
    Keep `base` = x^(2^i), squaring it each step, and multiply it into the
    result whenever the current lowest bit of n is 1. A negative exponent is
    handled by inverting x and using |n| (Python ints do not overflow, so
    -2^31 is safe).

Complexity:
    Time:  O(log |n|)
    Space: O(1)

Alternative (recursive divide and conquer):
    x^n = (x^(n/2))^2 for even n, and x * (x^(n//2))^2 for odd n.
    Time O(log |n|), space O(log |n|) for the call stack.
"""


class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x, n = 1 / x, -n
        result = 1.0
        base = x
        while n:
            if n & 1:
                result *= base
            base *= base
            n >>= 1
        return result

    def myPowRecursive(self, x: float, n: int) -> float:
        def helper(b: float, e: int) -> float:
            if e == 0:
                return 1.0
            half = helper(b, e // 2)
            return half * half if e % 2 == 0 else half * half * b

        if n < 0:
            return helper(1 / x, -n)
        return helper(x, n)


if __name__ == "__main__":
    s = Solution()

    def close(a: float, b: float) -> bool:
        return abs(a - b) <= 1e-9 * max(1.0, abs(b))

    for f in (s.myPow, s.myPowRecursive):
        assert close(f(2.0, 10), 1024.0)
        assert close(f(2.1, 3), 9.261)
        assert close(f(2.0, -2), 0.25)
        assert f(5.0, 0) == 1.0
        assert f(1.0, 2**31 - 1) == 1.0
        assert f(-1.0, 2**31 - 1) == -1.0
        assert f(-1.0, -2**31) == 1.0
        assert f(0.0, 5) == 0.0
        assert close(f(-2.0, 3), -8.0)
        assert close(f(-2.0, -3), -0.125)
        assert close(f(0.00001, 2147483647), 0.0)
        for x in (1.5, -0.5, 3.0, 7.0):
            for n in range(-8, 9):
                assert close(f(x, n), x ** n), (x, n)
    print("All tests passed.")
