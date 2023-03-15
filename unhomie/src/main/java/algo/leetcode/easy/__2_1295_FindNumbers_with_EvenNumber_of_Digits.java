package algo.leetcode.easy;

public class __2_1295_FindNumbers_with_EvenNumber_of_Digits {
    public static void main(String[] args) {
        Solution s = new Solution();
        int[] nums = {12, 345, 2, 6, 7896};
        int res = s.findNumbers(nums);
        System.out.println(res);
    }

}

class Solution {
    public int findNumbers(int[] nums) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            String str_num = Integer.toString(nums[i]);
            if (str_num.length() % 2 == 0){
                count++;
            }
        }
        return count;
    }
}