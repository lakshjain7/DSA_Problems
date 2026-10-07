"""
17. Letter Combinations of a Phone Number
Difficulty: Medium
Topics: Hash Table, String, Backtracking

Problem:
Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent (using a standard telephone keypad
mapping). Return the answer in any order. Digit 1 does not map to any letters.

Examples:
    Input: digits = "23"
    Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

    Input: digits = ""
    Output: []

    Input: digits = "2"
    Output: ["a","b","c"]

Constraints:
    0 <= digits.length <= 4
    digits[i] is a digit in the range ['2', '9'].

Approach (backtracking):
    Build the combination one digit at a time. At depth i, try every letter that
    digit[i] maps to, append it to the current path, recurse to depth i+1, then
    pop it (undo). When the path length equals len(digits) it is a full answer.
    Every leaf of the decision tree is a distinct valid combination, so nothing
    is missed or duplicated.

Complexity:
    Time:  O(4^n * n) - up to 4 letters per digit, n characters joined per result.
    Space: O(n) recursion depth (excluding output).

Alternative (iterative BFS / product):
    Start with [""] and, for each digit, expand every partial string by every letter.
"""
from typing import List

MAP = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
       "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def letterCombinations(digits: str) -> List[str]:
    if not digits:
        return []
    res: List[str] = []
    path: List[str] = []

    def backtrack(i: int) -> None:
        if i == len(digits):
            res.append("".join(path))
            return
        for ch in MAP[digits[i]]:
            path.append(ch)
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return res


def letterCombinationsIterative(digits: str) -> List[str]:
    if not digits:
        return []
    res = [""]
    for d in digits:
        res = [p + ch for p in res for ch in MAP[d]]
    return res


if __name__ == "__main__":
    for f in (letterCombinations, letterCombinationsIterative):
        assert sorted(f("23")) == sorted(["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"])
        assert f("") == []
        assert sorted(f("2")) == ["a", "b", "c"]
        assert len(f("79")) == 16
        assert len(f("2345")) == 81
        assert len(f("7777")) == 256
        assert len(set(f("9999"))) == 256
    assert sorted(letterCombinations("234")) == sorted(letterCombinationsIterative("234"))
    print("All tests passed!")
