"""
321. Create Maximum Number
Difficulty: Hard
Topics: Array, Two Pointers, Stack, Greedy, Monotonic Stack

Problem:
You are given two integer arrays nums1 and nums2 of lengths m and n
respectively. nums1 and nums2 represent the digits of two numbers. You are also
given an integer k.

Create the maximum number of length k <= m + n from digits of the two numbers.
The relative order of the digits from the same array must be preserved.
Return an array of the k digits representing the answer.

Example 1:
    Input: nums1 = [3,4,6,5], nums2 = [9,1,2,5,8,3], k = 5
    Output: [9,8,6,5,3]
Example 2:
    Input: nums1 = [6,7], nums2 = [6,0,4], k = 5
    Output: [6,7,6,0,4]
Example 3:
    Input: nums1 = [3,9], nums2 = [8,9], k = 3
    Output: [9,8,9]

Constraints:
    m == nums1.length, n == nums2.length
    1 <= m, n <= 500
    0 <= nums1[i], nums2[i] <= 9
    1 <= k <= m + n

Approach:
    Split k as i digits from nums1 and k-i from nums2, for every feasible i.
    1) pick(nums, t): the lexicographically largest subsequence of length t,
       using a monotonic stack that may drop at most len(nums)-t elements.
    2) merge(a, b): build the largest merged sequence; when heads tie, compare
       the remaining suffixes lexicographically and take from the larger one.
    3) Keep the best merged candidate over all splits.

Complexity:
    Time:  O((m+n) * k^2) worst case (merge suffix compares), typically less
    Space: O(k)
"""
from itertools import product
from typing import List


def maxNumber(nums1: List[int], nums2: List[int], k: int) -> List[int]:
    def pick(nums: List[int], t: int) -> List[int]:
        drop = len(nums) - t
        stack: List[int] = []
        for x in nums:
            while drop and stack and stack[-1] < x:
                stack.pop()
                drop -= 1
            stack.append(x)
        return stack[:t]

    def merge(a: List[int], b: List[int]) -> List[int]:
        res = []
        while a or b:
            # list comparison handles ties by comparing remaining suffixes
            big = a if a > b else b
            res.append(big.pop(0))
        return res

    m, n = len(nums1), len(nums2)
    best: List[int] = []
    for i in range(max(0, k - n), min(k, m) + 1):
        cand = merge(pick(nums1, i), pick(nums2, k - i))
        if cand > best:
            best = cand
    return best


# Alternative approach: brute force (exponential), used to validate on small input.
def maxNumberBrute(nums1: List[int], nums2: List[int], k: int) -> List[int]:
    m, n = len(nums1), len(nums2)
    best: List[int] = []
    # choose which positions of the interleaving come from nums1
    for mask in range(1 << (m + n)):
        if bin(mask).count("1") != m:
            continue
        i = j = 0
        seq = []
        for p in range(m + n):
            if mask >> p & 1:
                seq.append(nums1[i]); i += 1
            else:
                seq.append(nums2[j]); j += 1
        # best subsequence of length k from seq = greedy stack
        drop = len(seq) - k
        st: List[int] = []
        for x in seq:
            while drop and st and st[-1] < x:
                st.pop(); drop -= 1
            st.append(x)
        st = st[:k]
        # an interleaving's subsequence is valid; subsequence preserves order
        if st > best:
            best = st
    return best


if __name__ == "__main__":
    assert maxNumber([3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5) == [9, 8, 6, 5, 3]
    assert maxNumber([6, 7], [6, 0, 4], 5) == [6, 7, 6, 0, 4]
    assert maxNumber([3, 9], [8, 9], 3) == [9, 8, 9]
    assert maxNumber([0], [0], 1) == [0]
    assert maxNumber([1], [2], 2) == [2, 1]
    assert maxNumber([8, 9], [3, 9], 3) == [9, 8, 9]
    assert maxNumber([2, 5, 6, 4, 4, 0], [7, 3, 8, 0, 6, 5, 7, 6, 2], 15) == \
        [7, 3, 8, 2, 5, 6, 4, 4, 0, 6, 5, 7, 6, 2, 0]
    # cross-check against brute force on random small inputs
    import random
    random.seed(1)
    for _ in range(150):
        a = [random.randint(0, 9) for _ in range(random.randint(1, 5))]
        b = [random.randint(0, 9) for _ in range(random.randint(1, 5))]
        kk = random.randint(1, len(a) + len(b))
        assert maxNumber(a, b, kk) == maxNumberBrute(a, b, kk), (a, b, kk)
    print("All tests passed.")
