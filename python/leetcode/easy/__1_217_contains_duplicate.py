"""217. Contains Duplicate. https://leetcode.com/problems/contains-duplicate/"""

import pytest


class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(set(nums)) < len(nums)


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], False),
        ([1], False),
        ([1, 2, 3, 4], False),
        ([1, 2, 3, 1], True),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
    ],
)
def test_contains_duplicate(nums: list[int], expected: bool) -> None:
    assert Solution().containsDuplicate(nums) is expected
