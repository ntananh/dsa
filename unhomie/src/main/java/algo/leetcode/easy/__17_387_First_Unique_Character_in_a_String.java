package algo.leetcode.easy;

public class __17_387_First_Unique_Character_in_a_String {
	public int firstUniqChar(String s) {
		int[] freqs = new int[26];
		for (int i = 0; i < s.length(); i++) {
			freqs[s.charAt(i) - 'a']++;
		}

		for (int i = 0; i < s.length(); i++) {
			if( freqs[s.charAt(i) - 'a'] == 1) return i;;
		}

		return -1;
    }
}
