# PRIM'S ALGORITHM
import heapq

def prims_mst(graph):
    """Prim's algorithm for MST"""
    vertices = list(graph.keys())
    start = vertices[0]
    
    visited = {start}
    edges = []
    mst = []
    total_cost = 0
    
    # Add all edges from start vertex
    for neighbor, weight in graph[start]:
        heapq.heappush(edges, (weight, start, neighbor))
    
    while edges and len(visited) < len(vertices):
        weight, u, v = heapq.heappop(edges)
        
        if v in visited:
            continue
            
        # Add edge to MST
        mst.append((u, v, weight))
        total_cost += weight
        visited.add(v)
        
        # Add new edges from v
        for neighbor, w in graph[v]:
            if neighbor not in visited:
                heapq.heappush(edges, (w, v, neighbor))
    
    return mst, total_cost

# KRUSKAL'S ALGORITHM
class UnionFind:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

def kruskals_mst(vertices, edges):
    """Kruskal's algorithm for MST"""
    edges.sort()  # Sort by weight
    uf = UnionFind(vertices)
    mst = []
    total_cost = 0
    
    for weight, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
            total_cost += weight
    
    return mst, total_cost

# Example graph for MST
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2)]
}

vertices = ['A', 'B', 'C', 'D', 'E']
edges = [(1, 'B', 'C'), (2, 'A', 'C'), (2, 'D', 'E'), (4, 'A', 'B'), 
         (5, 'B', 'D'), (8, 'C', 'D'), (10, 'C', 'E')]

prim_mst, prim_cost = prims_mst(graph)
kruskal_mst, kruskal_cost = kruskals_mst(vertices, edges)
print(f"Prim's MST: {prim_mst}, Cost: {prim_cost}")
print(f"Kruskal's MST: {kruskal_mst}, Cost: {kruskal_cost}")
