"""
189. Rotate Array
Difficulty: Medium
Topics: Array, Math, Two Pointers

Problem:
Given an integer array nums, rotate the array to the right by k steps,
where k is non-negative. Modify nums in place.

Example 1:
    Input: nums = [1,2,3,4,5,6,7], k = 3
    Output: [5,6,7,1,2,3,4]
Example 2:
    Input: nums = [-1,-100,3,99], k = 2
    Output: [3,99,-1,-100]

Constraints:
    1 <= nums.length <= 10^5
    -2^31 <= nums[i] <= 2^31 - 1
    0 <= k <= 10^5

Approach (three reversals):
    Reverse the whole array, then reverse the first k elements and the
    remaining n-k elements. Reversing the whole array moves the last k items
    to the front (in reversed order); the two partial reversals fix the order.
    k is reduced modulo n first.

Complexity: Time O(n), Space O(1).
"""
from typing import List


def rotate(nums: List[int], k: int) -> None:
    n = len(nums)
    k %= n

    def rev(l: int, r: int) -> None:
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1

    rev(0, n - 1)
    rev(0, k - 1)
    rev(k, n - 1)


# Alternative: cyclic replacements (O(n) time, O(1) space)
def rotate_cyclic(nums: List[int], k: int) -> None:
    n = len(nums)
    k %= n
    count = 0
    start = 0
    while count < n:
        cur, prev = start, nums[start]
        while True:
            nxt = (cur + k) % n
            nums[nxt], prev = prev, nums[nxt]
            cur = nxt
            count += 1
            if cur == start:
                break
        start += 1


if __name__ == "__main__":
    for fn in (rotate, rotate_cyclic):
        a = [1, 2, 3, 4, 5, 6, 7]; fn(a, 3); assert a == [5, 6, 7, 1, 2, 3, 4]
        a = [-1, -100, 3, 99]; fn(a, 2); assert a == [3, 99, -1, -100]
        a = [1]; fn(a, 5); assert a == [1]
        a = [1, 2]; fn(a, 0); assert a == [1, 2]
        a = [1, 2, 3, 4, 5, 6]; fn(a, 6); assert a == [1, 2, 3, 4, 5, 6]
        a = [1, 2, 3, 4, 5, 6]; fn(a, 8); assert a == [5, 6, 1, 2, 3, 4]
    print("All tests passed")
