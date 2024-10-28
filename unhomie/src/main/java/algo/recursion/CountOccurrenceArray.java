package algo.recursion;

public class CountOccurrenceArray {
	public static int count(int[] nums, int target, int index) {
		if (index == nums.length - 1) return 0;
		if (nums[index] == target) {
			return 1 + count(nums, 2, index + 1);
		}
		return count(nums, 2, index + 1);
	}

	public static int count(String s, char target, int index) {
		if (index == s.length() - 1) return 0;
		if (s.charAt(index) == target) {
			return 1 + count(s, target, index + 1);
		}
		return count(s, target, index + 1);
	}
}
