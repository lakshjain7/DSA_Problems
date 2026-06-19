def find_connected_components_dfs(graph):
    """
    Find all connected components using DFS
    
    Args:
        graph: Dictionary representation {vertex: [neighbors]}
    
    Returns:
        List of connected components, each component is a list of vertices
    """
    visited = set()
    components = []
    
    def dfs(vertex, current_component):
        """DFS helper function to explore component"""
        visited.add(vertex)
        current_component.append(vertex)
        
        # Visit all unvisited neighbors
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs(neighbor, current_component)
    
    # Find all components
    for vertex in graph:
        if vertex not in visited:
            component = []
            dfs(vertex, component)
            components.append(component)
    
    return components

def is_connected(graph):
    """Check if graph is connected (has only one component)"""
    components = find_connected_components_dfs(graph)
    return len(components) == 1

# Example 1: Simple Disconnected Graph
print("=" * 60)
print("EXAMPLE 1: Simple Disconnected Graph")
print("=" * 60)

graph1 = {
    'A': ['B', 'C'],
    'B': ['A', 'C'],
    'C': ['A', 'B'],
    'D': ['E'],
    'E': ['D'],
    'F': []  # Isolated vertex
}

print("Graph 1:")
for vertex, neighbors in graph1.items():
    print(f"  {vertex} -> {neighbors}")

components1 = find_connected_components_dfs(graph1)
print(f"\nConnected Components (DFS): {components1}")
print(f"Number of components: {len(components1)}")
print(f"Is connected: {is_connected(graph1)}")


