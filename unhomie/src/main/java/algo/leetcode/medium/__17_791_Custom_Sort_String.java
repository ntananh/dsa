package algo.leetcode.medium;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class __17_791_Custom_Sort_String {

	public String customSortString(String order, String s) {
		return optimized(order, s);
	}

	String optimized(String order, String s) {
		Map<Character, Integer> cMap = new HashMap<>();

		StringBuilder sb = new StringBuilder();
		for (char c : s.toCharArray()) {
			cMap.put(c, cMap.getOrDefault(c, 0) + 1);
		}

		int count;
		for (char c : order.toCharArray()) {
			if (cMap.containsKey(c)) {
				count = cMap.get(c);
				while (count-- > 0) sb.append(c);
				cMap.remove(c);
			}
		}

		for (char c : cMap.keySet()) {
			count = cMap.get(c);
			while (count-- > 0) sb.append(c);
		}

		return sb.toString();
	}

	String naive(String order, String s) {
		Map<Character, List<Character>> map = new HashMap<>();

		for (char c : order.toCharArray()) {
			map.put(c, new ArrayList<>());
		}
		map.put('_', new ArrayList<>());

		for (char c : s.toCharArray()) {
			if (map.containsKey(c)) {
				map.get(c).add(c);
			} else {
				map.get('_').add(c);
			}
		}

		StringBuilder res = new StringBuilder();
		for (char c : order.toCharArray()) {
			List<Character> cL = map.get(c);
			StringBuilder bd = new StringBuilder();
			if (!cL.isEmpty()) {
				cL.forEach(bd::append);
				res.append(bd);
			}
		}

		List<Character> unknown = map.get('_');
		StringBuilder bd = new StringBuilder();
		unknown.forEach(bd::append);
		res.append(bd);

		return res.toString();
	}


	public static void main(String[] args) {
		String order = "bcafg", s = "abcd";

		System.out.println(new __17_791_Custom_Sort_String().customSortString(order, s));
	}
}
