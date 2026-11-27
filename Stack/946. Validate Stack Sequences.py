"""
946. Validate Stack Sequences
Difficulty: Medium
Topics: Array, Stack, Simulation

Problem:
Given two integer arrays `pushed` and `popped` each with distinct values,
return true if this could have been the result of a sequence of push and pop
operations on an initially empty stack, or false otherwise.

Example 1:
    Input: pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
    Output: true
    Explanation: push(1), push(2), push(3), push(4), pop() -> 4,
    push(5), pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1

Example 2:
    Input: pushed = [1,2,3,4,5], popped = [4,3,5,1,2]
    Output: false
    Explanation: 1 cannot be popped before 2.

Constraints:
    1 <= pushed.length <= 1000
    0 <= pushed[i] <= 1000
    All the elements of pushed are unique.
    popped.length == pushed.length
    popped is a permutation of pushed.

Approach (greedy simulation):
    Push elements of `pushed` one by one onto a real stack. After every push,
    pop greedily while the stack top equals the next expected value in
    `popped`. Greedy is safe: since values are distinct, if the top equals the
    next value to pop, that value must be popped now -- pushing anything on
    top of it would bury it and it could never come out next. At the end the
    sequence is valid iff every element of `popped` was matched.

Complexity:
    Time:  O(n) -- each element is pushed and popped at most once.
    Space: O(n) -- the auxiliary stack.

Alternative (O(1) extra space):
    Reuse the prefix of `pushed` itself as the stack: keep a write index `top`;
    write pushed[i] to pushed[top], then while top >= 0 and pushed[top] equals
    popped[j], decrement top and advance j. (Mutates the input.)
"""
from typing import List


class Solution:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        stack: List[int] = []
        j = 0
        for x in pushed:
            stack.append(x)
            while stack and stack[-1] == popped[j]:
                stack.pop()
                j += 1
        return j == len(popped)

    def validateStackSequencesInPlace(self, pushed: List[int], popped: List[int]) -> bool:
        pushed = pushed[:]  # copy so tests don't see mutation
        top = -1
        j = 0
        for x in pushed:
            top += 1
            pushed[top] = x
            while top >= 0 and pushed[top] == popped[j]:
                top -= 1
                j += 1
        return top == -1


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3, 4, 5], [4, 5, 3, 2, 1], True),
        ([1, 2, 3, 4, 5], [4, 3, 5, 1, 2], False),
        ([1], [1], True),
        ([1, 2], [1, 2], True),
        ([1, 2], [2, 1], True),
        ([1, 2, 3], [3, 1, 2], False),
        ([1, 2, 3], [1, 2, 3], True),     # pop immediately each time
        ([1, 2, 3], [3, 2, 1], True),     # push all then pop all
        ([0, 2, 1], [0, 1, 2], True),
        ([2, 1, 0], [1, 2, 0], True),
    ]
    for pu, po, exp in cases:
        assert s.validateStackSequences(pu, po) == exp, (pu, po)
        assert s.validateStackSequencesInPlace(pu, po) == exp, (pu, po)
    n = 1000
    assert s.validateStackSequences(list(range(n)), list(range(n - 1, -1, -1)))
    print("All tests passed!")
