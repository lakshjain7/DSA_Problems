"""
Problem: 55. Jump Game
Difficulty: Medium
Topics: Array, Greedy, Dynamic Programming

You are given an integer array nums. You are initially positioned at the
array's first index, and each element in the array represents your maximum
jump length at that position.
Return true if you can reach the last index, or false otherwise.

Example 1:
    Input: nums = [2,3,1,1,4]
    Output: true
    Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:
    Input: nums = [3,2,1,0,4]
    Output: false
    Explanation: You always arrive at index 3 whose max jump is 0.

Constraints:
    1 <= nums.length <= 10^4
    0 <= nums[i] <= 10^5
"""
from typing import List

# Approach (greedy, furthest reach):
#   Sweep left to right keeping `far`, the furthest index reachable so far.
#   If the current index i > far, i is unreachable, so the end is too.
#   Otherwise update far = max(far, i + nums[i]). Reachable positions form a
#   contiguous prefix [0, far], so tracking one number is sufficient.
#
# Complexity: Time O(n), Space O(1).


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        far = 0
        for i, jump in enumerate(nums):
            if i > far:
                return False
            far = max(far, i + jump)
            if far >= len(nums) - 1:
                return True
        return True

    # Alternative: work backwards, tracking the leftmost "good" index.
    # Same O(n) time, O(1) space.
    def canJumpBackward(self, nums: List[int]) -> bool:
        goal = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0


if __name__ == "__main__":
    s = Solution()
    for f in (s.canJump, s.canJumpBackward):
        assert f([2, 3, 1, 1, 4]) is True
        assert f([3, 2, 1, 0, 4]) is False
        assert f([0]) is True
        assert f([0, 1]) is False
        assert f([1, 0]) is True
        assert f([2, 0, 0]) is True
        assert f([1, 1, 0, 1]) is False
        assert f([5, 0, 0, 0, 0, 0]) is True
    print("All tests passed.")
