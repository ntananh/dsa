package algo.leetcode.medium;

import java.util.HashSet;
import java.util.Set;

public class __42_961_N_Repeated_Element_in_Size_2N_Array {
    public static int repeatedNTimes(final int[] nums) {
        final Set<Integer> seen = new HashSet<>();
        for (final int n : nums) {
            if (seen.contains(n)) {
                return n;
            }
            seen.add(n);
        }
        return -1;
    }
}
