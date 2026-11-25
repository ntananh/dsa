"""217. Contains Duplicate (Easy)

Time:  O(?)
Space: O(?)
"""


# @lc code=start
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(set(nums)) < len(nums)


# @lc code=end
