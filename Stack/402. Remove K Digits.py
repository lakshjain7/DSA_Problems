"""
402. Remove K Digits
Difficulty: Medium
Topics: String, Stack, Greedy, Monotonic Stack

PROBLEM STATEMENT
-----------------
Given string num representing a non-negative integer num, and an integer k,
return the smallest possible integer after removing k digits from num.

Examples
--------
Example 1:
    Input:  num = "1432219", k = 3
    Output: "1219"
    Explanation: Remove the three digits 4, 3, and 2 to form the new number
                 1219 which is the smallest.

Example 2:
    Input:  num = "10200", k = 1
    Output: "200"
    Explanation: Remove the leading 1 and the number is 200. Note that the
                 output must not have any leading zeroes.

Example 3:
    Input:  num = "10", k = 2
    Output: "0"
    Explanation: Remove all the digits from the number and it is left with
                 nothing which is 0.

Constraints
-----------
- 1 <= k <= num.length <= 10^5
- num consists of only digits.
- num does not have any leading zeros except for the zero itself.


APPROACH  (Greedy + Monotonic Increasing Stack)
-----------------------------------------------
To make the resulting number as small as possible, we want the most
significant (leftmost) digits to be as small as possible. A larger digit that
sits to the LEFT of a smaller digit hurts us far more than one on the right,
because leftmost positions carry the highest place value.

So we scan digits left to right, maintaining a stack that we keep as close to
non-decreasing as possible. When the current digit is smaller than the digit
on top of the stack, that top digit is "hurting" us, so we pop it (spending one
removal). We keep popping while we still have removals (k > 0) and the top is
strictly greater than the current digit.

After the pass, if we still have removals left (k > 0), the number is already
non-decreasing, so we remove from the end (the largest trailing digits).

Finally we strip leading zeros and handle the empty-result case ("0").

Why it works:
- Each pop removes a digit that has a smaller digit immediately after it,
  which is always a strictly beneficial (or neutral) swap toward a smaller
  number. Greedily eliminating the earliest such "descent" is optimal.

COMPLEXITY
----------
Time:  O(n) -- each digit is pushed and popped at most once.
Space: O(n) -- the stack.
"""

from typing import List


def removeKdigits(num: str, k: int) -> str:
    """Return the smallest integer string after removing k digits."""
    stack: List[str] = []

    for digit in num:
        # Pop larger digits sitting to the left while we still have budget.
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)

    # If removals remain, the stack is non-decreasing; drop from the end.
    if k > 0:
        stack = stack[:-k]

    # Build result: strip leading zeros.
    result = "".join(stack).lstrip("0")
    return result if result else "0"


# ---------------------------------------------------------------------------
# Alternative approach (reference): repeatedly delete the first digit that is
# greater than its right neighbor (the first "descent"), or the last digit if
# the string is already non-decreasing. This is the same greedy insight but
# formulated iteratively at O(n*k). Used to cross-check the optimal solution.
# ---------------------------------------------------------------------------
def removeKdigits_bruteforce(num: str, k: int) -> str:
    """O(n*k) reference implementation for verification."""
    s = num
    for _ in range(k):
        i = 0
        while i < len(s) - 1 and s[i] <= s[i + 1]:
            i += 1
        s = s[:i] + s[i + 1:]  # delete digit at index i
    s = s.lstrip("0")
    return s if s else "0"


if __name__ == "__main__":
    # Provided examples
    assert removeKdigits("1432219", 3) == "1219"
    assert removeKdigits("10200", 1) == "200"
    assert removeKdigits("10", 2) == "0"

    # Edge cases
    assert removeKdigits("9", 1) == "0"                # remove everything
    assert removeKdigits("112", 1) == "11"             # already ascending
    assert removeKdigits("1234567890", 9) == "0"       # trailing zero wins
    assert removeKdigits("100", 1) == "0"              # leading-zero handling
    assert removeKdigits("10001", 4) == "0"
    assert removeKdigits("5337", 2) == "33"
    assert removeKdigits("1173", 2) == "11"

    # Cross-check against the brute-force reference on many random cases.
    import random
    for _ in range(2000):
        n = random.randint(1, 8)
        s = "".join(random.choice("0123456789") for _ in range(n))
        # avoid illegal leading zeros in the *input* per constraints
        if len(s) > 1 and s[0] == "0":
            s = "1" + s[1:]
        kk = random.randint(1, len(s))
        assert removeKdigits(s, kk) == removeKdigits_bruteforce(s, kk), (s, kk)

    print("All tests passed for 402. Remove K Digits")
