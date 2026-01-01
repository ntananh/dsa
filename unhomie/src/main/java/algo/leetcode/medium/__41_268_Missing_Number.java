package algo.leetcode.medium;

public class __41_268_Missing_Number {
    public int missingNumber(final int[] nums) {
        final int n = nums.length;
        final int expectedSum = (n * (n + 1)) / 2;

        int realSum = 0;
        for (final int num : nums) {
            realSum += num;
        }

        return expectedSum - realSum;
    }
}
