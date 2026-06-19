def graph_coloring(graph, num_colors):
    """
    Graph coloring using backtracking. Finds all valid colorings.

    Args:
        graph (dict): Adjacency list of the graph.
        num_colors (int): Number of colors available.

    Returns:
        List of valid colorings (each as a dict), or empty list if no solution.
    """
    vertices = list(graph.keys())
    colors = {}
    all_solutions = []

    def is_safe(vertex, color):
        for neighbor in graph[vertex]:
            if neighbor in colors and colors[neighbor] == color:
                return False
        return True

    def solve(vertex_idx):
        if vertex_idx == len(vertices):
            all_solutions.append(colors.copy())
            return

        vertex = vertices[vertex_idx]
        for color in range(num_colors):
            if is_safe(vertex, color):
                colors[vertex] = color
                solve(vertex_idx + 1)
                del colors[vertex]

    solve(0)
    return all_solutions

# Example graph
color_graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

# Example usage
num_colors = 3
solutions = graph_coloring(color_graph, num_colors)

# Print results
if solutions:
    print(f"Found {len(solutions)} solutions with {num_colors} colors:")
    for idx, sol in enumerate(solutions, 1):
        print(f"Solution {idx}: {sol}")
else:
    print("No valid coloring found.")
