package algo.leetcode.medium;

public class __14_1750_Minimum_Length {

	public static int minimumLength(String s) {
		int i = 0, j = s.length() - 1;

		while (i < j && s.charAt(i) == s.charAt(j)) {
			char c = s.charAt(j);
			while (i <= j && c == s.charAt(i)) {
				i++;
			}

			while (j >= i && c == s.charAt(j)) {
				--j;
			}
		}

		return j - i + 1;
	}

	public static void main(String[] args) {
		System.out.println(minimumLength("aabccabba"));
	}
}
