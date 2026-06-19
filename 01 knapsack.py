def knapsack_01(weights, values, capacity):
    """0/1 Knapsack using dynamic programming, returns max value and solution set"""
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Build table dp[][] in bottom up manner
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], 
                               dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
    # Backtrack to find which items are included
    solution_set = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            solution_set.append(i-1)  # Item index included
            w -= weights[i-1]
    
    # Reverse solution set for original order
    solution_set.reverse()
    
    return dp[n][capacity], solution_set

# Example
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
max_value, solution_set = knapsack_01(weights, values, capacity)

print(f"Maximum value in knapsack: {max_value}")
print(f"Items included in knapsack: {solution_set}")

# Print the actual items in a readable format
for i in solution_set:
    print(f"Item {i}: weight={weights[i]}, value={values[i]}")
