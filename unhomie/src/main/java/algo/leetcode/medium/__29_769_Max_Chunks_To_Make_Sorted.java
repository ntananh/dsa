package algo.leetcode.medium;

public class __29_769_Max_Chunks_To_Make_Sorted {

	/**
	 * <p>
	 * Input: int[] arr = [...] | arr.length = n. Represents a <b>permutation of the integers</b> in the range [0, n - 1].
	 * </p>
	 *
	 * <p>Req:</p>
	 * <ul>
	 *      <li>Split array into number of chunks (i.e., partitions) => Sort each chunk.</li>
	 *      <li>After concatenating the chunks, the result == the sorted array.</li>
	 *      <li>Return the largest number of chunks we can make to sort the array.</li>
	 * </ul>
	 *
	 * <p><b>Constraints:</b></p>
	 *
	 * <ul>
	 *      <li>{@code n == arr.length }</li>
	 *      <li>{@code 1 <= n <= 10 }</li>
	 *      <li>{@code 0 <= arr[i] < n }</li>
	 *      <li>All the elements of arr are unique.</li>
	 * </ul>
	 *
	 * @param arr input
	 * @return Return the largest number of chunks we can make to sort the array.
	 */
	public static int maxChunksToSorted(int[] arr) {
		return maxElement(arr);
	}

	public static int maxElement(int[] arr) {
		int chunks = 0, maxEl = 0, n = arr.length;

		for (int i = 0; i < n; i++) {
			maxEl = Math.max(maxEl, arr[i]);
			if (maxEl == i) {
				chunks++;
			}
		}

		return chunks;
	}
}
