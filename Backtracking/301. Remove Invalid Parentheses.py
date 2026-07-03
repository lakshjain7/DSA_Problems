"""
301. Remove Invalid Parentheses
Difficulty: Hard
Topics: Backtracking, BFS, String

Problem Statement:
Given a string s that contains parentheses and letters, remove the minimum
number of invalid parentheses to make the input string valid.

Return a list of all the possible results. You may return the answer in
any order.

Examples:
    Input: s = "()())()"
    Output: ["(())()","()()()"]

    Input: s = "(a)())()"
    Output: ["(a())()","(a)()()"]

    Input: s = ")("
    Output: [""]

Constraints:
    1 <= s.length <= 25
    s consists of lowercase English letters and parentheses '(' and ')'.
    There will be at most 20 parentheses in s.

Approach (BFS level-by-level string pruning):
We want the minimum number of removals, and BFS naturally finds the
shortest "distance" (fewest removals) to a valid string first, since it
explores all strings reachable by removing exactly k characters before
trying k+1. Starting from the original string, each BFS level generates
all strings obtained by deleting exactly one character from every string
in the previous level (only removing '(' or ')', never letters, since
letters never invalidate the string). As soon as any string in the current
level is valid, we record it and every other valid string at that same
level (since they all represent the same minimal removal count), then stop
without exploring further levels. A visited set prevents processing the
same string twice, which keeps the branching factor manageable in
practice. Validity of a string is checked with a simple running balance
counter that must never go negative and must end at exactly zero.

Complexity Analysis:
    Time:  O(2^n) worst case, where n = len(s), since in the worst case we
           may need to consider many subsets of characters to remove
           before finding valid results. In practice BFS with the visited
           set and early stopping at the first valid level prunes this
           substantially.
    Space: O(2^n) worst case for the queue and visited set holding
           generated substrings.

Alternative Approach (DFS backtracking with precomputed removal counts):
First scan the string once to count the number of extra '(' and extra ')'
that must be removed to balance it (this gives a tight lower bound on
removals without any search). Then do a DFS/backtracking traversal over
the string: at each parenthesis character, branch into "keep it" and
"remove it" (only allowed while we still have a removal budget for that
character type and only removing the first of consecutive duplicates to
avoid generating duplicate results). Prune whenever the running balance
goes negative. This is generally faster in practice than plain BFS because
it uses the precomputed removal counts to prune the search space
aggressively, though its worst-case complexity is the same order.
"""

from collections import deque
from typing import List


def is_valid(s: str) -> bool:
    balance = 0
    for ch in s:
        if ch == "(":
            balance += 1
        elif ch == ")":
            balance -= 1
            if balance < 0:
                return False
    return balance == 0


def remove_invalid_parentheses(s: str) -> List[str]:
    if is_valid(s):
        return [s]

    visited = {s}
    queue = deque([s])
    found = False
    result = []

    while queue and not found:
        level_size = len(queue)
        for _ in range(level_size):
            current = queue.popleft()
            if is_valid(current):
                result.append(current)
                found = True
                continue
            if found:
                continue
            for i in range(len(current)):
                if current[i] not in ("(", ")"):
                    continue
                candidate = current[:i] + current[i + 1:]
                if candidate not in visited:
                    visited.add(candidate)
                    queue.append(candidate)

    return result if result else [""]


def remove_invalid_parentheses_backtrack(s: str) -> List[str]:
    """Alternative approach: DFS backtracking with precomputed removal budgets."""
    remove_left = remove_right = 0
    for ch in s:
        if ch == "(":
            remove_left += 1
        elif ch == ")":
            if remove_left > 0:
                remove_left -= 1
            else:
                remove_right += 1

    result = set()

    def backtrack(index, path, open_count, close_count, remove_left, remove_right):
        if index == len(s):
            if remove_left == 0 and remove_right == 0 and open_count == close_count:
                result.add(path)
            return

        ch = s[index]

        # Option 1: remove current character (only if it's a parenthesis we still need to remove)
        if ch == "(" and remove_left > 0:
            backtrack(index + 1, path, open_count, close_count, remove_left - 1, remove_right)
        elif ch == ")" and remove_right > 0:
            backtrack(index + 1, path, open_count, close_count, remove_left, remove_right - 1)

        # Option 2: keep current character
        if ch != "(" and ch != ")":
            backtrack(index + 1, path + ch, open_count, close_count, remove_left, remove_right)
        elif ch == "(":
            backtrack(index + 1, path + ch, open_count + 1, close_count, remove_left, remove_right)
        elif ch == ")" and open_count > close_count:
            backtrack(index + 1, path + ch, open_count, close_count + 1, remove_left, remove_right)

    backtrack(0, "", 0, 0, remove_left, remove_right)
    return list(result) if result else [""]


if __name__ == "__main__":
    assert sorted(remove_invalid_parentheses("()())()")) == sorted(["(())()", "()()()"])
    assert sorted(remove_invalid_parentheses("(a)())()")) == sorted(["(a())()", "(a)()()"])
    assert remove_invalid_parentheses(")(") == [""]
    assert remove_invalid_parentheses("") == [""]
    assert remove_invalid_parentheses("(((") == [""]
    assert remove_invalid_parentheses("()") == ["()"]
    assert sorted(remove_invalid_parentheses("()())()")) == sorted(
        remove_invalid_parentheses_backtrack("()())()")
    )
    assert sorted(remove_invalid_parentheses("(a)())()")) == sorted(
        remove_invalid_parentheses_backtrack("(a)())()")
    )
    assert remove_invalid_parentheses_backtrack(")(") == [""]
    assert remove_invalid_parentheses_backtrack("()") == ["()"]

    print("All tests passed for 301. Remove Invalid Parentheses")
