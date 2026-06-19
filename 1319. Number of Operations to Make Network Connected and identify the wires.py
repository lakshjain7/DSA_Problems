from typing import List, Union


class Solution:
    def rewireNetwork(self, n: int, connections: List[List[int]]) -> Union[dict, int]:
        """
        Given 'n' computers and their 'connections' (edges),
        this function finds:
          - Which redundant edges (extra cables) can be removed.
          - Which new edges need to be added to make the entire network connected.

        Returns a dictionary:
            {
                "remove": [list of edges to remove],
                "add": [list of edges to add]
            }

        If the network cannot be fully connected (not enough spare cables), returns -1.
        """

        # --- Step 1: Check if enough connections exist ---
        # To connect 'n' nodes, we need at least (n - 1) edges.
        if len(connections) < n - 1:
            return -1  # Not enough cables even if we rearrange

        # --- Step 2: Initialize Disjoint Set Union (Union-Find) structures ---
        parent = [i for i in range(n)]
        size = [1] * n  # Used for union by size optimization

        # Find function with path compression
        def find(u):
            if parent[u] != u:
                parent[u] = find(parent[u])
            return parent[u]

        # Union function that merges two sets and detects cycles
        def union(u, v):
            pu, pv = find(u), find(v)
            if pu == pv:
                return False  # This edge forms a cycle (redundant)
            if size[pu] < size[pv]:
                parent[pu] = pv
                size[pv] += size[pu]
            else:
                parent[pv] = pu
                size[pu] += size[pv]
            return True

        # --- Step 3: Process all edges ---
        # Store edges that form cycles (can be removed)
        extra_edges = []
        for u, v in connections:
            if not union(u, v):  # If u and v already connected
                extra_edges.append((u, v))  # This edge is redundant

        # --- Step 4: Identify unique disconnected components ---
        components = set(find(i) for i in range(n))  # each root is a component
        components = list(components)  # convert to list for indexing

        # --- Step 5: Plan new edges to connect components ---
        # We connect all components to the first one as a hub
        new_edges = []
        for i in range(1, len(components)):
            new_edges.append((components[0], components[i]))

        # --- Step 6: Check if we have enough spare (redundant) cables ---
        if len(extra_edges) < len(new_edges):
            return -1  # Not enough redundant cables to rewire

        # --- Step 7: Return rewire plan ---
        return {
            "remove": extra_edges[:len(new_edges)],  # cables we can remove
            "add": new_edges                         # cables to add for full connectivity
        }
