package algo.leetcode.easy;

public class __31_3151_Special_Array_I {

    /**
     * Special if every pair of its adjacent elements contains two numbers with different parity.
     * Parity means (nums[i] is odd and nums[i + 1] is even and vice versa)
     * @param nums input array
     * @return {@code true} if array is special
     */
    public boolean isArraySpecial(int[] nums) {
        for (int i = 1; i < nums.length; i++) {
            if (nums[i - 1] % 2 == nums[i] % 2) {
                return false;
            }
        }

        return true;
    }
}
