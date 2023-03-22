package algo.leetcode.easy;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class __4_242_Valid_Anagram {
    static class Solution {
        public static boolean isAnagram(String s, String t) {
            if (s.length() != t.length()) return false;

            Map<Character, Integer> swords = new HashMap<>();
            Map<Character, Integer> twords = new HashMap<>();

            for (int i = 0; i < s.length(); i++) {
                int svalue = swords.get(s.charAt(i)) != null ? swords.get(s.charAt(i)) : 0;
                int tvalue = twords.get(t.charAt(i)) != null ? twords.get(t.charAt(i)) : 0;
                swords.put(s.charAt(i), svalue + 1);
                twords.put(t.charAt(i), tvalue + 1);
            }

            for (int i = 0; i < s.length(); i++) {
                if (!Objects.equals(swords.get(s.charAt(i)), twords.get(s.charAt(i)))) {
                    return false;
                }
            }

            return true;
        }

        public static boolean isAnagramV2(String s, String t) {
            if (s.length() != t.length()) return false;

            Map<Character, Integer> words = new HashMap<>();

            for (int i = 0; i < s.length(); i++) {
                words.put(s.charAt(i), words.getOrDefault(s.charAt(i), 0) + 1);
                words.put(t.charAt(i), words.getOrDefault(t.charAt(i), 0) - 1);
            }

            for (int remain : words.values()) {
                if (remain > 0) return false;
            }

            return true;
        }

        public static boolean isAnagramV3(String s, String t) {
            if (s.length() != t.length()) return false;
            int[] count = new int[26];

            for (int i = 0; i < s.length(); i++) {
                count[s.charAt(i) - 'a']++;
                count[t.charAt(i) - 'a']--;
            }

            for (int c: count) {
                if (c != 0) return false;
            }

            return true;
        }

        public static boolean isAnagramV4(String s, String t) {
            if (s.length() != t.length()) return false;

            int[] count = new int[268];

            for (char c: s.toCharArray()) {
                count[c - 'a']++;
            }

            for (char c: t.toCharArray()) {
                count[c - 'a']--;
            }

            for (int c: count) {
                if (c != 0) return false;
            }

            return true;
        }
    }

    public static void main(String[] args) {
        System.out.println(Solution.isAnagramV4("anagram", "agnaarm"));
        System.out.println(Solution.isAnagramV4("cat", "rat"));
    }
}
