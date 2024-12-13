package algo.leetcode.easy;

import java.util.Collections;
import java.util.PriorityQueue;

public class __23_2558_Take_Gifts_From_the_Richest_Pile {

	/**
	 * <p> Given an array {@code gifts} denoting the number of gifts in each pile and {@code k} seconds. </p>
	 * <ul> Every second:
	 *      <li> Choose max.</li>
	 *      <li> If multiple max, choose any.</li>
	 *      <li> Square root max.</li>
	 * </ul>
	 * <p> Return the number of gifts after {@code k } seconds </p>
	 *
	 * <p><b>Constraints:</b></p>
	 * <ul>
	 *      <li>{@code 1 <= gifts.length <= 103 }</li>
	 *      <li>{@code 1 <= gifts[i] <= 109 }</li>
	 *      <li>{@code 1 <= k <= 103 }</li>
	 * </ul>
	 *
	 * @param gifts list of gifts
	 * @param k     picking seconds
	 * @return total number of gifts left.
	 */
	public static long pickGifts(int[] gifts, int k) {

		if (gifts == null || gifts.length == 0 || k == 0) {
			return -1;
		}

		final PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
		for (int gift : gifts) maxHeap.add(gift);

		while (k-- > 0) {
			final Integer top = maxHeap.peek();
			if (top == null || top <= 1) break;
			final Integer max = maxHeap.poll();
			maxHeap.add((int) Math.sqrt(max));
		}

		// NOTE: use loop is faster :v
		return maxHeap.stream().mapToLong(Integer::longValue).sum();
	}
}
