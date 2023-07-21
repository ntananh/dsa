package algo.leetcode.medium;

/*
 * Idea     : store prefix and postfix product of current value
 * Improve  : we can use the same array to store result, loop for prefix first then postfix after
 *
 * input    : [ 1 | 2 | 3 | 4 ]
 * prefix   : [ 1 | 1 | 2 | 6 ]
 * postfix  : [ 24| 12| 4 | 4 ]
 * output   : [ 24| 12| 8 | 6 ]
 */
public class __6_238_Product_of_Array_Except_Self {
    public static int[] productExceptSelf(int[] nums) {
        int[] answers = new int[nums.length];
        int prefix = 1;
        for (int i = 0; i < nums.length; i++) {
            answers[i] = prefix;
            prefix *= nums[i];
        }

        int postfix = 1;
        for (int i = nums.length - 1; i >= 0; i--) {
            answers[i] *= postfix;
            postfix *= nums[i];
        }

        return answers;
    }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4};
        int[] result = productExceptSelf(nums);
        for (int n : result) {
            System.out.print(n);
        }
    }
}
