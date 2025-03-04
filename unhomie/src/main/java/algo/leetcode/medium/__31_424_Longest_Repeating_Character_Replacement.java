package algo.leetcode.medium;

import java.util.HashMap;
import java.util.Map;

public class __31_424_Longest_Repeating_Character_Replacement {

    /**
     * <p>
     * You are given a string s and an integer k.
     * Operation: Choose any character of the string and change it to any other uppercase English character.
     * Can perform the operation at most k times.
     * </p>
     * <p>
     * Idea:
     * - Sliding windows, with char frequencies map, keep track **max frequency char**.
     * - Valid window is {@code (right - left + 1) - maxFreqChar <= k}
     * </p>
     *
     * @param s the original string
     * @param k times to do operation
     * @return the length of the longest substring containing the same letter you can get after performing the above operations.
     */
    public static int characterReplacement(String s, int k) {
        final Map<Character, Integer> frequencies = new HashMap<>();

        int left = 0, res = 0, maxFreqChar = 0;
        for (int right = 0; right < s.length(); right++) {
            frequencies.put(s.charAt(right), frequencies.getOrDefault(s.charAt(right), 0) + 1);

            maxFreqChar = Math.max(maxFreqChar, frequencies.get(s.charAt(right)));

            while ((right - left + 1) - maxFreqChar > k) {
                char leftChar = s.charAt(left);
                frequencies.put(leftChar, frequencies.getOrDefault(leftChar, 0) - 1);
                left++;
            }

            res = Math.max(res, right - left + 1);
        }

        return res;
    }
}
