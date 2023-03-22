package algo.leetcode.easy;

import java.util.HashSet;
import java.util.Set;

import static junit.framework.TestCase.assertFalse;
import static junit.framework.TestCase.assertTrue;

public class __5_217_Contains_Duplicate {

    static class Solution {
        public static boolean containsDuplicate(int[] nums) {
            Set<Integer> numbers = new HashSet<>();

            for (int i: nums) {
                if (!numbers.add(i)) return true;
            }

            return false;
        }
    }

    public static void main(String[] args) {
        int[] nums = new int[]{1, 1, 1, 3, 3, 4, 3, 2, 4, 2};
        int[] numsV2 = new int[]{1, 2, 3, 4};
        assertTrue(Solution.containsDuplicate(nums));
        assertFalse(Solution.containsDuplicate(numsV2));
    }
}
