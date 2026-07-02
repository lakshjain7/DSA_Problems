"""
224. Basic Calculator
Difficulty: Hard
Topics: Stack, Math, String, Recursion

Problem Statement:
Given a string s representing a valid expression, implement a basic
calculator to evaluate it, and return the result of the evaluation.
Note: You are not allowed to use any built-in function which evaluates
strings as mathematical expressions, such as eval().

The expression contains only non-negative integers, '+', '-', '(', ')', and
' '. Division and multiplication are not part of this problem (see
"Basic Calculator II" / "III" for those).

Examples:
    Example 1:
        Input: s = "1 + 1"
        Output: 2
    Example 2:
        Input: s = " 2-1 + 2 "
        Output: 3
    Example 3:
        Input: s = "(1+(4+5+2)-3)+(6+8)"
        Output: 23

Constraints:
    1 <= s.length <= 3 * 10^5
    s consists of digits, '+', '-', '(', ')', and ' '.
    s represents a valid expression.
    '+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" are
    invalid).
    '-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" are
    valid).
    There will be no two consecutive operators in the input.
    Every number and running calculation will fit in a signed 32-bit integer.

Approach (Stack-based single pass):
    Walk through the string left to right while tracking:
      - result: the running total for the current (innermost open) expression
      - number: the multi-digit number currently being parsed
      - sign: +1 or -1, the sign to apply to the next number/sub-expression
    On a digit, accumulate into number.
    On '+' or '-', fold (sign * number) into result, reset number, and set the
    new sign.
    On '(', we are about to start a nested expression. Push the current
    (result, sign) onto the stack so we can resume the outer expression later,
    then reset result to 0 and sign to +1 for the inner expression.
    On ')', fold the last number into result to close out the inner
    expression, then pop the outer (result, sign) from the stack and combine:
    outer_result + outer_sign * inner_result becomes the new result.
    At the end, fold any trailing number into result and return it.
    This correctly handles unary minus because "-(" pushes the current state
    and starts the parenthesized expression with sign flipped by whatever
    sign preceded '(' (handled through the stack's stored sign).

Complexity Analysis:
    Time:  O(n) - single pass over the string.
    Space: O(n) - the stack can hold O(n) entries in the worst case of deeply
           nested parentheses (e.g., "((((((1))))))").

Alternative Approach (Recursion):
    Treat '(' as a signal to recurse into evaluating the sub-expression, and
    ')' as the signal to return from that recursive call. This naturally
    mirrors the nested structure of parentheses, using the call stack instead
    of an explicit stack. Time: O(n), Space: O(n) due to recursion depth.
"""

from typing import List


def calculate(s: str) -> int:
    """Evaluate a basic calculator expression using an explicit stack."""
    stack: List[int] = []
    result = 0
    number = 0
    sign = 1  # +1 or -1, applies to the next number/sub-expression

    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch == '+':
            result += sign * number
            number = 0
            sign = 1
        elif ch == '-':
            result += sign * number
            number = 0
            sign = -1
        elif ch == '(':
            # Save current result and sign, start fresh for the sub-expression
            stack.append(result)
            stack.append(sign)
            result = 0
            sign = 1
        elif ch == ')':
            result += sign * number
            number = 0
            prev_sign = stack.pop()
            prev_result = stack.pop()
            result = prev_result + prev_sign * result
        # spaces are ignored

    result += sign * number
    return result


def calculate_recursive(s: str) -> int:
    """Alternative: recursive descent using an index pointer in a list."""
    pos = [0]  # mutable index shared across recursive calls

    def helper() -> int:
        result = 0
        number = 0
        sign = 1

        while pos[0] < len(s):
            ch = s[pos[0]]
            if ch.isdigit():
                number = number * 10 + int(ch)
            elif ch == '+':
                result += sign * number
                number = 0
                sign = 1
            elif ch == '-':
                result += sign * number
                number = 0
                sign = -1
            elif ch == '(':
                pos[0] += 1
                number = helper()
            elif ch == ')':
                result += sign * number
                return result
            pos[0] += 1

        result += sign * number
        return result

    return helper()


if __name__ == "__main__":
    for fn in (calculate, calculate_recursive):
        assert fn("1 + 1") == 2, f"{fn.__name__} failed example 1"
        assert fn(" 2-1 + 2 ") == 3, f"{fn.__name__} failed example 2"
        assert fn("(1+(4+5+2)-3)+(6+8)") == 23, f"{fn.__name__} failed example 3"

        # Simple no-space expression
        assert fn("1-1") == 0, f"{fn.__name__} failed simple subtraction"

        # Unary minus before parenthesis
        assert fn("-(2+3)") == -5, f"{fn.__name__} failed unary minus paren"

        # Single number
        assert fn("42") == 42, f"{fn.__name__} failed single number"

        # Nested parentheses
        assert fn("((((((1))))))") == 1, f"{fn.__name__} failed deep nesting"

        # Multiple signs and spaces
        assert fn("  2 - ( 5 - 6 ) ") == 3, f"{fn.__name__} failed mixed spaces"

        # Larger multi-digit numbers
        assert fn("100 - (50 + 25)") == 25, f"{fn.__name__} failed multi-digit"

        print(f"{fn.__name__}: all tests passed")

    print("All tests passed!")
