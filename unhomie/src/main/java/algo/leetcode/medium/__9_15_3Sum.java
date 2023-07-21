package algo.leetcode.medium;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

public class __9_15_3Sum {

    /*
     * Sort input, for each first element, find next two where -a = b+c.
     * If a == prevA => skip a
     * If b == prevB => skip b to eliminate duplicates;
     * To find b,c use two pointers, left/right on remaining list;
     * */
    public static List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();

        if (nums.length == 0) return new ArrayList<>(res);
        Arrays.sort(nums);

        for (int i = 0; i < nums.length; i++) {
            int a = nums[i];
            if (i > 0 && a == nums[i - 1]) continue;

            int l = i + 1, r = nums.length - 1;
            while (l < r) {
                int threeSum = a + nums[l] + nums[r];
                if (threeSum > 0) {
                    r--;
                } else if (threeSum < 0) {
                    l++;
                } else {
                    res.add(Arrays.asList(a, nums[l], nums[r]));
                    l++;
                    while (nums[l] == nums[l - 1] && l < r) {
                        l++;
                    }
                }
            }

        }
        return res;
    }

    public static List<List<Integer>> threeSum2nd(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new LinkedList<>();
        for (int i = 0; i < nums.length - 2; i++) {
            if (i == 0 || nums[i] != nums[i - 1]) {
                int low = i + 1;
                int high = nums.length - 1;
                int sum_tmp = -nums[i];

                while (low < high) {
                    if (nums[low] + nums[high] == sum_tmp) {
                        res.add(Arrays.asList(nums[i], nums[low], nums[high]));
                        while ((low < high) && nums[low] == nums[low + 1]) low++;
                        while ((low < high) && nums[high] == nums[high - 1]) high--;
                        low++;
                        high--;
                    } else if (nums[low] + nums[high] < sum_tmp) {
                        low++;
                    } else {
                        high--;
                    }
                }
            }
        }
        return res;
    }
}
