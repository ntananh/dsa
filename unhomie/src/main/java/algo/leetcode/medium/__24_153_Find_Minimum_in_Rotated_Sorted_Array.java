package algo.leetcode.medium;

public class __24_153_Find_Minimum_in_Rotated_Sorted_Array {


	/**
	 * <p>
	 * Given an array of length {@code n} that is sorted in ascending order and
	 * then <b>rotated</b> between {@code 1} and {@code n} times:
	 * </p>
	 *
	 * <p>Examples:</p>
	 * <ul>
	 *      <li>{@code nums = [0, 1, 2, 4, 5, 6, 7]} becomes {@code [4, 5, 6, 7, 0, 1, 2]}
	 *          if rotated {@code 4} times.</li>
	 *      <li>{@code nums = [0, 1, 2, 4, 5, 6, 7]} remains unchanged if rotated {@code 7} times.</li>
	 * </ul>
	 *
	 * <p>
	 * Notice rotating {@code [a[0], a[1], a[2], ..., a[n-1]] } <b>1 time</b> results is {@code [a[n-1], a[0], a[1], a[2], ..., a[n-2]] }.
	 * </p>
	 *
	 * <p>
	 * You are given the rotated sorted array {@code nums} of unique elements. The task
	 * is to return <i>the minimum element</i> of this array.
	 * </p>
	 *
	 * <p><b>Note:</b> You must implement an algorithm with a time complexity of {@code O(log n)}.</p>
	 *
	 * @param nums A rotated sorted array of unique integers in ascending order.
	 * @return The minimum element in the array.
	 */
	public int findMin(int[] nums) {
		int l = 0;
		int r = nums.length - 1;
		int res = nums[0];

		while (l <= r) {
			if (nums[l] < nums[r]) {
				res = Math.min(nums[l], res);
				break;
			}

			int mid = l + (r - l) / 2;
			res = Math.min(nums[mid], res);
			if (nums[l] <= nums[mid]) {
				l = mid + 1;
			} else {
				r = mid - 1;
			}
		}

		return res;
	}
}
