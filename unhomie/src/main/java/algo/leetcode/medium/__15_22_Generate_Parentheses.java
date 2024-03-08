package algo.leetcode.medium;

import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

public class __15_22_Generate_Parentheses {

	public static List<String> generateParenthesis(int n) {
		List<String> generated = new ArrayList<>();
		Stack<String> stack = new Stack<>();

		// add open IF open < n
		// add close IF close < open
		// valid IF open == close == n
		backtrack(generated, stack, n, 0, 0);

		return generated;
	}

	private static void backtrack(List<String> res, Stack<String> stack, int n, int openN, int closeN) {
		if (openN == closeN && closeN == n) {
			res.add(String.join("", stack));
			return;
		}

		if (openN < n) {
			stack.add("(");
			backtrack(res, stack, n,openN + 1, closeN);
			stack.pop();
		}

		if (closeN < openN) {
			stack.add(")");
			backtrack(res, stack, n,openN, closeN + 1);
			stack.pop();
		}
	}
}
