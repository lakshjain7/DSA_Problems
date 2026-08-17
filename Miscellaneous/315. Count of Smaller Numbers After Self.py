"""
315. Count of Smaller Numbers After Self
Difficulty: Hard
Topics: Array, Binary Indexed Tree (Fenwick), Segment Tree, Merge Sort,
        Divide and Conquer, Binary Search

Problem Statement
-----------------
Given an integer array nums, return an integer array counts where counts[i]
is the number of smaller elements to the right of nums[i].

Example 1:
    Input:  nums = [5,2,6,1]
    Output: [2,1,1,0]
    Explanation:
        To the right of 5 there are 2 smaller elements (2 and 1).
        To the right of 2 there is  1 smaller element  (1).
        To the right of 6 there is  1 smaller element  (1).
        To the right of 1 there are 0 smaller elements.

Example 2:
    Input:  nums = [-1]
    Output: [0]

Example 3:
    Input:  nums = [-1,-1]
    Output: [0,0]

Constraints:
    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4


Approach (Merge Sort / Count of Inversions)
-------------------------------------------
This is the classic "count inversions" problem, but each element needs its
own count rather than a single global total.

We sort indices (not values) with a merge sort. During the merge step we
combine two already-sorted halves, left and right, both ordered by value
ascending. When we are about to place a left-half element, every right-half
element already emitted is both to its right in the original array AND
smaller in value - exactly what we want to count.

Concretely, while merging ascending we keep a pointer j over the right
half. Whenever we place a left element, j counts how many right-half
elements have already been emitted (all smaller and originally to the
right), so we add j to that left index's answer.

Because we carry original indices through the sort, each index accumulates
the count contributed across every merge level.

Why it works:
- Merge sort touches every cross-half pair exactly once through the
  partition structure, and the "left index vs. emitted right elements"
  relationship during a merge is precisely "later position, smaller value".

Complexity
----------
Time:  O(n log n) - merge sort.
Space: O(n) for index buffers and the counts array.


Alternative Approach (Binary Indexed Tree)
------------------------------------------
Coordinate-compress the values, then scan from right to left. For each
value, query the BIT for how many already-seen values are strictly smaller
(a prefix sum), then add the current value to the BIT. Also O(n log n) time
and provided below as countSmaller_bit for cross-validation.
"""

from typing import List


def countSmaller(nums: List[int]) -> List[int]:
    n = len(nums)
    counts = [0] * n
    # indices[k] = original index; we sort these by nums value.
    indices = list(range(n))

    def merge_sort(lo: int, hi: int) -> List[int]:
        # Sort indices[lo:hi] by value; return the sorted sublist of indices.
        if hi - lo <= 1:
            return indices[lo:hi]

        mid = (lo + hi) // 2
        left = merge_sort(lo, mid)
        right = merge_sort(mid, hi)

        merged: List[int] = []
        i = j = 0
        # Merge ascending by value. Track how many right elements are
        # already consumed (they are smaller AND to the right).
        while i < len(left) and j < len(right):
            if nums[left[i]] <= nums[right[j]]:
                # 'j' right-side elements are smaller and to the right.
                counts[left[i]] += j
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        # Remaining left elements: all 'j' == len(right) right elements
        # were smaller and to their right.
        while i < len(left):
            counts[left[i]] += j
            merged.append(left[i])
            i += 1
        while j < len(right):
            merged.append(right[j])
            j += 1

        # Write the merged order back so parent merges see sorted indices.
        indices[lo:hi] = merged
        return merged

    if n > 0:
        merge_sort(0, n)
    return counts


def countSmaller_bit(nums: List[int]) -> List[int]:
    """Binary Indexed Tree (Fenwick) solution for cross-validation."""
    if not nums:
        return []

    sorted_vals = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_vals)}  # 1-based ranks
    size = len(sorted_vals)
    tree = [0] * (size + 1)

    def update(i: int) -> None:
        while i <= size:
            tree[i] += 1
            i += i & (-i)

    def query(i: int) -> int:
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    res = [0] * len(nums)
    for idx in range(len(nums) - 1, -1, -1):
        r = rank[nums[idx]]
        res[idx] = query(r - 1)  # count of strictly smaller seen so far
        update(r)
    return res


def _brute(nums: List[int]) -> List[int]:
    """O(n^2) reference used only in tests."""
    return [sum(1 for j in range(i + 1, len(nums)) if nums[j] < nums[i])
            for i in range(len(nums))]


if __name__ == "__main__":
    # Provided examples
    assert countSmaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert countSmaller([-1]) == [0]
    assert countSmaller([-1, -1]) == [0, 0]

    # Edge cases
    assert countSmaller([]) == []
    assert countSmaller([1, 2, 3, 4]) == [0, 0, 0, 0]      # already sorted asc
    assert countSmaller([4, 3, 2, 1]) == [3, 2, 1, 0]      # strictly descending
    assert countSmaller([2, 2, 2]) == [0, 0, 0]            # all equal
    assert countSmaller([3, 1, 2, 1]) == [3, 0, 1, 0]      # duplicates

    # Randomized cross-check against brute force and the BIT solution.
    import random
    random.seed(315)
    for _ in range(300):
        arr = [random.randint(-20, 20) for _ in range(random.randint(0, 40))]
        expected = _brute(arr)
        assert countSmaller(arr) == expected
        assert countSmaller_bit(arr) == expected

    print("All tests passed for 315. Count of Smaller Numbers After Self")
