"""
282. Expression Add Operators
Difficulty: Hard
Topics: Math, String, Backtracking

PROBLEM STATEMENT
-----------------
Given a string num that contains only digits and an integer target, return all
possibilities to insert the binary operators '+', '-', and/or '*' between the
digits of num so that the resulting expression evaluates to the target value.
Note that operands in the returned expressions should not contain leading zeros.

Example 1:
    Input:  num = "123", target = 6
    Output: ["1*2*3", "1+2+3"]
    Explanation: Both "1*2*3" and "1+2+3" evaluate to 6.

Example 2:
    Input:  num = "232", target = 8
    Output: ["2*3+2", "2+3*2"]
    Explanation: Both "2*3+2" and "2+3*2" evaluate to 8.

Example 3:
    Input:  num = "3456237490", target = 9191
    Output: []
    Explanation: There are no expressions that can be created from "3456237490"
                 to evaluate to 9191.

Constraints:
    1 <= num.length <= 10
    num consists of only digits.
    -2^31 <= target <= 2^31 - 1

APPROACH — Backtracking with a running evaluation
-------------------------------------------------
We scan the digit string left to right. At each position we choose the next
operand by taking a prefix of the remaining digits, then choose which operator
precedes it. The hard part is multiplication precedence: "2 + 3 * 2" is 8, not
10, so a naive left-to-right accumulation is wrong.

We solve this by carrying two running values through the recursion:
    * `total` — the value of the expression built so far, and
    * `last`  — the value of the last multiplicative term, i.e. the operand (or
      chain of operands) most recently added/subtracted.

For a new operand `cur`:
    '+':  total + cur          ; new last =  cur
    '-':  total - cur          ; new last = -cur
    '*':  total - last + last*cur ; new last = last * cur

The multiplication case "undoes" the previous term's contribution (subtract
`last`) and replaces it with `last * cur`, which correctly folds the new factor
into the current product while leaving earlier '+'/'-' terms untouched. This
mirrors how operator precedence groups multiplication tighter than addition.

Leading-zero rule: an operand may be a single '0', but a multi-digit operand may
not start with '0'. So once we've taken a prefix starting at index i, if that
prefix has length > 1 and num[i] == '0', we stop extending.

WHY IT WORKS
------------
Every valid expression is uniquely determined by (a) where the operand
boundaries fall and (b) which operator sits in each gap. The recursion enumerates
exactly these choices — each gap independently becomes +, -, or * and each
operand is a contiguous prefix of the remaining suffix — so no valid expression
is missed and none is produced twice. The (total, last) invariant guarantees the
value we compare against target respects precedence at every step, so a match is
always a genuinely correct expression.

COMPLEXITY
----------
Let n = len(num). Between the n digits there are n-1 gaps, each with up to 4
states (start, +, -, *), giving O(4^n) expressions in the worst case, and each
completed expression costs O(n) to record.
    Time:  O(n * 4^n)
    Space: O(n) recursion depth (excluding the output list).
"""

from typing import List


def add_operators(num: str, target: int) -> List[str]:
    n = len(num)
    res: List[str] = []

    def backtrack(index: int, expr: str, total: int, last: int) -> None:
        if index == n:
            if total == target:
                res.append(expr)
            return

        for end in range(index + 1, n + 1):
            operand_str = num[index:end]
            # Disallow multi-digit operands with a leading zero.
            if len(operand_str) > 1 and operand_str[0] == "0":
                break
            cur = int(operand_str)

            if index == 0:
                # First operand: no leading operator.
                backtrack(end, operand_str, cur, cur)
            else:
                # Addition.
                backtrack(end, expr + "+" + operand_str, total + cur, cur)
                # Subtraction.
                backtrack(end, expr + "-" + operand_str, total - cur, -cur)
                # Multiplication (fix up precedence via `last`).
                backtrack(
                    end,
                    expr + "*" + operand_str,
                    total - last + last * cur,
                    last * cur,
                )

    backtrack(0, "", 0, 0)
    return res


def _evaluate(expr: str) -> int:
    """Safe evaluator used only to validate test results (no eval of solver)."""
    # Tokenize into numbers and operators.
    tokens: List[str] = []
    i = 0
    while i < len(expr):
        if expr[i] in "+-*":
            tokens.append(expr[i])
            i += 1
        else:
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            tokens.append(expr[i:j])
            i = j
    # First pass: handle '*'.
    stack: List[int] = []
    stack.append(int(tokens[0]))
    idx = 1
    while idx < len(tokens):
        op = tokens[idx]
        val = int(tokens[idx + 1])
        if op == "*":
            stack[-1] *= val
        elif op == "+":
            stack.append(val)
        else:  # '-'
            stack.append(-val)
        idx += 2
    return sum(stack)


if __name__ == "__main__":
    # Provided examples (compare as sets since order is unspecified).
    assert sorted(add_operators("123", 6)) == sorted(["1*2*3", "1+2+3"])
    assert sorted(add_operators("232", 8)) == sorted(["2*3+2", "2+3*2"])
    assert add_operators("3456237490", 9191) == []

    # Leading-zero handling: single-zero operands are allowed, multi-digit
    # operands with a leading zero are not.
    assert sorted(add_operators("105", 5)) == sorted(["1*0+5", "10-5"])
    assert sorted(add_operators("00", 0)) == sorted(["0+0", "0-0", "0*0"])

    # Single digit cases.
    assert add_operators("5", 5) == ["5"]
    assert add_operators("5", 3) == []

    # Negative target.
    assert "1-2-3" in add_operators("123", -4)

    # Validate every returned expression actually evaluates to target and has no
    # illegal leading zeros, across a batch of inputs.
    for num, tgt in [("123", 6), ("232", 8), ("105", 5), ("1234", 10),
                     ("99", 18), ("1000", 1)]:
        for expr in add_operators(num, tgt):
            assert _evaluate(expr) == tgt, f"{expr} != {tgt}"
            # Check no operand has an illegal leading zero.
            operands = []
            token = ""
            for ch in expr:
                if ch in "+-*":
                    operands.append(token)
                    token = ""
                else:
                    token += ch
            operands.append(token)
            for op in operands:
                assert len(op) == 1 or op[0] != "0", f"leading zero in {expr}"

    print("All tests passed!")
