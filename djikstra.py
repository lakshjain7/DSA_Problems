def dijkstra(graph, start):
    """
    Dijkstra's algorithm without heapq.
    Graph is an adjacency list: {node: [(neighbor, weight), ...]}
    """
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    visited = set()
    
    while len(visited) < len(graph):
        # Find the unvisited node with the smallest distance
        u = None
        min_dist = float('inf')
        for node in graph:
            if node not in visited and dist[node] < min_dist:
                u = node
                min_dist = dist[node]
        
        if u is None:
            break  # All remaining nodes are inaccessible from start
        
        visited.add(u)
        
        for neighbor, weight in graph[u]:
            if neighbor not in visited:
                if dist[u] + weight < dist[neighbor]:
                    dist[neighbor] = dist[u] + weight
    
    return dist

# Example graph
graph = {
    'A': [('B', 4), ('C', 1)],
    'B': [('A', 4), ('C', 2), ('D', 5)],
    'C': [('A', 1), ('B', 2), ('D', 8)],
    'D': [('B', 5), ('C', 8)]
}

# Run Dijkstra's algorithm
start_node = 'A'
distances = dijkstra(graph, start_node)
print(f"Shortest distances from {start_node}:")
for node, d in distances.items():
    print(f"  {node}: {d}")
