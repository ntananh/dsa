package algo.recursion;

public class FindMax {
	public static int max(int[] nums, int index) {
		if (index == nums.length - 1) return nums[index];
		int maxInRest = max(nums, index + 1);
		return Math.max(nums[index], maxInRest);
	}
}
