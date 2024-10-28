package algo.recursion;

public class SumOfDigits {
	public static int sum(int num) {
		if (num < 10) return num;
		return num % 10 + sum(num / 10);
	}
}
