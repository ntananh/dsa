package algo.recursion;

public class ReverseString {
	public static String reverse(String input) {
		if (input.length() == 1) return input;
		return input.charAt(input.length() - 1) + reverse(input.substring(0, input.length() - 1));
	}
}
