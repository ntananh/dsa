package algo.leetcode.easy;

import java.util.Arrays;
import java.util.HashMap;

public class __3_1_Two_Sum {

    public static void main(String[] args) {
        int[] nums = {7, 11, 2, 15};
        int target = 9;
        Solution_1 s = new Solution_1();
        int[] res =  s.twoSum(nums, target);

        System.out.println(Arrays.toString(res));

    }
}

class Solution_1 {
    public int[] twoSum(int[] nums, int target) {
        HashMap<Integer, Integer> dict = new HashMap<Integer, Integer>();
        for (int i = 0; i < nums.length; i++) {
           int complement = target - nums[i];
           if (dict.containsKey(complement)) {
               return new int[] {dict.get(complement), i};
           }
           dict.put(nums[i], i);
        }
        throw new IllegalArgumentException("No two sum solution");
    }
}