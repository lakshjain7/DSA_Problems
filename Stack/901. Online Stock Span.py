"""
901. Online Stock Span
Difficulty: Medium
Topics: Stack, Design, Monotonic Stack, Data Stream

Problem Statement
-----------------
Design an algorithm that collects daily price quotes for some stock and returns
the span of that stock's price for the current day.

The span of the stock's price in one day is the maximum number of consecutive
days (starting from that day and going backward) for which the stock price was
less than or equal to the price of that day.

  - For example, if the prices of the stock in the last four days is
    [7, 2, 1, 2] and the price of the stock today is 2, then the span of today
    is 4 because starting from today, the price of the stock was less than or
    equal to today's price for 4 consecutive days.
  - Also, if the prices of the stock in the last four days is [7, 34, 1, 2] and
    the price of the stock today is 8, then the span of today is 3 because
    starting from today, the price of the stock was less than or equal to
    today's price for 3 consecutive days.

Implement the StockSpanner class:
  - StockSpanner() Initializes the object of the class.
  - int next(int price) Returns the span of the stock's price given that today's
    price is `price`.

Example
-------
    Input
    ["StockSpanner","next","next","next","next","next","next","next"]
    [[],[100],[80],[60],[70],[60],[75],[85]]
    Output
    [null, 1, 1, 1, 2, 1, 4, 6]

    Explanation
    StockSpanner spanner = new StockSpanner();
    spanner.next(100); // return 1
    spanner.next(80);  // return 1
    spanner.next(60);  // return 1
    spanner.next(70);  // return 2
    spanner.next(60);  // return 1
    spanner.next(75);  // return 4, because the last 4 prices
                       //           (including today's 75) were <= 75:
                       //           [60, 70, 60, 75].
    spanner.next(85);  // return 6

Constraints
-----------
    - 1 <= price <= 10^5
    - At most 10^4 calls will be made to next.

Approach (Monotonic Stack)
--------------------------
The span for today = 1 + (number of previous consecutive days whose price is
<= today's price). A naive scan backward is O(n) per query, O(n^2) overall.

The key insight: once a previous day's price is "swallowed" by a later higher
day, it can never again be the day that stops a future span — because any future
day that reaches back past that later higher day must also be >= it, and thus
>= everything the higher day already swallowed. So we can collapse consecutive
runs.

We keep a stack of pairs (price, span) that is strictly decreasing in price from
bottom to top. For each new price:
    - Start with span = 1 (today itself).
    - While the stack is non-empty and the top price <= today's price, pop it
      and add its span to today's span (we absorb that entire run).
    - Push (price, span) onto the stack and return span.

Each price is pushed once and popped at most once, so the total work across all
next() calls is O(n) amortized -> O(1) amortized per call.

Complexity
----------
    Time:  O(1) amortized per next() call, O(n) total for n calls.
    Space: O(n) in the worst case (strictly decreasing prices keep everything).
"""

from typing import List, Tuple


class StockSpanner:
    def __init__(self) -> None:
        # Monotonic stack of (price, span), strictly decreasing prices upward.
        self.stack: List[Tuple[int, int]] = []

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span


class StockSpannerBruteForce:
    """
    Reference O(n) per query implementation, kept for cross-checking the
    monotonic-stack version in tests. Stores the full price history and scans
    backward while prices stay <= today's price.
    """

    def __init__(self) -> None:
        self.prices: List[int] = []

    def next(self, price: int) -> int:
        self.prices.append(price)
        span = 0
        i = len(self.prices) - 1
        while i >= 0 and self.prices[i] <= price:
            span += 1
            i -= 1
        return span


if __name__ == "__main__":
    # Example from the problem statement.
    spanner = StockSpanner()
    prices = [100, 80, 60, 70, 60, 75, 85]
    expected = [1, 1, 1, 2, 1, 4, 6]
    assert [spanner.next(p) for p in prices] == expected

    # Single call.
    s = StockSpanner()
    assert s.next(5) == 1

    # Strictly increasing prices: spans grow 1, 2, 3, ...
    s = StockSpanner()
    assert [s.next(p) for p in [1, 2, 3, 4, 5]] == [1, 2, 3, 4, 5]

    # Strictly decreasing prices: every span is 1.
    s = StockSpanner()
    assert [s.next(p) for p in [5, 4, 3, 2, 1]] == [1, 1, 1, 1, 1]

    # Equal prices count (<= today's price), so spans accumulate.
    s = StockSpanner()
    assert [s.next(p) for p in [7, 7, 7]] == [1, 2, 3]

    # Randomized cross-check against the brute-force reference.
    import random
    random.seed(1372)
    for _ in range(200):
        fast = StockSpanner()
        slow = StockSpannerBruteForce()
        seq = [random.randint(1, 20) for _ in range(random.randint(1, 60))]
        for p in seq:
            assert fast.next(p) == slow.next(p)

    print("All tests passed for 901. Online Stock Span")
