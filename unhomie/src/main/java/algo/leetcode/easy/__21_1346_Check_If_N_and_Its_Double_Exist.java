package algo.leetcode.easy;

import java.util.HashSet;
import java.util.Set;

public class __21_1346_Check_If_N_and_Its_Double_Exist {

	/**
	 * <p>
	 * Given an {@code arr} of <i>integer</i>, check if exists two indices {@code i} and {@code j} such that:
	 * <ul>
	 *     <li>{@code i != j}</li>
	 *     <li>{@code 0 <= i && j < arr.length}</li>
	 *     <li>{@code arr[i] == 2 * a[j]}</li>
	 * </ul>
	 * </p>
	 *
	 * <p><b>Constraints:</b></p>
	 * <ul>
	 *      <li>{@code 2 <= arr.length <= 500 }</li>
	 *      <li>{@code 103 <= arr[i] <= 103 }</li>
	 * </ul>
	 *
	 * @param arr the array to search.
	 * @return {@code true } if exist {@code arr[i] == 2 * arr[j]}, otherwise {@code false }
	 */
	public boolean checkIfExist(int[] arr) {
		final Set<Integer> seen = new HashSet<>();

		for (int value : arr) {
			if (seen.contains(value * 2) || (value % 2 == 0 && seen.contains(value / 2))) {
				return true;
			}
			seen.add(value);
		}

		return false;
	}
}
