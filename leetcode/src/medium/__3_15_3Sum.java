package medium;

import java.util.*;

public class __3_15_3Sum {
    public static void main(String[] args) {
        Solution_15 s = new Solution_15();
        int[] nums = {-1, 0, 1, 2, -1, -4};
        List<List<Integer>> b = s.threeSum(nums);

        System.out.println(b);
    }
}

class Solution_15 {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new LinkedList();
        for (int i = 0; i < nums.length - 2; i++) {
            if ((i == 0) || (i > 0) && (nums[i] != nums[i - 1])) {
                int low = i + 1;
                int high = nums.length - 1;
                int sum_tmp = 0 - nums[i];

                while (low < high){
                    if (nums[low] + nums[high] == sum_tmp){
                        res.add(Arrays.asList(nums[i], nums[low], nums[high]));
                        while ((low < high) && nums[low] == nums[low + 1]) low++;
                        while ((low < high) && nums[high] == nums[high - 1]) high--;
                        low++;
                        high--;
                    }else if (nums[low] + nums[high] < sum_tmp){
                        low++;
                    }
                    else{
                        high--;
                    }
                }
            }
        }
        return res;
    }
}