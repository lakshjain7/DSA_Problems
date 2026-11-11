"""
678. Valid Parenthesis String
Difficulty: Medium
Topics: String, Stack, Greedy, Dynamic Programming

Problem:
Given a string s containing only three types of characters: '(', ')' and '*',
return true if s is valid.

The following rules define a valid string:
  - Any left parenthesis '(' must have a corresponding right parenthesis ')'.
  - Any right parenthesis ')' must have a corresponding left parenthesis '('.
  - Left parenthesis '(' must go before the corresponding right parenthesis ')'.
  - '*' could be treated as a single right parenthesis ')', a single left
    parenthesis '(', or an empty string "".

Example 1:
    Input: s = "()"
    Output: true

Example 2:
    Input: s = "(*)"
    Output: true

Example 3:
    Input: s = "(*))"
    Output: true

Constraints:
    1 <= s.length <= 100
    s[i] is '(', ')' or '*'.

Approach (Greedy range of open counts):
    Instead of tracking a single "open parentheses" balance, track the RANGE
    [lo, hi] of balances that are reachable given the choices for '*'.
      - '(' : lo += 1, hi += 1
      - ')' : lo -= 1, hi -= 1
      - '*' : lo -= 1 (treat as ')'), hi += 1 (treat as '(')
    If hi < 0 at any point, even treating every '*' as '(' can't save us, so
    the string is invalid. lo is clamped at 0 because a negative balance is
    never a legal state (we just drop the choices that would have produced it).
    At the end the string is valid iff 0 is reachable, i.e. lo == 0.
    Every balance between lo and hi is reachable because each '*' can shift
    the balance by -1, 0 or +1, so the reachable set is always contiguous.

Complexity:
    Time:  O(n) — single pass.
    Space: O(1).

Alternative (Two stacks of indices):
    Push indices of '(' onto `opens` and of '*' onto `stars`. On ')', pop an
    '(' if available, else a '*', else fail. Finally, match remaining '(' with
    a '*' that appears AFTER it (compare indices). O(n) time, O(n) space.
"""


def checkValidString(s: str) -> bool:
    lo = hi = 0
    for ch in s:
        if ch == "(":
            lo += 1
            hi += 1
        elif ch == ")":
            lo -= 1
            hi -= 1
        else:  # '*'
            lo -= 1
            hi += 1
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0


def checkValidStringStacks(s: str) -> bool:
    opens: list[int] = []
    stars: list[int] = []
    for i, ch in enumerate(s):
        if ch == "(":
            opens.append(i)
        elif ch == "*":
            stars.append(i)
        else:
            if opens:
                opens.pop()
            elif stars:
                stars.pop()
            else:
                return False
    while opens and stars:
        if opens.pop() > stars.pop():
            return False  # '*' before '(' can't close it
    return not opens


def _brute(s: str) -> bool:
    def go(i: int, bal: int) -> bool:
        if bal < 0:
            return False
        if i == len(s):
            return bal == 0
        c = s[i]
        if c == "(":
            return go(i + 1, bal + 1)
        if c == ")":
            return go(i + 1, bal - 1)
        return go(i + 1, bal + 1) or go(i + 1, bal - 1) or go(i + 1, bal)
    return go(0, 0)


if __name__ == "__main__":
    import itertools

    cases = {
        "()": True,
        "(*)": True,
        "(*))": True,
        "*": True,
        "(": False,
        ")": False,
        "*(": False,
        "(*": True,
        "**))": True,
        "((*)": True,
        "(((*)": False,
        "*)(": False,
        "(*)(*)": True,
        "((((()(()()()*()(((((*)()*(**(())))))(())()())(((())())())))))))(((((())*)))()))(()((*()*(*)))(*)()": True,
    }
    for s, exp in cases.items():
        assert checkValidString(s) == exp, s
        assert checkValidStringStacks(s) == exp, s

    # Exhaustive cross-check against brute force for all strings up to length 8
    for n in range(1, 9):
        for tup in itertools.product("()*", repeat=n):
            s = "".join(tup)
            b = _brute(s)
            assert checkValidString(s) == b, s
            assert checkValidStringStacks(s) == b, s

    print("All tests passed for 678. Valid Parenthesis String")
