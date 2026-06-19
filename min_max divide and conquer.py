def find_min_max(arr, low, high):
    """Find minimum and maximum using divide and conquer"""
    # Base case: only one element
    if low == high:
        return arr[low], arr[low]
    
    # Base case: two elements
    if high == low + 1:
        if arr[low] > arr[high]:
            return arr[high], arr[low]
        else:
            return arr[low], arr[high]
    
    # Divide
    mid = (low + high) // 2
    min1, max1 = find_min_max(arr, low, mid)
    min2, max2 = find_min_max(arr, mid + 1, high)
    
    # Conquer
    return min(min1, min2), max(max1, max2)

# Example usage
arr = [3, 5, 1, 9, 7, 2, 8]
min_val, max_val = find_min_max(arr, 0, len(arr) - 1)
print(f"Min: {min_val}, Max: {max_val}")
