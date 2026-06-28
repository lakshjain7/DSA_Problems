"""
Problem: 394. Decode String
Difficulty: Medium
Topics: Stack, String

Problem Statement:
    Given an encoded string, return its decoded string. The encoding rule is:
    k[encoded_string], where the encoded_string inside the square brackets is
    repeated exactly k times. You may assume that the input data is always valid.
    Numbers k are positive integers and k < 300.

Examples:
    Input: s = "3[a]2[bc]"       Output: "aaabcbc"
    Input: s = "3[a2[c]]"        Output: "accaccacc"
    Input: s = "2[abc]3[cd]ef"   Output: "abcabccdcdcdef"
    Input: s = "abc3[cd]xyz"     Output: "abccdcdcdxyz"

Constraints:
    - 1 <= s.length <= 30
    - s consists of lowercase letters, digits, and square brackets '[]'.
    - s is guaranteed to be a valid input.
    - All integers in s are in range [1, 300].

Approach:
    Use a stack to handle nested brackets. As we scan each character:
    - Digit: accumulate into current_num
    - '[': push (current_string, current_num) onto stack, reset both
    - ']': pop (prev_string, k) and set current_string = prev_string + k * current_string
    - Letter: append to current_string

    The key insight is that when we encounter '[', we save the string built so far
    and the multiplier, then start fresh for the inner content. When we see ']',
    we finalize the inner content, multiply it, and prepend the saved outer string.

Complexity:
    Time:  O(n * maxK) where maxK is the max repeat count (decoding can produce
           strings up to O(300^(depth)) but input length bounds total work)
    Space: O(n) for stack depth

Alternative:
    Recursive DFS / index-based parsing — equivalent but more complex to implement.
"""

from typing import List


def decodeString(s: str) -> str:
    stack: list = []          # stores (string_so_far, repeat_count)
    current_string: str = ""
    current_num: int = 0

    for ch in s:
        if ch.isdigit():
            current_num = current_num * 10 + int(ch)  # handle multi-digit numbers
        elif ch == '[':
            stack.append((current_string, current_num))
            current_string = ""
            current_num = 0
        elif ch == ']':
            prev_string, k = stack.pop()
            current_string = prev_string + k * current_string
        else:
            current_string += ch

    return current_string


if __name__ == "__main__":
    # Basic cases
    assert decodeString("3[a]2[bc]") == "aaabcbc"
    assert decodeString("3[a2[c]]") == "accaccacc"
    assert decodeString("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert decodeString("abc3[cd]xyz") == "abccdcdcdxyz"

    # Single character no brackets
    assert decodeString("a") == "a"

    # Multi-digit number
    assert decodeString("10[a]") == "aaaaaaaaaa"

    # Deeply nested
    assert decodeString("2[3[a]]") == "aaaaaa"

    # Letters before and after brackets
    assert decodeString("x2[y]z") == "xyyz"

    # Just letters
    assert decodeString("hello") == "hello"

    print("All tests passed for 394. Decode String!")
