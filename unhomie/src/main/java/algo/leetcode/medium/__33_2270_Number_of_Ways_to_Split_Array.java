package algo.leetcode.medium;

public class __33_2270_Number_of_Ways_to_Split_Array {

    /**
     * <p>
     * Given {@code nums[], nums.length = n }.
     * {@code nums } contains a valid split at index i if the following are true:
     * Sum of the first i + 1 elements >= sum of the last n - i - 1 elements. {@code sum(i + i) >= sum(n - i - 1)}
     * There is at least one element to the right of i. That is, 0 <= i < n - 1.
     * </p>
     *
     * @param nums input array
     * @return the number of valid splits in nums.
     */
    public static int waysToSplitArray(int[] nums) {
        long totalSum = 0, left = 0;
        for (int num : nums) totalSum += num;

        int res = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            left += nums[i];
            if (left >= totalSum - left) res++;
        }

        return res;
    }
}
