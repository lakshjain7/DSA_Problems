"""
215. Kth Largest Element in an Array
Difficulty: Medium
Topics: Heap (Priority Queue), Quickselect, Divide and Conquer, Sorting

Problem Statement:
Given an integer array nums and an integer k, return the kth largest element
in the array.
Note that it is the kth largest element in sorted order, not the kth distinct
element.
You must solve it in O(n log n) time complexity or better (a linear-time
average solution is expected in industry interviews).

Examples:
    Example 1:
        Input: nums = [3,2,1,5,6,4], k = 2
        Output: 5
    Example 2:
        Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
        Output: 4

Constraints:
    1 <= k <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4

Approach (Min-Heap of size k):
    Maintain a min-heap containing the k largest elements seen so far. Push
    each element; whenever the heap grows beyond size k, pop the smallest.
    After processing all elements, the heap's root (smallest element in the
    heap) is exactly the kth largest element of the array, since the heap
    holds precisely the top k values.

Complexity Analysis:
    Time:  O(n log k) - each of the n elements triggers at most one push and
           one pop on a heap of size <= k.
    Space: O(k) - the heap holds at most k elements.

Alternative Approach (Quickselect):
    Based on the partition step of quicksort. To find the kth largest element,
    we equivalently look for the element at index (n - k) in the sorted
    array. Pick a pivot, partition the array so elements less than the pivot
    are on the left and elements greater are on the right, then recurse into
    only the half that contains the target index. A random pivot choice gives
    expected O(n) time, though worst case is O(n^2).
    Time: O(n) average, O(n^2) worst case. Space: O(1) extra (in-place).
"""

import heapq
import random
from typing import List


def find_kth_largest(nums: List[int], k: int) -> int:
    """Return the kth largest element using a min-heap of size k."""
    heap: List[int] = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def find_kth_largest_quickselect(nums: List[int], k: int) -> int:
    """Alternative: quickselect, expected O(n) time."""
    nums = nums[:]  # avoid mutating caller's list
    target_index = len(nums) - k  # index of kth largest in sorted order

    def partition(left: int, right: int, pivot_index: int) -> int:
        pivot_value = nums[pivot_index]
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        store_index = left
        for i in range(left, right):
            if nums[i] < pivot_value:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1
        nums[right], nums[store_index] = nums[store_index], nums[right]
        return store_index

    left, right = 0, len(nums) - 1
    while True:
        if left == right:
            return nums[left]
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)
        if pivot_index == target_index:
            return nums[pivot_index]
        elif pivot_index < target_index:
            left = pivot_index + 1
        else:
            right = pivot_index - 1


if __name__ == "__main__":
    for fn in (find_kth_largest, find_kth_largest_quickselect):
        assert fn([3, 2, 1, 5, 6, 4], 2) == 5, f"{fn.__name__} failed example 1"
        assert fn([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4, f"{fn.__name__} failed example 2"

        # Single element
        assert fn([1], 1) == 1, f"{fn.__name__} failed single element"

        # k == n (smallest element)
        assert fn([7, 10, 4, 3, 20, 15], 6) == 3, f"{fn.__name__} failed k==n"

        # k == 1 (largest element)
        assert fn([7, 10, 4, 3, 20, 15], 1) == 20, f"{fn.__name__} failed k==1"

        # All duplicates
        assert fn([2, 2, 2, 2], 3) == 2, f"{fn.__name__} failed duplicates"

        # Negative numbers
        assert fn([-1, -2, -3, -4], 2) == -2, f"{fn.__name__} failed negatives"

        # Larger mixed list
        assert fn([9, 3, 2, 4, 8], 3) == 4, f"{fn.__name__} failed mixed list"

        print(f"{fn.__name__}: all tests passed")

    print("All tests passed!")
