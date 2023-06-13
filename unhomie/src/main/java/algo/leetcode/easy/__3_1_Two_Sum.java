package algo.leetcode.easy;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class __3_1_Two_Sum {

    public static void main(String[] args) {
        int[] nums = {7, 11, 2, 15};
        int target = 9;
        Solution_1 s = new Solution_1();
        int[] res =  s.twoSum(nums, target);

        System.out.println(Arrays.toString(res));

    }

    static class Solution_1 {
        public int[] twoSum(int[] nums, int target) {
            Map<Integer, Integer> mapNums = new HashMap<>();
            for (int i = 0; i < nums.length; i++) {
                if (mapNums.containsKey(target - nums[i]))
                    return new int[] {mapNums.get(target - nums[i]), i};
                mapNums.put(nums[i], i);
            }
            return new int[]{0, 0};
        }
    }
}
