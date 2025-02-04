package algo.leetcode.easy;

public class __32_1800_Maximum_Ascending_Subarray_Sum {
    /**
     * Given
     * @param nums integer array
     * @return maximum sum of ascending subarray in {@code nums}
     */
    public static int maxAscendingSum(int[] nums) {
        int max = nums[0], cur = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = nums[i] > nums[i - 1] ? cur + nums[i] : nums[i];
            max = Math.max(max, cur);
        }
        return max;
    }
}
