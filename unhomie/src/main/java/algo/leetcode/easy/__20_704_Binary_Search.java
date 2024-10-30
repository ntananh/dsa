package algo.leetcode.easy;

public class __20_704_Binary_Search {
	public static int search(int[] nums, int target) {
		int l = 0, r = nums.length - 1;
		while (l <= r) {
			int mid = l + (r - l) / 2;
			if (target == nums[mid]) {
				return mid;
			} else if (target > nums[mid]) {
				l = mid + 1;
			} else {
				r = mid - 1;
			}
		}

		return -1;
	}
}
