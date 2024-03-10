package algo.leetcode.easy;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class __15_349_Intersection_of_Two_Arrays {
	public int[] intersection(int[] nums1, int[] nums2) {
		Set<Integer> set = new HashSet<>();

		Arrays.sort(nums1);
		Arrays.sort(nums2);

		int i = 0, j = 0;
		while (i < nums1.length && j < nums2.length) {
			if (nums1[i] < nums2[j]) {
				i++;
			} else if (nums1[i] > nums2[j]) {
				j++;
			} else {
				set.add(nums1[i]);
				i++;
				j++;
			}
		}

		int[] res = new int[set.size()];
		int k = 0;
		for (Integer num : set) {
			res[k++] = num;
		}
		return res;
	}
}
