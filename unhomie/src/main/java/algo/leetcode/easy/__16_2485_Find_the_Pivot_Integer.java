package algo.leetcode.easy;

public class __16_2485_Find_the_Pivot_Integer {
	public int pivotInteger(int n) {
		if (n <= 1) return n;

		int[] bucket = new int[n];
		for (int val = 1; val <= n; val++) {
			int index = val - 1;
			if (index == 0) bucket[index] = val;
			else bucket[index] = bucket[index - 1] + val;
		}

		int cal = 0;
		for (int i = n; i > 2; i--) {
			if (cal == 0) cal = i;
			else  cal += i;
			if (cal == bucket[i - 1]) return i;
		}

		return -1;
	}
}
