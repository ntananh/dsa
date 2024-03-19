package algo.leetcode.medium;

import java.util.Arrays;

public class __20_621_Task_Scheduler {
	public int leastInterval(char[] tasks, int n) {

		int[] freq = new int[26];
		for (char c : tasks) {
			freq[c - 'A']++;
		}
		Arrays.sort(freq);

		int maxVal = freq[25] - 1;
		int idleSlots = maxVal * n;
		for (int i = 24; i >= 0; i--) {
			idleSlots -= Math.min(freq[i], maxVal);
		}

		return idleSlots > 0 ? idleSlots + tasks.length : tasks.length;
	}
}
