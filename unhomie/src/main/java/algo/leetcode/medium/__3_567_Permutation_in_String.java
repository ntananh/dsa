package algo.leetcode.medium;

import java.util.HashMap;
import java.util.Map;

public class __3_567_Permutation_in_String {

    /**
     * Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.
     *
     * @param s1 first
     * @param s2 second
     * @return true if one of s1's permutations is the substring of s2.
     */
    public static boolean checkInclusion(String s1, String s2) {
        if (s1.length() > s2.length()) return false;

        int[] s1map = new int[26], s2map = new int[26];
        for (int i = 0; i < s1.length(); i++) {
            s1map[s1.charAt(i) - 'a']++;
            s2map[s2.charAt(i) - 'a']++;
        }


        for (int i = 0; i < s2.length() - s1.length(); i++) {
            if (matches(s1map, s2map)) return true;
            s2map[s2.charAt(i + s1.length()) - 'a']++;
            s2map[s2.charAt(i) - 'a']--;
        }

        return matches(s1map, s2map);
    }

    private static boolean matches(int[] s1map, int[] s2map) {
        for (int i = 0; i < 26; i++) {
            if (s1map[i] != s2map[i]) return false;
        }
        return true;
    }

    public static boolean dump(String s1, String s2) {

        // fixed sliding window with length s1
        // cal frequency of char in s1
        // if frequency match with frequency in window => valid

        final Map<Character, Integer> frequency = new HashMap<>();
        for (char c : s1.toCharArray()) frequency.put(c, frequency.getOrDefault(c, 0) + 1);

        int n = s1.length(), left = 0, right = n - 1;

        while (right < s2.length()) {
            final Map<Character, Integer> copy = new HashMap<>(frequency);
            int runner = left;
            while (runner <= right) {
                char curChar = s2.charAt(runner);
                if (copy.containsKey(curChar)) {
                    copy.put(curChar, copy.get(curChar) - 1);
                }
                runner++;
            }

            boolean valid = true;
            for (char c : copy.keySet()) {
                if (copy.get(c) > 0) {
                    valid = false;
                }
            }
            if (valid) return true;
            left++;
            right++;
        }

        return false;
    }
}
