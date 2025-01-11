package algo.leetcode.medium;

public class __37_1400_Construct_K_Palindrome_Strings {

    /**
     * @param s a string
     * @param k an integer
     * @return {@code true} if can use all the characters in {@code s} to construct {@code k} palindrome strings,
     * otherwise {@code false}.
     */
    public static boolean canConstruct(String s, int k) {
        if (s.length() < k) return false;

        int[] chars = new int[26];
        for (int i = 0; i < s.length(); i++) {
            chars[s.charAt(i) - 'a']++;
        }

        int oddCount = 0;
        for (int count : chars) {
            if (count % 2 != 0) oddCount++;
        }

        return oddCount <= k;
    }
}
