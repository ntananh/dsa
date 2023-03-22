package algo.leetcode.easy;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class __6_49_Group_Anagrams {

    static class Solution {
        public static List<List<String>> groupAnagrams(String[] strs) {
            Map<String, List<String>> result = new HashMap<>();

            // 26 is number characters a-z
            int[] count = new int[26];
            for (String s : strs) {
                Arrays.fill(count, 0);
                for (char c : s.toCharArray()) count[c - 'a']++;

                StringBuilder sb = new StringBuilder();
                for (int j : count) {
                    sb.append("#");
                    sb.append(j);
                }

                String key = sb.toString();
                if (!result.containsKey(key)) result.put(key, new ArrayList<>());
                result.get(key).add(s);

            }

            return new ArrayList<>(result.values());
        }
    }

    public static void main(String[] args) {
        String[] strs = { "eat","tea","tan","ate","nat","bat" };
        List<List<String>> result = Solution.groupAnagrams(strs);
    }
}
