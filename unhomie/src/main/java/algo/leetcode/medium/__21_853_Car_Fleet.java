package algo.leetcode.medium;

import java.util.Arrays;
import java.util.Comparator;

/**
 * N car: start at mile 0 try to reach the [target]
 * 2 arrays, length [n]
 * int[] position  : position[i] is the starting point of ith car.
 * int[] speed     : speed[i] is the speed of ith car.
 * <p>
 * Constrains:
 * a car cannot pass another
 * can catch up then travel next to at the speed of slower car.
 * <p>
 * Car fleet:
 * a car or cars driving next to each other.
 * speed of car fleet is the slowest one
 * if a car catches up to a car fleet at the mile target -> it's a part of the car fleet
 * <p>
 * Return:
 * number of car fleet will arrive at the target
 * <p>
 * Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3] => Output: 3
 * <p>
 * Explanation:
 * The cars starting at 10 (speed 2) and 8 (speed 4) become a fleet, meeting each other at 12.
 * <p>
 * The fleet forms at target.
 * <p>
 * The car starting at 0 (speed 1) does not catch up to any other car, so it is a fleet by itself.
 * <p>
 * The cars starting at 5 (speed 1) and 3 (speed 3) become a fleet, meeting each other at 6.
 * <p>
 * The fleet moves at speed 1 until it reaches target.
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
