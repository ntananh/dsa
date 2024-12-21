package algo.leetcode.easy;

import java.util.HashSet;
import java.util.Set;

public class __26_3_Longest_Substring_Without_Repeating_Characters {

	/**
	 * <p>
	 * Finds the length of the longest substring in {@code s} without repeating characters.
	 * </p>
	 *
	 * <b>Constraints:</b>
	 * <ul>
	 *      <li>{@code 0 <= s.length <= 5 * 10}<sup>4</sup></li>
	 *      <li>{@code s} contains English letters, digits, symbols, and spaces.</li>
	 * </ul>
	 *
	 * @param s the input string
	 * @return the length of the longest substring without repeating characters
	 */
	public static int lengthOfLongestSubstring(String s) {
		final Set<Character> seen = new HashSet<>();
		int left = 0, maxLength = 0;

		for (int right = 0; right < s.length(); right++) {
			while (seen.contains(s.charAt(right))) {
				seen.remove(s.charAt(left));
				left++;
			}
			seen.add(s.charAt(right));
			maxLength = Math.max(maxLength, right - left + 1);
		}

		return maxLength;
	}

	public static void main(String[] args) {

		String s = "abcabcbb";
		System.out.println(lengthOfLongestSubstring(s));
	}

}
