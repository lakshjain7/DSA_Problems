"""
43. Multiply Strings
Difficulty: Medium
Topics: Math, String, Simulation

Problem:
Given two non-negative integers num1 and num2 represented as strings, return
the product of num1 and num2, also represented as a string.

Note: You must not use any built-in BigInteger library or convert the inputs
to integer directly.

Example 1:
    Input: num1 = "2", num2 = "3"
    Output: "6"

Example 2:
    Input: num1 = "123", num2 = "456"
    Output: "56088"

Constraints:
    1 <= num1.length, num2.length <= 200
    num1 and num2 consist of digits only.
    Both num1 and num2 do not contain any leading zero, except the number 0 itself.

Approach (Grade-school multiplication into a position array):
    The product of an m-digit and an n-digit number has at most m + n digits.
    Digit num1[i] * num2[j] contributes to positions i + j (carry) and
    i + j + 1 (ones place) of the result array when indices are counted from
    the most-significant end. Iterate i, j from right to left, add the product
    into res[i+j+1], then push the carry into res[i+j]. Because we process
    lower positions first, every res[i+j+1] is final-ish (< 10) after its own
    update, and carries only flow leftward. Finally strip leading zeros.

Complexity:
    Time:  O(m * n)
    Space: O(m + n) for the result array.

Alternative (Accumulate raw products, then one carry pass):
    Add num1[i]*num2[j] into res[i+j+1] without carrying, then sweep once from
    right to left normalizing carries. Same complexity; slightly simpler inner
    loop, but intermediate cells can grow up to 81 * min(m, n).
"""


def multiply(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"
    m, n = len(num1), len(num2)
    res = [0] * (m + n)
    for i in range(m - 1, -1, -1):
        d1 = ord(num1[i]) - 48
        for j in range(n - 1, -1, -1):
            d2 = ord(num2[j]) - 48
            total = d1 * d2 + res[i + j + 1]
            res[i + j + 1] = total % 10
            res[i + j] += total // 10
    k = 0
    while k < len(res) - 1 and res[k] == 0:
        k += 1
    return "".join(chr(48 + d) for d in res[k:])


def multiplyLazyCarry(num1: str, num2: str) -> str:
    m, n = len(num1), len(num2)
    res = [0] * (m + n)
    for i in range(m):
        for j in range(n):
            res[i + j + 1] += (ord(num1[i]) - 48) * (ord(num2[j]) - 48)
    carry = 0
    for k in range(m + n - 1, -1, -1):
        carry, res[k] = divmod(res[k] + carry, 10)
    out = "".join(map(str, res)).lstrip("0")
    return out or "0"


if __name__ == "__main__":
    import random

    cases = [
        ("2", "3", "6"),
        ("123", "456", "56088"),
        ("0", "0", "0"),
        ("0", "98765", "0"),
        ("12345", "0", "0"),
        ("1", "1", "1"),
        ("9", "9", "81"),
        ("99", "99", "9801"),
        ("999", "1", "999"),
        ("100", "100", "10000"),
    ]
    for a, b, exp in cases:
        assert multiply(a, b) == exp, (a, b)
        assert multiplyLazyCarry(a, b) == exp, (a, b)

    # Random cross-check (int() used only to verify the test, not in solution)
    rng = random.Random(43)
    for _ in range(500):
        a = str(rng.randint(0, 10 ** rng.randint(1, 60)))
        b = str(rng.randint(0, 10 ** rng.randint(1, 60)))
        exp = str(int(a) * int(b))
        assert multiply(a, b) == exp, (a, b)
        assert multiplyLazyCarry(a, b) == exp, (a, b)

    # Max-size inputs
    a = "9" * 200
    b = "9" * 200
    assert multiply(a, b) == str(int(a) * int(b))

    print("All tests passed for 43. Multiply Strings")
