def find_articulation_points(graph):
    """
    Find all articulation points using Tarjan's algorithm
    
    Args:
        graph: Dictionary representation {vertex: [neighbors]}
    
    Returns:
        Set of articulation points
    """
    if not graph:
        return set()
    
    # Initialize data structures
    visited = set()
    disc = {}      # Discovery times
    low = {}       # Low values
    parent = {}    # Parent in DFS tree
    ap = set()     # Articulation points
    time = [0]     # Current time (using list for mutable reference)
    
    def dfs(u):
        # Count children of current vertex in DFS tree
        children = 0
        
        # Mark current vertex as visited
        visited.add(u)
        
        # Initialize discovery time and low value
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        # Explore all adjacent vertices
        for v in graph.get(u, []):
            if v not in visited:
                # v is not visited, so it becomes child of u in DFS tree
                children += 1
                parent[v] = u
                
                # Recursively explore subtree rooted at v
                dfs(v)
                
                # Update low value of u based on subtree rooted at v
                low[u] = min(low[u], low[v])
                
                # Check articulation point conditions
                
                # Condition 1: u is root and has more than one child
                if u not in parent and children > 1:
                    ap.add(u)
                
                # Condition 2: u is not root and low[v] >= disc[u]
                if u in parent and low[v] >= disc[u]:
                    ap.add(u)
            
            elif v != parent.get(u):
                # v is visited and not parent of u, so (u,v) is back edge
                # Update low value of u
                low[u] = min(low[u], disc[v])
    
    # Start DFS from all unvisited vertices (for disconnected graphs)
    for vertex in graph:
        if vertex not in visited:
            dfs(vertex)
    
    return ap


print("=" * 70)
print("EXAMPLE 1: Simple Graph with Articulation Points")
print("=" * 70)

# Graph structure:
#     A
#    / \
#   B   C
#   |   |
#   D   E
#       |
#       F

graph1 = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'E'],
    'D': ['B'],
    'E': ['C', 'F'],
    'F': ['E']
}

print("Graph 1:")
for vertex, neighbors in graph1.items():
    print(f"  {vertex} -> {neighbors}")

print("\nFinding articulation points...")
ap1 = find_articulation_points(graph1)
print(f"Articulation Points: {ap1}")
