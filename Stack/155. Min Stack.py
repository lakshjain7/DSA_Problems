"""
155. Min Stack
Difficulty: Medium
Topics: Stack, Design

Problem Statement
-----------------
Design a stack that supports push, pop, top, and retrieving the minimum
element in constant time.

Implement the MinStack class:
    - MinStack() initializes the stack object.
    - void push(int val) pushes the element val onto the stack.
    - void pop() removes the element on the top of the stack.
    - int top() gets the top element of the stack.
    - int getMin() retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

Example 1:
    Input:
        ["MinStack","push","push","push","getMin","pop","top","getMin"]
        [[],[-2],[0],[-3],[],[],[],[]]
    Output:
        [null,null,null,null,-3,null,0,-2]

    Explanation:
        MinStack minStack = new MinStack();
        minStack.push(-2);
        minStack.push(0);
        minStack.push(-3);
        minStack.getMin(); // return -3
        minStack.pop();
        minStack.top();    // return 0
        minStack.getMin(); // return -2

Constraints:
    -2^31 <= val <= 2^31 - 1
    Methods pop, top and getMin operations will always be called on
    non-empty stacks.
    At most 3 * 10^4 calls will be made to push, pop, top, and getMin.


Approach: Two Stacks (main stack + running-minimum stack)
---------------------------------------------------------
The challenge is that getMin must be O(1), but a normal stack only knows
its top element. If we merely stored a single running minimum, we would
lose the previous minimum whenever that minimum got popped.

The fix is to keep a parallel "min stack" whose top always equals the
minimum of the elements currently in the main stack. On every push we
push min(val, current_min) onto the min stack, and on every pop we pop
both stacks together. Because each entry in the min stack corresponds to
exactly one entry in the main stack, the min stack top is always in sync
with the current contents.

Why it works: min_stack[i] stores the minimum of the first i+1 elements
that are still present. When we pop, the element that had recorded that
minimum leaves too, exposing the minimum that was valid before it arrived.

Complexity
----------
Time:  O(1) for push, pop, top, and getMin.
Space: O(n) for storing n elements twice (main + min stack).
"""

from typing import List


class MinStack:
    def __init__(self) -> None:
        self._stack: List[int] = []
        self._mins: List[int] = []

    def push(self, val: int) -> None:
        self._stack.append(val)
        if not self._mins:
            self._mins.append(val)
        else:
            self._mins.append(min(val, self._mins[-1]))

    def pop(self) -> None:
        self._stack.pop()
        self._mins.pop()

    def top(self) -> int:
        return self._stack[-1]

    def getMin(self) -> int:
        return self._mins[-1]


# -----------------------------------------------------------------------------
# Alternative approach: single stack of (value, min_so_far) tuples.
# Same O(1) guarantees; keeps everything in one list instead of two.
# -----------------------------------------------------------------------------
class MinStackTuples:
    def __init__(self) -> None:
        self._stack: List[tuple] = []  # (value, min_so_far)

    def push(self, val: int) -> None:
        cur_min = val if not self._stack else min(val, self._stack[-1][1])
        self._stack.append((val, cur_min))

    def pop(self) -> None:
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1][0]

    def getMin(self) -> int:
        return self._stack[-1][1]


if __name__ == "__main__":
    # Example from the problem statement.
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.getMin() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.getMin() == -2

    # Minimum is restored correctly after the current min is popped.
    ms2 = MinStack()
    ms2.push(5)
    assert ms2.getMin() == 5
    ms2.push(3)
    assert ms2.getMin() == 3
    ms2.push(3)                 # duplicate minimum
    assert ms2.getMin() == 3
    ms2.pop()
    assert ms2.getMin() == 3    # still 3, one copy remains
    ms2.pop()
    assert ms2.getMin() == 5    # restored to 5

    # Single element behaviour.
    ms3 = MinStack()
    ms3.push(42)
    assert ms3.top() == 42
    assert ms3.getMin() == 42

    # Negative / large boundary values.
    ms4 = MinStack()
    ms4.push(2**31 - 1)
    ms4.push(-(2**31))
    assert ms4.getMin() == -(2**31)
    ms4.pop()
    assert ms4.getMin() == 2**31 - 1

    # Cross-check the tuple-based alternative against the two-stack version.
    a, b = MinStack(), MinStackTuples()
    import random
    random.seed(0)
    reference = []
    for _ in range(1000):
        if not reference or random.random() < 0.6:
            v = random.randint(-100, 100)
            a.push(v)
            b.push(v)
            reference.append(v)
        else:
            a.pop()
            b.pop()
            reference.pop()
        if reference:
            expected = min(reference)
            assert a.getMin() == expected
            assert b.getMin() == expected
            assert a.top() == reference[-1]
            assert b.top() == reference[-1]

    print("All tests passed for 155. Min Stack")
