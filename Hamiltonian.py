def find_hamiltonian_cycles(graph):
    """
    Find all Hamiltonian cycles in the given undirected graph.

    Args:
        graph (dict): Adjacency list representation of the graph.

    Returns:
        List of Hamiltonian cycles (each cycle is a list of vertices).
    """
    vertices = list(graph.keys())
    n = len(vertices)
    start_vertex = vertices[0]
    path = [start_vertex]
    all_cycles = []

    def is_safe(v, pos):
        # Check if vertex v can be added at position pos
        last_vertex = path[-1]
        if v not in graph[last_vertex]:
            return False  # Not adjacent

        if v in path:
            return False  # Already in path

        return True

    def solve(pos):
        if pos == n:
            # Check if last vertex connects back to start
            if start_vertex in graph[path[-1]]:
                all_cycles.append(path[:] + [start_vertex])  # Complete cycle
            return

        for v in vertices:
            if is_safe(v, pos):
                path.append(v)
                solve(pos + 1)
                path.pop()  # Backtrack

    solve(1)
    return all_cycles

# Example 1: Graph with Hamiltonian cycles
ham_graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C', 'D'],
    'C': ['B', 'D'],
    'D': ['A', 'B', 'C']
}

# Example 2: Graph with no Hamiltonian cycle
no_ham_graph = {
    'A': ['B'],
    'B': ['A', 'C'],
    'C': ['B']
}

# Run
print("Hamiltonian cycles in ham_graph:")
cycles1 = find_hamiltonian_cycles(ham_graph)
if cycles1:
    for cycle in cycles1:
        print(" -> ".join(cycle))
else:
    print("No Hamiltonian cycle found.")

print("\nHamiltonian cycles in no_ham_graph:")
cycles2 = find_hamiltonian_cycles(no_ham_graph)
if cycles2:
    for cycle in cycles2:
        print(" -> ".join(cycle))
else:
    print("No Hamiltonian cycle found.")
