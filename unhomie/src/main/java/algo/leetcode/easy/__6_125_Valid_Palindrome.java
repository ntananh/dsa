package algo.leetcode.easy;

import static java.lang.Character.isLetterOrDigit;

/*
 * Idea: this one has 2 solutions
 * 1. Use 2 pointers technique
 * 2. Create a string and reverse, compare with original string
 */
public class __6_125_Valid_Palindrome {

    /*
    * Idea: create 2 pointers
    *   - left pointer start at 0
    *   - right pointer start at the end of string
    * Compare the character between 2 indexes
    * */
    public static boolean isPalindrome(String s) {
        if (s.isEmpty()) {
            return true;
        }
        StringBuilder sb = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (isLetterOrDigit(c)) {
                sb.append(String.valueOf(c).toLowerCase());
            }
        }
        String cleanS = sb.toString();
        int l = 0,r = cleanS.length() - 1;
        while (l < r) {
            if (cleanS.charAt(l) != cleanS.charAt(r))  {
                return false;
            }
            l++;
            r--;
        }
        return true;
    }

    public static void main(String[] args) {
        String s = "A man, a plan, a canal: Panama";
        System.out.println(isPalindrome(s));
    }
}
