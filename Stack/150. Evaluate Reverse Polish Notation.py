"""
150. Evaluate Reverse Polish Notation
Difficulty: Medium
Topics: Stack, Array, Math

Problem Statement:
You are given an array of strings tokens that represents an arithmetic
expression in Reverse Polish Notation (postfix notation).

Evaluate the expression. Return an integer that represents the value of
the expression.

Note that:
- The valid operators are '+', '-', '*', and '/'.
- Each operand may be an integer or another expression.
- The division between two integers always truncates toward zero.
- There will not be any division by zero.
- The input represents a valid arithmetic expression in a reverse polish
  notation.
- The answer and all intermediate calculations can be represented in a
  32-bit integer.

Examples:
Input: tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9

Input: tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6

Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
Output: 22
Explanation:
((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22

Constraints:
- 1 <= tokens.length <= 10^4
- tokens[i] is either an operator: "+", "-", "*", or "/", or an integer
  in the range [-200, 200].

Approach:
Reverse Polish Notation is naturally evaluated with a stack. Scan the
tokens left to right:
- If the token is a number, push it onto the stack.
- If the token is an operator, pop the top two values (the second-popped
  value is the left operand, the first-popped value is the right
  operand), apply the operator, and push the result back.

At the end, the stack contains exactly one value: the final result.

Python's default integer division (//) rounds toward negative infinity,
but the problem requires truncation toward zero (e.g. -7 // 2 == -4 in
Python, but truncated division gives -3). We use int(a / b) or
math.trunc(a / b) to truncate correctly, or equivalently
int(a / b) with float division and int() truncation.

Why it works:
Postfix notation removes the need for parentheses or operator precedence
rules — every operator's operands are exactly the two values most
recently computed/pushed, which is exactly what a stack's LIFO order
gives us for free.

Complexity:
- Time: O(n), each token is processed once with O(1) stack operations.
- Space: O(n) for the stack in the worst case (all tokens are numbers
  before a single operator at the end, e.g. all operands then chained
  ops reduce the stack, but worst case still O(n)).

Alternative approach:
A recursive approach can evaluate RPN by processing tokens from the end
of the array backward, using recursion to consume two operands for each
operator. This is less natural because RPN is designed for forward,
stack-based, single-pass evaluation, but it demonstrates the equivalence
between an explicit stack and the implicit call stack of recursion.
"""

from typing import List


def evalRPN(tokens: List[str]) -> int:
    stack: List[int] = []
    operators = {"+", "-", "*", "/"}

    for token in tokens:
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:  # division, truncate toward zero
                stack.append(int(a / b))
        else:
            stack.append(int(token))

    return stack[-1]


def evalRPN_recursive(tokens: List[str]) -> int:
    """Alternative: consume tokens from the back using recursion + an
    index cursor that mutates as we go (simulates the call stack)."""
    operators = {"+", "-", "*", "/"}

    def helper(idx: int):
        token = tokens[idx]
        if token not in operators:
            return int(token), idx - 1
        b, idx = helper(idx - 1)
        a, idx = helper(idx)
        if token == "+":
            return a + b, idx
        elif token == "-":
            return a - b, idx
        elif token == "*":
            return a * b, idx
        else:
            return int(a / b), idx

    result, _ = helper(len(tokens) - 1)
    return result


if __name__ == "__main__":
    for fn in (evalRPN, evalRPN_recursive):
        assert fn(["2", "1", "+", "3", "*"]) == 9
        assert fn(["4", "13", "5", "/", "+"]) == 6
        assert (
            fn(
                [
                    "10", "6", "9", "3", "+", "-11", "*", "/", "*", "17",
                    "+", "5", "+",
                ]
            )
            == 22
        )
        # Single number, no operators.
        assert fn(["42"]) == 42
        # Negative numbers.
        assert fn(["-4", "-5", "*"]) == 20
        # Truncation toward zero for negative division.
        assert fn(["7", "-2", "/"]) == -3
        # Subtraction order matters (a - b, not b - a).
        assert fn(["5", "3", "-"]) == 2

    print("All Evaluate RPN tests passed.")
