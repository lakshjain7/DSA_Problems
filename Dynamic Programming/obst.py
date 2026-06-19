def optimal_bst(keys, freq):
    n = len(keys)
    cost = [[0 for _ in range(n)] for _ in range(n)]
    root = [[-1 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        cost[i][i] = freq[i]
        root[i][i] = i
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float('inf')
            freq_sum = sum(freq[i:j+1])
            
            for r in range(i, j + 1):
                left = cost[i][r-1] if r > i else 0
                right = cost[r+1][j] if r < j else 0
                temp_cost = left + right + freq_sum
                
                if temp_cost < cost[i][j]:
                    cost[i][j] = temp_cost
                    root[i][j] = r

    # Reconstruct tree
    def build_tree(i, j):
        if i > j:
            return None
        r = root[i][j]
        node = {
            'key': keys[r],
            'left': build_tree(i, r-1),
            'right': build_tree(r+1, j)
        }
        return node

    tree = build_tree(0, n-1)

    return cost[0][n-1], tree

# Example usage
keys = [10, 12, 20]
freq = [34, 8, 50]
min_cost, tree = optimal_bst(keys, freq)
print(f"Minimum cost of optimal BST: {min_cost}")

def print_tree(node, indent=0):
    if not node:
        return
    print(' ' * indent + f"Key: {node['key']}")
    if node['left']:
        print(' ' * (indent + 2) + f"Left child of {node['key']}:")
        print_tree(node['left'], indent + 4)
    if node['right']:
        print(' ' * (indent + 2) + f"Right child of {node['key']}:")
        print_tree(node['right'], indent + 4)

print("\nOptimal BST Structure:")
print_tree(tree)
