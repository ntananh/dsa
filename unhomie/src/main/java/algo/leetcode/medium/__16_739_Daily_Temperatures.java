package algo.leetcode.medium;

import java.util.Stack;

public class __16_739_Daily_Temperatures {
	public int[] dailyTemperatures(int[] temperatures) {
		int[] res = new int[temperatures.length];
		Stack<Integer> stack = new Stack<>();

		for (int i = 0; i < temperatures.length; i++) {
			while (!stack.empty() && temperatures[stack.peek()] < temperatures[i]) {
				int idx = stack.pop();
				res[idx] = i - idx;
			}
			stack.push(i);
		}

		return res;
	}
}
