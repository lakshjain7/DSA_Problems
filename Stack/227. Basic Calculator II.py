"""
227. Basic Calculator II
Difficulty: Medium
Topics: Math, String, Stack

Problem Statement
-----------------
Given a string s which represents an expression, evaluate this expression and
return its value.

The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate
results will be in the range of [-2^31, 2^31 - 1].

Note: You are not allowed to use any built-in function which evaluates strings
as mathematical expressions, such as eval().

Examples
--------
Example 1:
    Input:  s = "3+2*2"
    Output: 7

Example 2:
    Input:  s = " 3/2 "
    Output: 1

Example 3:
    Input:  s = " 3+5 / 2 "
    Output: 5

Constraints
-----------
    1 <= s.length <= 3 * 10^5
    s consists of integers and the operators '+', '-', '*', and '/' separated
        by some number of spaces.
    s represents a valid expression.
    All the integers in the expression are non-negative integers in the range
        [0, 2^31 - 1].
    The answer is guaranteed to fit in a 32-bit integer.

Approach
--------
Only two precedence levels exist: '*' and '/' bind tighter than '+' and '-'.

Scan left to right, building each number as its digits appear. Keep a running
`prev_op` that records the operator that preceded the current number (start it
at '+'). When we finish reading a number (either we hit an operator or the end
of the string), we resolve it based on `prev_op`:

    '+' : push +num onto a stack
    '-' : push -num onto a stack
    '*' : pop, multiply by num, push back
    '/' : pop, integer-divide by num (truncating toward zero), push back

Because multiplication and division are applied immediately against the top of
the stack, higher-precedence operations are collapsed as we go, while additive
terms are simply accumulated. The final answer is the sum of the stack.

Truncation toward zero: Python's // floors toward negative infinity, so for a
negative top-of-stack we use int(a / b) which truncates toward zero, matching
the problem's required semantics.

Complexity
----------
Time:  O(n) - single pass over the string.
Space: O(n) - stack holds the additive terms (worst case all '+'/'-').
"""

from typing import List


def calculate(s: str) -> int:
    """Evaluate a +, -, *, / expression with correct operator precedence."""
    stack: List[int] = []
    num = 0
    prev_op = "+"

    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)

        # Resolve at each operator, and also at the final character.
        if (not ch.isdigit() and ch != " ") or i == len(s) - 1:
            if prev_op == "+":
                stack.append(num)
            elif prev_op == "-":
                stack.append(-num)
            elif prev_op == "*":
                stack.append(stack.pop() * num)
            elif prev_op == "/":
                top = stack.pop()
                # Truncate toward zero (int() on the float quotient).
                stack.append(int(top / num))
            prev_op = ch
            num = 0

    return sum(stack)


def calculate_o1_space(s: str) -> int:
    """
    Alternative: O(1) extra space.

    Instead of a stack, keep only `last_term` (the most recent additive term)
    and a running `result`. When a '+'/'-' is resolved we fold `last_term` into
    `result`; '*' and '/' update `last_term` in place. This avoids storing every
    term at the cost of slightly more bookkeeping.
    """
    result = 0
    last_term = 0
    num = 0
    prev_op = "+"

    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)

        if (not ch.isdigit() and ch != " ") or i == len(s) - 1:
            if prev_op == "+":
                result += last_term
                last_term = num
            elif prev_op == "-":
                result += last_term
                last_term = -num
            elif prev_op == "*":
                last_term = last_term * num
            elif prev_op == "/":
                last_term = int(last_term / num)
            prev_op = ch
            num = 0

    return result + last_term


if __name__ == "__main__":
    cases = [
        ("3+2*2", 7),
        (" 3/2 ", 1),
        (" 3+5 / 2 ", 5),
        ("1", 1),
        ("0", 0),
        ("14-3/2", 13),
        ("100000000/1/2/3", 16666666),
        ("2*3+4", 10),
        ("2+3*4-6/2", 11),
        ("10  - 3*  2", 4),
        ("14/3*2", 8),          # (14/3)=4, 4*2=8  -> left to right
        ("1-1+1", 1),
        ("100", 100),
    ]

    for expr, want in cases:
        got = calculate(expr)
        assert got == want, f"calculate({expr!r}) = {got}, expected {want}"

        got2 = calculate_o1_space(expr)
        assert got2 == want, f"calculate_o1_space({expr!r}) = {got2}, expected {want}"

    print("All tests passed for 227. Basic Calculator II")
