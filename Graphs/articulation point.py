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
    
    visited = set()
    disc = {}      # Discovery times
    low = {}       # Low values
    parent = {}    # Parent in DFS tree
    ap = set()     # Articulation points
    time = [0]     # Current time (using list for mutable reference)
    
    def dfs(u):
        children = 0
        visited.add(u)
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        for v in graph.get(u, []):
            if v not in visited:
                children += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                
                if u not in parent and children > 1:
                    ap.add(u)
                if u in parent and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])
    
    for vertex in graph:
        if vertex not in visited:
            dfs(vertex)
    
    return ap


print("=" * 70)
print("EXAMPLE 1: Simple Graph with Articulation Points")
print("=" * 70)

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
