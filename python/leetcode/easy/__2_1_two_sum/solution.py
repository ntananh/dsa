"""1. Two Sum (Easy)

Time:  O(n), one pass, each dict lookup and insert is O(1) on average.
Space: O(n), the dict holds up to n - 1 values before the pair is found.
"""


# @lc code=start
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # Look up the complement before storing the current value,
        # so a value is never paired with itself ([3, 3], target 6).
        seen: dict[int, int] = {}
        for index, value in enumerate(nums):
            complement = target - value
            if complement in seen:
                return [seen[complement], index]
            seen[value] = index
        return []


# @lc code=end
