package algo.leetcode.hard;

import java.util.*;
import java.util.stream.Collectors;

/*
 * Idea: Add all number to set
 * If the set is *not* contains n - 1 value, n is start of sequence
 * Start find all possibly n + 1 value in set.
 *
 * Example: <no value>-1-2-3-4      : 1 is start of sequence, start counting values after 1
 *          <no value>-0-<no value> : 0 also is a sequence with length is 1
 */
public class __1_128_Longest_Consecutive_Sequence {

    public static int longestConsecutive(int[] nums) {
        Set<Integer> numsSet = new HashSet<>();
        for (int n : nums) numsSet.add(n);

        int longestConsecutive = 0;
        for (int n : nums) {
            if (!numsSet.contains(n - 1)) {
                int length = 0;
                while (numsSet.contains(n + length)) {
                    length++;
                }
                longestConsecutive = Integer.max(length, longestConsecutive);
            }
        }
        return longestConsecutive;
    }

    public static void main(String[] args) {
        int[] nums = {100, 4, 200, 1, 3, 2};
        System.out.println(longestConsecutive(nums));
    }
}
