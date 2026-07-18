"""
658. Find K Closest Elements
Difficulty: Medium
Topics: Array, Two Pointers, Binary Search, Sliding Window, Heap

------------------------------------------------------------------------
PROBLEM STATEMENT
------------------------------------------------------------------------
Given a sorted integer array arr, two integers k and x, return the k
closest integers to x in the array. The result should also be sorted in
ascending order.

An integer a is closer to x than an integer b if:
    - |a - x| < |b - x|, or
    - |a - x| == |b - x| and a < b

------------------------------------------------------------------------
EXAMPLES
------------------------------------------------------------------------
Example 1:
Input:  arr = [1,2,3,4,5], k = 4, x = 3
Output: [1,2,3,4]

Example 2:
Input:  arr = [1,2,3,4,5], k = 4, x = -1
Output: [1,2,3,4]

------------------------------------------------------------------------
CONSTRAINTS
------------------------------------------------------------------------
- 1 <= k <= arr.length
- 1 <= arr.length <= 10^4
- arr is sorted in ascending order.
- -10^4 <= arr[i], x <= 10^4

------------------------------------------------------------------------
APPROACH (Binary search for the left boundary of the window)
------------------------------------------------------------------------
Because arr is sorted and the answer is a contiguous window of length k
(the k closest values are always adjacent in a sorted array), we only need
to find the correct left boundary `lo` of that window. The result is then
arr[lo : lo + k].

We binary-search over the candidate left boundaries lo in [0, len(arr)-k].
For a midpoint `mid`, we compare the two ends of the window that would be
"pushed out" if we shifted right:

    - x - arr[mid]        -> distance from x to the left end
    - arr[mid + k] - x    -> distance from x to the element just past the
                             right end of the window starting at mid

If (x - arr[mid]) > (arr[mid + k] - x), then arr[mid] is farther from x
than arr[mid + k], so a better window lies to the right -> lo = mid + 1.
Otherwise the window starting at mid is at least as good -> hi = mid.

When lo == hi the search converges to the optimal left boundary. The
tie-breaking rule (prefer smaller a on equal distance) is handled
naturally: when the two distances are equal we keep the left window,
which contains the smaller elements.

Why it works: shifting the window right trades the leftmost element
(distance x - arr[mid]) for a new rightmost element (distance
arr[mid+k] - x). The total window "cost" is monotonic in the boundary, so
binary search finds the boundary where shifting no longer helps.

------------------------------------------------------------------------
COMPLEXITY
------------------------------------------------------------------------
Time:  O(log(n - k) + k) -- binary search over boundaries plus slicing k.
Space: O(1) extra (O(k) for the returned slice).
"""

from typing import List


def findClosestElements(arr: List[int], k: int, x: int) -> List[int]:
    lo, hi = 0, len(arr) - k
    while lo < hi:
        mid = (lo + hi) // 2
        # Compare the element leaving (arr[mid]) vs the element entering
        # (arr[mid + k]) if we were to slide the window one step right.
        if x - arr[mid] > arr[mid + k] - x:
            lo = mid + 1
        else:
            hi = mid
    return arr[lo:lo + k]


# ----------------------------------------------------------------------
# ALTERNATIVE APPROACH: two pointers shrinking from both ends
# ----------------------------------------------------------------------
# Start with the full array as the window and repeatedly discard whichever
# end is farther from x until exactly k elements remain. On ties (equal
# distance) we discard the right end, honoring the "smaller a wins" rule.
def findClosestElements_twoPointers(arr: List[int], k: int, x: int) -> List[int]:
    left, right = 0, len(arr) - 1
    while right - left + 1 > k:
        if x - arr[left] <= arr[right] - x:
            right -= 1
        else:
            left += 1
    return arr[left:right + 1]


if __name__ == "__main__":
    # Example 1
    assert findClosestElements([1, 2, 3, 4, 5], 4, 3) == [1, 2, 3, 4]
    assert findClosestElements_twoPointers([1, 2, 3, 4, 5], 4, 3) == [1, 2, 3, 4]

    # Example 2: x smaller than all elements
    assert findClosestElements([1, 2, 3, 4, 5], 4, -1) == [1, 2, 3, 4]
    assert findClosestElements_twoPointers([1, 2, 3, 4, 5], 4, -1) == [1, 2, 3, 4]

    # x larger than all elements -> take the largest k
    assert findClosestElements([1, 2, 3, 4, 5], 3, 100) == [3, 4, 5]
    assert findClosestElements_twoPointers([1, 2, 3, 4, 5], 3, 100) == [3, 4, 5]

    # k == len(arr): must return the whole array
    assert findClosestElements([2, 4, 6], 3, 5) == [2, 4, 6]
    assert findClosestElements_twoPointers([2, 4, 6], 3, 5) == [2, 4, 6]

    # k == 1: single closest element
    assert findClosestElements([1, 3, 8, 10], 1, 9) == [8]
    assert findClosestElements_twoPointers([1, 3, 8, 10], 1, 9) == [8]

    # Tie-breaking: equidistant -> prefer the smaller value
    # x = 3, both 2 and 4 are distance 1; k=1 should pick 2.
    assert findClosestElements([1, 2, 4, 5], 1, 3) == [2]
    assert findClosestElements_twoPointers([1, 2, 4, 5], 1, 3) == [2]

    # Duplicates in array
    assert findClosestElements([1, 1, 1, 10, 10, 10], 1, 9) == [10]
    assert findClosestElements_twoPointers([1, 1, 1, 10, 10, 10], 1, 9) == [10]

    # Negative values
    assert findClosestElements([-5, -3, 0, 2, 6], 3, -1) == [-3, 0, 2]
    assert findClosestElements_twoPointers([-5, -3, 0, 2, 6], 3, -1) == [-3, 0, 2]

    print("658. Find K Closest Elements: all tests passed!")
