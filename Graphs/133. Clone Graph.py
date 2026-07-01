"""
133. Clone Graph
Difficulty: Medium
Topics: Graph, Hash Table, Depth-First Search, Breadth-First Search

Problem Statement:
Given a reference to a node in a connected undirected graph, return a deep
copy (clone) of the graph. Each node in the graph contains a value (int)
and a list of its neighbors (List[Node]).

    class Node:
        def __init__(self, val = 0, neighbors = None):
            self.val = val
            self.neighbors = neighbors if neighbors is not None else []

Test case format: the graph is serialized as an adjacency list, where each
list index i corresponds to node with val = i + 1, and the list at index i
contains the vals of that node's neighbors. The first node always has
val = 1.

Examples:
    Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
    Output: [[2,4],[1,3],[2,4],[1,3]]
    Explanation: There are 4 nodes. Node 1's neighbors are 2 and 4. Node 2's
    neighbors are 1 and 3. Node 3's neighbors are 2 and 4. Node 4's
    neighbors are 1 and 3.

    Input: adjList = [[]]
    Output: [[]]
    Explanation: A single node with no neighbors.

    Input: adjList = []
    Output: []
    Explanation: The graph is empty (node is None).

Constraints:
    The number of nodes in the graph is in the range [0, 100].
    1 <= Node.val <= 100
    Node.val is unique for each node.
    There are no repeated edges and no self-loops.
    The graph is connected and all nodes can be visited starting from the
    given node.

Approach (DFS with a hash map of visited clones):
The core difficulty of cloning a graph (as opposed to a tree) is that it
can contain cycles, so a naive recursive copy would recurse forever. The
fix is to keep a hash map `old_to_new` from original node -> cloned node.
When we visit a node for the first time we immediately create its clone
and register it in the map *before* recursing into its neighbors. That way
if a neighbor's DFS call leads back to a node already being processed
(a cycle), the lookup in `old_to_new` returns the in-progress clone instead
of triggering infinite recursion. For every neighbor of the original node,
we recursively clone it (or fetch the existing clone) and append it to the
current clone's neighbor list. A BFS variant works identically, using a
queue and the same hash map, and is provided as the alternative.

Complexity Analysis:
    Time:  O(V + E) -- every node is cloned once and every edge is visited
    once (twice if you count both directions of the undirected edge, still
    O(E)).
    Space: O(V) for the hash map and the recursion stack / BFS queue, plus
    O(V + E) for the output graph itself.

Alternative Approach (BFS):
Use a queue-based traversal instead of recursion. Create the clone of the
starting node up front, push the original start node onto a queue, and
while the queue is non-empty, pop a node, iterate its neighbors, cloning
any neighbor not yet in `old_to_new` and pushing the *original* neighbor
onto the queue for further exploration. This avoids recursion depth issues
for very large graphs (though the constraint of <= 100 nodes here makes
that a non-issue) and is otherwise equivalent in complexity.
"""

from collections import deque
from typing import Dict, List, Optional


class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List["Node"]] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node: Optional[Node]) -> Optional[Node]:
    """Return a deep copy of the connected undirected graph via DFS."""
    if node is None:
        return None

    old_to_new: Dict[Node, Node] = {}

    def dfs(cur: Node) -> Node:
        if cur in old_to_new:
            return old_to_new[cur]

        copy = Node(cur.val)
        old_to_new[cur] = copy
        for neighbor in cur.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy

    return dfs(node)


def clone_graph_bfs(node: Optional[Node]) -> Optional[Node]:
    """Alternative BFS-based deep copy of the graph."""
    if node is None:
        return None

    old_to_new: Dict[Node, Node] = {node: Node(node.val)}
    queue = deque([node])

    while queue:
        cur = queue.popleft()
        for neighbor in cur.neighbors:
            if neighbor not in old_to_new:
                old_to_new[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            old_to_new[cur].neighbors.append(old_to_new[neighbor])

    return old_to_new[node]


# ---------- Test helpers: build/serialize graphs from adjacency lists ----------

def build_graph(adj_list: List[List[int]]) -> Optional[Node]:
    """Build a graph from an adjacency list (1-indexed vals) and return node 1."""
    if not adj_list:
        return None

    nodes = {i + 1: Node(i + 1) for i in range(len(adj_list))}
    for i, neighbors in enumerate(adj_list):
        nodes[i + 1].neighbors = [nodes[n] for n in neighbors]
    return nodes[1]


def serialize(node: Optional[Node]) -> List[List[int]]:
    """Serialize a graph back into an adjacency list sorted by node val."""
    if node is None:
        return []

    visited: Dict[int, Node] = {}
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.val in visited:
            continue
        visited[cur.val] = cur
        for neighbor in cur.neighbors:
            if neighbor.val not in visited:
                stack.append(neighbor)

    return [
        sorted(n.val for n in visited[val].neighbors)
        for val in sorted(visited.keys())
    ]


def assert_deep_copy(original: Optional[Node], copy: Optional[Node]) -> None:
    """Verify `copy` is a structurally identical but distinct-object graph."""
    if original is None:
        assert copy is None
        return

    assert copy is not None
    assert original is not copy

    visited_pairs = {}
    stack = [(original, copy)]
    while stack:
        o, c = stack.pop()
        if id(o) in visited_pairs:
            continue
        visited_pairs[id(o)] = c
        assert o.val == c.val
        assert o is not c
        assert len(o.neighbors) == len(c.neighbors)
        o_sorted = sorted(o.neighbors, key=lambda x: x.val)
        c_sorted = sorted(c.neighbors, key=lambda x: x.val)
        for on, cn in zip(o_sorted, c_sorted):
            stack.append((on, cn))


if __name__ == "__main__":
    for solve in (clone_graph, clone_graph_bfs):
        # Example 1: 4-node cycle graph
        adj = [[2, 4], [1, 3], [2, 4], [1, 3]]
        original = build_graph(adj)
        copy = solve(original)
        assert serialize(copy) == [sorted(x) for x in adj]
        assert_deep_copy(original, copy)

        # Example 2: single node, no neighbors
        adj_single = [[]]
        original_single = build_graph(adj_single)
        copy_single = solve(original_single)
        assert serialize(copy_single) == [[]]
        assert_deep_copy(original_single, copy_single)

        # Example 3: empty graph
        assert solve(None) is None

        # Larger graph: triangle plus a pendant node
        # 1-2, 2-3, 3-1, 3-4
        adj_larger = [[2, 3], [1, 3], [1, 2, 4], [3]]
        original_larger = build_graph(adj_larger)
        copy_larger = solve(original_larger)
        assert serialize(copy_larger) == [sorted(x) for x in adj_larger]
        assert_deep_copy(original_larger, copy_larger)

    print("All tests passed.")
