"""
179. Largest Number
Difficulty: Medium
Topics: Array, String, Greedy, Sorting

Problem:
Given a list of non-negative integers nums, arrange them such that they form
the largest number and return it. Since the result may be very large, return
a string instead of an integer.

Example 1:
    Input: nums = [10, 2]
    Output: "210"
Example 2:
    Input: nums = [3, 30, 34, 5, 9]
    Output: "9534330"

Constraints:
    1 <= nums.length <= 100
    0 <= nums[i] <= 10^9

Approach:
Define a custom ordering: string a should come before b if a+b > b+a.
This comparator is a valid total preorder (transitive), so sorting by it
and concatenating gives the maximum number. Exchange argument: if some
adjacent pair violates the order, swapping them does not decrease the result.
Edge case: if the largest element is 0, all are 0 -> return "0".

Complexity:
    Time:  O(n log n * L) where L is max digit length (<= 10)
    Space: O(n * L)
"""
from functools import cmp_to_key
from typing import List


class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        strs = [str(x) for x in nums]
        strs.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)))
        if strs[0] == "0":
            return "0"
        return "".join(strs)

    # Alternative: pad-key trick. Constraint is <= 10 digits, so repeating each
    # string to length 10 and sorting descending lexicographically matches the
    # a+b vs b+a comparison.
    def largestNumberKey(self, nums: List[int]) -> str:
        strs = sorted((str(x) for x in nums), key=lambda s: s * 10, reverse=True)
        res = "".join(strs)
        return "0" if res[0] == "0" else res


if __name__ == "__main__":
    s = Solution()
    for f in (s.largestNumber, s.largestNumberKey):
        assert f([10, 2]) == "210"
        assert f([3, 30, 34, 5, 9]) == "9534330"
        assert f([0, 0]) == "0"
        assert f([0]) == "0"
        assert f([1]) == "1"
        assert f([121, 12]) == "12121"
        assert f([824, 8247]) == "8248247"
        assert f([999999998, 999999997, 999999999]) == "999999999999999998999999997"
    print("All tests passed.")
