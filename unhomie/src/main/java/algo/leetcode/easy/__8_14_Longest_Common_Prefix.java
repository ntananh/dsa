package algo.leetcode.easy;

import java.util.Arrays;
import java.util.Comparator;

public class __8_14_Longest_Common_Prefix {
	public static String longestCommonPrefix(String[] strs) {
		return optimized(strs);
	}

	public static String naive(String[] strs) {
		Arrays.sort(strs, Comparator.comparing(String::length));

		StringBuilder longestPrefix = new StringBuilder();

		final int size = strs.length;
		final String firstStr = strs[0];
		final int minLength = strs[0].length();

		for (int i = 0; i < minLength; i++) {
			char c = firstStr.charAt(i);
			boolean common = true;

			for (int j = 1; j < size; j++) {
				if (c != strs[j].charAt(i)) {
					common = false;
					break;
				}
			}

			if (common) {
				longestPrefix.append(c);
			} else {
				return longestPrefix.toString();
			}
		}

		return longestPrefix.toString();
	}

	public static String optimized(String[] strs) {
		StringBuilder ans = new StringBuilder();

		Arrays.sort(strs);

		final String first = strs[0];
		final String last = strs[strs.length - 1];

		for (int i = 0; i < Math.min(first.length(), last.length()); i++) {
			if (first.charAt(i) != last.charAt(i)) {
				break;
			}
			ans.append(first.charAt(i));
		}

		return ans.toString();
	}

	public static void main(String[] args) {
		String[] failed = new String[]{"cir", "car"};

		System.out.println(longestCommonPrefix(failed));
	}
}
