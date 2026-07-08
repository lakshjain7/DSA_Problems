"""
332. Reconstruct Itinerary
Difficulty: Hard
Topics: Graph, Depth-First Search, Eulerian Path, Hierholzer's Algorithm

Problem Statement
-----------------
You are given a list of airline tickets where tickets[i] = [from_i, to_i]
represent the departure and the arrival airports of one flight. Reconstruct
the itinerary in order and return it.

All of the tickets belong to a man who departs from "JFK", thus the itinerary
must begin with "JFK". If there are multiple valid itineraries, you should
return the itinerary that has the smallest lexical order when read as a single
string.

    - For example, the itinerary ["JFK", "LGA"] has a smaller lexical order
      than ["JFK", "LGB"].

You may assume all tickets form at least one valid itinerary. You must use all
the tickets once and only once.

Example 1:
    Input:  tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
    Output: ["JFK","MUC","LHR","SFO","SJC"]

Example 2:
    Input:  tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],
                        ["ATL","JFK"],["ATL","SFO"]]
    Output: ["JFK","ATL","JFK","SFO","ATL","SFO"]
    Explanation: Another possible reconstruction is
                 ["JFK","SFO","ATL","JFK","ATL","SFO"] but it is larger in
                 lexical order.

Constraints:
    1 <= tickets.length <= 300
    tickets[i].length == 2
    from_i.length == 3
    to_i.length == 3
    from_i and to_i consist of uppercase English letters.
    from_i != to_i


Approach: Hierholzer's Algorithm for an Eulerian Path
-----------------------------------------------------
Each ticket is a directed edge that must be used exactly once. Using every
edge once and only once is precisely the definition of an Eulerian path.
The problem guarantees such a path exists, so we do not need to check the
degree conditions ourselves.

Hierholzer's algorithm builds the path by following unused edges until we
get stuck (reach a vertex with no outgoing edges left), then "backtracks"
by prepending that dead-end vertex to the answer. Vertices are added to the
result only after all their outgoing edges are exhausted, so the answer is
constructed in reverse and reversed at the end.

Lexical order: for each airport we sort its destinations. If we always take
the smallest available destination first, the resulting Eulerian path is the
lexicographically smallest one. We store each adjacency list as a stack that
has been sorted in reverse, so pop() removes the smallest remaining
destination in O(1).

Why post-order works: when we hit a dead end, that vertex can only be the
final airport of the current traversal. Any edges we skipped over earlier
are revisited as the recursion unwinds, and their sub-tours get spliced in
at the correct positions. Reversing the post-order emission yields a valid
Eulerian path that uses every edge exactly once.

Complexity
----------
Let E = number of tickets (edges), V = number of distinct airports.
Time:  O(E log E) - dominated by sorting each adjacency list; the traversal
       itself visits each edge exactly once, O(E).
Space: O(V + E) - adjacency lists plus the recursion/explicit stack and the
       output list.
"""

from collections import defaultdict
from typing import Dict, List


def findItinerary(tickets: List[List[str]]) -> List[str]:
    graph: Dict[str, List[str]] = defaultdict(list)
    for src, dst in tickets:
        graph[src].append(dst)

    # Sort destinations in reverse so pop() yields the smallest one first.
    for src in graph:
        graph[src].sort(reverse=True)

    route: List[str] = []
    stack: List[str] = ["JFK"]

    # Iterative Hierholzer to avoid recursion-depth limits on long chains.
    while stack:
        airport = stack[-1]
        if graph[airport]:
            stack.append(graph[airport].pop())  # smallest unused destination
        else:
            route.append(stack.pop())           # dead end -> post-order emit

    return route[::-1]


# -----------------------------------------------------------------------------
# Alternative approach: recursive Hierholzer (same algorithm, DFS style).
# Cleaner to read; risks hitting Python's recursion limit on very long
# single-path itineraries, which is why the iterative version above is the
# primary solution.
# -----------------------------------------------------------------------------
def findItineraryRecursive(tickets: List[List[str]]) -> List[str]:
    graph: Dict[str, List[str]] = defaultdict(list)
    for src, dst in tickets:
        graph[src].append(dst)
    for src in graph:
        graph[src].sort(reverse=True)

    route: List[str] = []

    def dfs(airport: str) -> None:
        while graph[airport]:
            dfs(graph[airport].pop())
        route.append(airport)

    dfs("JFK")
    return route[::-1]


if __name__ == "__main__":
    # Provided examples.
    assert findItinerary(
        [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    ) == ["JFK", "MUC", "LHR", "SFO", "SJC"]

    assert findItinerary(
        [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"],
         ["ATL", "JFK"], ["ATL", "SFO"]]
    ) == ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]

    # Single ticket.
    assert findItinerary([["JFK", "ABC"]]) == ["JFK", "ABC"]

    # Lexical tie-break: must pick "A" before "D" from JFK.
    assert findItinerary(
        [["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]
    ) == ["JFK", "NRT", "JFK", "KUL"]

    # A case where the greedy-smallest-first choice would strand tickets if
    # done naively; Hierholzer still produces a valid full itinerary.
    result = findItinerary(
        [["JFK", "A"], ["A", "JFK"], ["JFK", "B"]]
    )
    assert result == ["JFK", "A", "JFK", "B"]
    assert len(result) == 4  # all 3 edges used

    # Multiple identical edges between the same pair of airports.
    assert findItinerary(
        [["JFK", "A"], ["A", "JFK"], ["JFK", "A"], ["A", "JFK"], ["JFK", "END"]]
    ) == ["JFK", "A", "JFK", "A", "JFK", "END"]

    # Both implementations must agree, and every itinerary must:
    #   (1) start at JFK, and
    #   (2) use exactly len(tickets)+1 airports (all edges consumed).
    samples = [
        [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]],
        [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"],
         ["ATL", "JFK"], ["ATL", "SFO"]],
        [["JFK", "A"], ["A", "B"], ["B", "JFK"], ["JFK", "C"], ["C", "JFK"]],
    ]
    for tk in samples:
        it = findItinerary([t[:] for t in tk])
        it_rec = findItineraryRecursive([t[:] for t in tk])
        assert it == it_rec
        assert it[0] == "JFK"
        assert len(it) == len(tk) + 1

    print("All tests passed for 332. Reconstruct Itinerary")
