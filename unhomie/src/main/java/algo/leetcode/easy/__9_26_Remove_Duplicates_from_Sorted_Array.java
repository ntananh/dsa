package algo.leetcode.easy;

public class __9_26_Remove_Duplicates_from_Sorted_Array {
	public static int removeDuplicates(int[] nums) {
		int j = 1;

		for (int i = 1; i < nums.length; i++) {
			if (nums[i] != nums[i - 1]) {
				nums[j] = nums[i];
				j++;
			}
		}
		return j;
	}

	public static void main(String[] args) {
		int[] input = {0, 0, 1, 1, 1, 2, 2, 3};
		System.out.println(removeDuplicates(input));
	}
}
