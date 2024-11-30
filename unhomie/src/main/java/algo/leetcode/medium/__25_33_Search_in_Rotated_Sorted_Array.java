package algo.leetcode.medium;

public class __25_33_Search_in_Rotated_Sorted_Array {


	/**
	 * <p>
	 * Given an rotated sorted array in ascending order (with <b>distinct</b> values).
	 * It has been rotated between {@code 1} and {@code n} times.
	 * </p>
	 *
	 * <ul>
	 * For example: array {@code nums = [1, 2, 3, 4, 5, 6]}
	 *   <li> {@code [3, 4, 5, 6, 1, 2]} if it was rotated {@code 4} times. </li>
	 *   <li> {@code [1, 2, 3, 4, 5, 6]} if it was rotated {@code 6} times. </li>
	 * </ul>
	 *
	 * <p>
	 * Problem statement: finding index of {@code target} in {@code nums}
	 * <b>Note: </b> the TS of search algorithm must {@code 0(log n)}
	 * </p>
	 *
	 * @param nums   the rotated sorted array
	 * @param target the target value
	 * @return the <i>index</i> of {@code target} if <i>it is</i> in {@code nums}, otherwise {@code -1}
	 */
	public static int search(int[] nums, int target) {
		if (nums == null || nums.length == 0) {
			return -1;
		}

		int pivot = findPivot(nums);

		int result = binarySearch(nums, target, 0, pivot - 1);
		if (result != -1) {
			return result;
		}

		return binarySearch(nums, target, pivot, nums.length - 1);
	}

	private static int findPivot(int[] nums) {
		int left = 0, right = nums.length - 1;

		if (nums[left] < nums[right]) {
			return 0;
		}

		while (left < right) {
			int mid = left + (right - left) / 2;
			if (nums[mid] > nums[right]) {
				left = mid + 1;
			} else {
				right = mid;
			}
		}
		return left;
	}

	private static int binarySearch(int[] nums, int target, int left, int right) {
		while (left <= right) {
			int mid = left + (right - left) / 2;
			if (nums[mid] == target) {
				return mid;
			} else if (nums[mid] < target) {
				left = mid + 1;
			} else {
				right = mid - 1;
			}
		}
		return -1;
	}
}
