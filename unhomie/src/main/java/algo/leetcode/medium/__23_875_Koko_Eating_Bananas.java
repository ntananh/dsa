package algo.leetcode.medium;

import java.util.Arrays;

public class __23_875_Koko_Eating_Bananas {


	/**
	 * <p>
	 * There are {@code n} piles of bananas.
	 * The {@code i}<sup>th</sup> pile has {@code piles[i]} bananas.
	 * The guards leave and will come back in {@code h} hours.
	 * </p>
	 *
	 * <p> {@code k} is eating speed </p>
	 * <p> Each hour, Koko chooses some pile of bananas and eat {@code k} bananas from that pile.</p>
	 * <ul>
	 *     <li>
	 *          The pile has less than (<) {@code k} bananas:
	 *          <ul>
	 *              <li> Eat all.</li>
	 *              <li> Will not eat any more bananas during this hour. </li>
	 *          </ul>
	 *     </li>
	 * </ul>
	 * <p>
	 * Example:
	 * <p><b>Input:</b> {@code piles = [3, 6, 7, 11], h = 8} </p>
	 * <p><b>Output:</b> {@code 4} </p>
	 * <p>
	 * Constraints:
	 * <ul>
	 *     <li>{@code 1 <= piles.length <= 1,000}</li>
	 *     <li>{@code piles.length <= h <= 1,000,000}</li>
	 *     <li>{@code 1 <= piles[i] <= 1,000,000,000 }</li>
	 * </ul>
	 *
	 * @param piles of banana size {@code n}
	 * @param h     the time of the guards leave
	 * @return the <i>minimum</i> {@code k} that Koko can eat all bananas within {@code h} hours
	 */
	public static int minEatingSpeed(int[] piles, int h) {
		return binarySearch(piles, h);
	}

	private static int binarySearch(int[] piles, int h) {
		if (piles.length == 0) {
			return -1;
		}

		int l = 1;
		int r = Arrays.stream(piles).max().getAsInt();
		int res = r;
		while (l <= r) {
			int k = (r + l) / 2;

			int totalTime = 0; // calculate the eating time with rate k
			for (int pile : piles) {
				totalTime += (int) Math.ceil((double) pile / k);
			}

			if (totalTime <= h) {
				res = Math.min(res, k);
				r = k - 1;
			} else {
				l = k + 1;
			}
		}

		return res;
	}

	private static int bruteforce(int[] piles, int h) {
		int speed = 1;

		while (true) {
			long totalTime = 0;
			for (int pile : piles) {
				totalTime += (int) Math.ceil((double) pile / speed);
			}
			if (totalTime <= h) {
				return speed;
			}
			speed++;
		}
	}

}
