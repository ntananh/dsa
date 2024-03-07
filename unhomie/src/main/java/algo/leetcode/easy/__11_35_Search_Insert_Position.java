package algo.leetcode.easy;

public class __11_35_Search_Insert_Position {

	public static int searchInsert(int[] nums, int target) {
		if (nums == null || nums.length == 0) return 0;

		int l = 0, r = nums.length;

		while (l < r) {

			int mid = l + (r - l) / 2;

			if (nums[mid] == target) return mid;
			else if (nums[mid] > target)  r = mid;
			else l = mid + 1;
		}

		return l;
	}

	public static void main(String[] args) {
		final int[] nums = {1, 3, 5, 6};
		final int target = 2;

		int result = searchInsert(nums, target);
		System.out.println(result);
	}
}
