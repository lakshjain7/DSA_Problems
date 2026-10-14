"""
31. Next Permutation
Difficulty: Medium
Topics: Array, Two Pointers

Problem:
    A permutation of an array of integers is an arrangement of its members into
    a sequence. The next permutation is the next lexicographically greater
    permutation. If no such arrangement exists (array is in descending order),
    rearrange to the lowest possible order (ascending). The replacement must be
    in place and use only constant extra memory.

Example 1:
    Input: nums = [1,2,3]   Output: [1,3,2]
Example 2:
    Input: nums = [3,2,1]   Output: [1,2,3]
Example 3:
    Input: nums = [1,1,5]   Output: [1,5,1]

Constraints:
    - 1 <= nums.length <= 100
    - 0 <= nums[i] <= 100

Approach (two pointers / suffix reversal):
    1. Scan from the right for the first index i with nums[i] < nums[i+1]; the
       suffix after i is non-increasing (the largest arrangement of itself).
    2. If none exists, the array is the last permutation: reverse it entirely.
    3. Otherwise find the rightmost j > i with nums[j] > nums[i] (smallest value
       bigger than nums[i] in the suffix), swap nums[i], nums[j].
    4. The suffix is still non-increasing; reverse it to make it the smallest.
    This is the minimal increase of the prefix, with the smallest possible tail.

Complexity:
    Time:  O(n)
    Space: O(1)

Alternative (brute force using itertools, for verification):
    Sort the distinct permutations and pick the successor - O(n! * n), only
    suitable for tiny inputs; used here to cross-check the main solution.
"""
from itertools import permutations
from typing import List


class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        l, r = i + 1, n - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1


def brute(nums: List[int]) -> List[int]:
    perms = sorted(set(permutations(nums)))
    idx = perms.index(tuple(nums))
    return list(perms[(idx + 1) % len(perms)])


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3], [1, 3, 2]),
        ([3, 2, 1], [1, 2, 3]),
        ([1, 1, 5], [1, 5, 1]),
        ([1], [1]),
        ([2, 2, 2], [2, 2, 2]),
        ([1, 3, 2], [2, 1, 3]),
        ([5, 4, 7, 5, 3, 2], [5, 5, 2, 3, 4, 7]),
    ]
    for inp, exp in cases:
        a = inp[:]
        s.nextPermutation(a)
        assert a == exp, (inp, a, exp)
    for arr in ([1, 2, 2, 3], [0, 1, 0], [3, 3, 1, 2], [1, 2, 3, 4]):
        a = arr[:]
        s.nextPermutation(a)
        assert a == brute(arr), (arr, a)
    print("All tests passed")
