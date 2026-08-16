"""
895. Maximum Frequency Stack
Difficulty: Hard
Topics: Hash Table, Stack, Design, Ordered Collections

Problem Statement
-----------------
Design a stack-like data structure to push elements to the stack and pop the
most frequent element from the stack.

Implement the FreqStack class:
- FreqStack() constructs an empty frequency stack.
- void push(int val) pushes an integer val onto the top of the stack.
- int pop() removes and returns the most frequent element in the stack.
    - If there is a tie for the most frequent element, the element closest to
      the top of the stack is removed and returned.

Examples
--------
Example 1:
    Input:
      ["FreqStack", "push", "push", "push", "push", "push", "push",
       "pop", "pop", "pop", "pop"]
      [[], [5], [7], [5], [7], [4], [5], [], [], [], []]
    Output: [null, null, null, null, null, null, null, 5, 7, 5, 4]
    Explanation:
      After the pushes the stack (bottom -> top) is [5,7,5,7,4,5].
      pop() -> 5 (freq 3, most frequent). Stack becomes [5,7,5,7,4].
      pop() -> 7 (5 and 7 tie at freq 2; 7 is closer to top). Stack [5,7,5,4].
      pop() -> 5 (freq 2, most frequent). Stack becomes [5,7,4].
      pop() -> 4 (5,7,4 all tie at freq 1; 4 is closest to top). Stack [5,7].

Constraints
-----------
- 0 <= val <= 10^9
- At most 2 * 10^4 calls will be made to push and pop.
- It is guaranteed that there will be at least one element in the stack before
  calling pop.

Approach
--------
Two hash maps plus a "stack of stacks" grouped by frequency:
- freq[val]      : current frequency of each value.
- group[f]       : a list (stack) of values that have reached frequency f,
                   in the order they were pushed.
- max_freq       : the highest frequency currently present.

push(val):
    Increment freq[val] to f, update max_freq, and append val to group[f].
    Appending to group[f] records that this particular occurrence of val is
    the f-th copy, and preserves push order within that frequency layer.

pop():
    The answer is the last value in group[max_freq] (most frequent, and among
    ties the most recently pushed = closest to top). Pop it, decrement its
    freq, and if group[max_freq] becomes empty, decrement max_freq.

Why it works
------------
Each occurrence of a value lives in exactly the frequency layer equal to how
many copies existed when it was pushed. The top layer group[max_freq] holds
precisely the elements tied for most frequent, ordered by recency, so popping
its last element satisfies both the "most frequent" rule and the "closest to
top" tie-breaker. Removing it leaves every other element in the correct layer,
maintaining the invariant.

Complexity
----------
Time:  O(1) amortised for both push and pop (dict and list-append/pop).
Space: O(n) where n is the number of elements currently stored.

Alternative Approach
--------------------
A max-heap keyed by (frequency, insertion_sequence) also solves it: push adds
(freq_after_push, seq, val) with an ever-increasing seq as tie-breaker, and
pop takes the heap max. That is O(log n) per operation - simpler to reason
about but asymptotically slower than the O(1) bucketed-stack solution above.
It is included below as FreqStackHeap.
"""
import heapq
from collections import defaultdict


class FreqStack:
    """O(1) bucketed 'stack of stacks' by frequency."""

    def __init__(self) -> None:
        self.freq: dict = defaultdict(int)
        self.group: dict = defaultdict(list)
        self.max_freq: int = 0

    def push(self, val: int) -> None:
        f = self.freq[val] + 1
        self.freq[val] = f
        if f > self.max_freq:
            self.max_freq = f
        self.group[f].append(val)

    def pop(self) -> int:
        val = self.group[self.max_freq].pop()
        self.freq[val] -= 1
        if not self.group[self.max_freq]:
            self.max_freq -= 1
        return val


class FreqStackHeap:
    """O(log n) max-heap variant using (freq, seq) ordering."""

    def __init__(self) -> None:
        self.freq: dict = defaultdict(int)
        self.heap: list = []
        self.seq: int = 0

    def push(self, val: int) -> None:
        self.freq[val] += 1
        # Negate for max-heap behaviour on (frequency, recency).
        heapq.heappush(self.heap, (-self.freq[val], -self.seq, val))
        self.seq += 1

    def pop(self) -> int:
        _, _, val = heapq.heappop(self.heap)
        self.freq[val] -= 1
        return val


if __name__ == "__main__":
    for cls in (FreqStack, FreqStackHeap):
        fs = cls()
        for v in (5, 7, 5, 7, 4, 5):
            fs.push(v)
        assert fs.pop() == 5
        assert fs.pop() == 7
        assert fs.pop() == 5
        assert fs.pop() == 4
        # Remaining stack is [5, 7]; both freq 1, 7 closest to top.
        assert fs.pop() == 7
        assert fs.pop() == 5

        # Single element push/pop
        fs2 = cls()
        fs2.push(42)
        assert fs2.pop() == 42

        # All distinct: behaves like a plain stack (LIFO) on ties.
        fs3 = cls()
        for v in (1, 2, 3):
            fs3.push(v)
        assert fs3.pop() == 3
        assert fs3.pop() == 2
        assert fs3.pop() == 1

        # Repeated pushes then interleaved pops.
        fs4 = cls()
        for v in (9, 9, 9):
            fs4.push(v)
        assert fs4.pop() == 9
        fs4.push(1)
        fs4.push(1)  # 1 now freq 2, 9 freq 2, 1 closer to top
        assert fs4.pop() == 1
        assert fs4.pop() == 9  # 9 freq 2 vs 1 freq 1 -> 9

    print("All tests passed.")
