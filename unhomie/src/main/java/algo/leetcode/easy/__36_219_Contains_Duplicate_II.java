package algo.leetcode.easy;

import java.util.HashSet;
import java.util.Set;

public class __36_219_Contains_Duplicate_II {
    public static boolean containsNearbyDuplicate(final int[] nums, final int k) {
        final Set<Integer> set = new HashSet<>();
        for (int i = 0; i < nums.length; i++) {
            if (i > k) {
                set.remove(nums[i - k - 1]);
            }
            if (!set.add(nums[i])) {
                return true;
            }
        }

        return false;
    }
}
