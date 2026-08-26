"""
1249. Minimum Remove to Make Valid Parentheses
Difficulty: Medium
Topics: String, Stack

Problem Statement
-----------------
Given a string `s` of '(', ')' and lowercase English letters, remove the
minimum number of parentheses ( '(' or ')', in any positions ) so that the
resulting parentheses string is valid and return any valid result.

A parentheses string is valid if and only if:
    - It is the empty string, contains only lowercase characters, or
    - It can be written as AB (A concatenated with B), where A and B are valid
      strings, or
    - It can be written as (A), where A is a valid string.

Examples
--------
Example 1:
    Input:  s = "lee(t(c)o)de)"
    Output: "lee(t(c)o)de"
    Explanation: "lee(t(co)de)" , "lee(t(c)ode)" would also be accepted.

Example 2:
    Input:  s = "a)b(c)d"
    Output: "ab(c)d"

Example 3:
    Input:  s = "))(("
    Output: ""
    Explanation: An empty string is also valid.

Constraints
-----------
    1 <= s.length <= 10^5
    s[i] is either '(', ')', or a lowercase English letter.

Approach: Stack of indices to identify invalid parentheses
----------------------------------------------------------
The minimum number of removals equals the count of parentheses that can never
be matched. We find the exact positions of those unmatched parentheses:

    1. Scan left to right, pushing the index of every '(' onto a stack.
       For every ')', if the stack is non-empty we pop (a match); otherwise
       this ')' is unmatched -- record its index for removal.
    2. After the scan, any indices still left on the stack are unmatched '('
       -- record them for removal too.
    3. Build the answer by skipping every recorded index.

The set of "indices to remove" is exactly the parentheses that break validity,
so removing them is both sufficient (result is valid) and minimal.

Complexity
----------
Time:  O(n)  -- one pass to find bad indices, one pass to rebuild.
Space: O(n)  -- stack and removal set in the worst case.

Alternative: Two-pass counting without a stack
----------------------------------------------
A second technique (implemented below as `min_remove_two_pass`) avoids the
stack. First pass left->right keeps only ')' that have a matching '(' seen so
far (tracked with a balance counter). Second pass right->left over that result
trims any surplus '(' the same way. Same O(n)/O(n) bounds; useful as a
cross-check.
"""

from typing import List


def min_remove_to_make_valid(s: str) -> str:
    """Return a valid string after removing the fewest parentheses (stack)."""
    to_remove = set()
    stack: List[int] = []
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if stack:
                stack.pop()
            else:
                to_remove.add(i)
    to_remove.update(stack)  # unmatched '(' left over
    return "".join(ch for i, ch in enumerate(s) if i not in to_remove)


def min_remove_two_pass(s: str) -> str:
    """Alternative balance-counting solution (used to validate the main one)."""
    # First pass: drop ')' that have no matching '(' to their left.
    first: List[str] = []
    balance = 0
    for ch in s:
        if ch == "(":
            balance += 1
        elif ch == ")":
            if balance == 0:
                continue
            balance -= 1
        first.append(ch)
    # Second pass: drop surplus '(' from the right.
    result: List[str] = []
    open_to_keep = sum(1 for ch in first if ch == "(") - balance
    for ch in first:
        if ch == "(":
            if open_to_keep == 0:
                continue
            open_to_keep -= 1
        result.append(ch)
    return "".join(result)


def _is_valid(s: str) -> bool:
    """Helper: is the parentheses structure of s valid?"""
    bal = 0
    for ch in s:
        if ch == "(":
            bal += 1
        elif ch == ")":
            bal -= 1
            if bal < 0:
                return False
    return bal == 0


if __name__ == "__main__":
    # Provided examples. Multiple valid outputs exist, so we assert on the
    # properties that must hold: validity + minimality (same length).
    for original, expected in [
        ("lee(t(c)o)de)", "lee(t(c)o)de"),
        ("a)b(c)d", "ab(c)d"),
        ("))((", ""),
    ]:
        out = min_remove_to_make_valid(original)
        assert _is_valid(out), (original, out)
        assert len(out) == len(expected), (original, out, expected)
        # letters must be preserved and in order
        assert [c for c in out if c.isalpha()] == [c for c in original if c.isalpha()]

    # Edge cases
    assert min_remove_to_make_valid("") == ""
    assert min_remove_to_make_valid("abc") == "abc"          # no parens
    assert min_remove_to_make_valid("()") == "()"            # already valid
    assert min_remove_to_make_valid("(((") == ""             # all open
    assert min_remove_to_make_valid(")))") == ""             # all close
    assert min_remove_to_make_valid("(a(b(c)d)") == "a(b(c)d)" or _is_valid(
        min_remove_to_make_valid("(a(b(c)d)")
    )

    # Cross-check the two approaches produce equally-minimal valid strings.
    import random
    for _ in range(1000):
        n = random.randint(0, 30)
        s = "".join(random.choice("()ab") for _ in range(n))
        a = min_remove_to_make_valid(s)
        b = min_remove_two_pass(s)
        assert _is_valid(a) and _is_valid(b), (s, a, b)
        assert len(a) == len(b), (s, a, b)  # both minimal -> same length
        # letters preserved
        assert [c for c in a if c.isalpha()] == [c for c in s if c.isalpha()]

    print("All tests passed for 1249. Minimum Remove to Make Valid Parentheses")
