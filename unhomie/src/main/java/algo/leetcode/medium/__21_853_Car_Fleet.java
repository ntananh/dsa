package algo.leetcode.medium;

import java.util.Arrays;
import java.util.Comparator;

/**
 * <p>
 * Sort cars by the start positions pos
 * Loop on each car from the end to the beginning
 * Calculate its time needed to arrive the target
 * cur records the current biggest time (the slowest)
 * </p>
 * <p>
 * If another car needs less or equal time than cur,
 * it can catch up this car fleet.
 * </p>
 * <p>
 * If another car needs more time, it will be the new slowest car,
 * and becomes the new lead of a car fleet.
 * </p>
 */
public class __21_853_Car_Fleet {
	public static int carFleet(int target, int[] position, int[] speed) {
		int N = position.length, res = 0;
		double[][] cars = new double[N][2];
		for (int i = 0; i < N; i++) {
			double eta = (double) (target - position[i]) / speed[i];
			cars[i] = new double[]{position[i], eta};
		}

		Arrays.sort(cars, Comparator.comparingDouble(a -> a[0]));

		double cur = 0;
		for (int i = N - 1; i >= 0; i--) {
			double curTime = cars[i][1];
			if (curTime > cur) {
				res++;
				cur = curTime;
			}
		}
		return res;
	}
}
