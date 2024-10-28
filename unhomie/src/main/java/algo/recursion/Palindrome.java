package algo.recursion;

public class Palindrome {
	public static boolean isPalindrome(String s) {
		if (s.isEmpty()) return false;

		return isPalindrome(s);
	}

	public static void main(String[] args) {
		isPalindrome("racecar");
	}

}
