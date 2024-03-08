package algo.leetcode.easy;

import java.util.HashMap;
import java.util.Map;

public class __13_3005_Count_Elements_With_Maximum_Frequency {
	public int maxFrequencyElements(int[] nums) {
		Map<Integer, Integer> map = new HashMap<>();

		for (int num : nums) {
			map.put(num, map.getOrDefault(num, 0) + 1);
		}

		int maxFreq = Integer.MIN_VALUE;
		for (int freq : map.values()) {
			maxFreq = Math.max(maxFreq, freq);
		}

		int res = 0;
		for (int freq : map.values()) {
			if (freq == maxFreq) res += maxFreq;
		}

		return res;
	}
}
