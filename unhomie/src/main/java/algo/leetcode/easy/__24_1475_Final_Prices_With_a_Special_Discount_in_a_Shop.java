package algo.leetcode.easy;

import java.util.Stack;

public class __24_1475_Final_Prices_With_a_Special_Discount_in_a_Shop {

	/**
	 * <p>
	 * Given an int array {@code prices } where {@code prices[i] } is the price of the {@code ith } item in a shop.
	 * </p>
	 * <p> If buy {@code ith } item, get discount {@code prices[j] } where: <p>
	 * <ul>
	 *      <li> {@code j} is the minimum index, such that {@code j > i} </li>
	 *      <li> {@code prices[j] <= prices[i]} </li>
	 * </ul>
	 *
	 * <p><b>Constraints:</b></p>
	 * <ul>
	 *      <li>{@code 1 <= prices.length <= 500 }</li>
	 *      <li>{@code 1 <= prices[i] <= 1000 }</li>
	 * </ul>
	 *
	 * @param prices array of prices.
	 * @return the final array of prices after discount.
	 */
	public int[] finalPrices(int[] prices) {
		int[] res = prices.clone();

		final Stack<Integer> stack = new Stack<>();
		for (int i = 0; i < prices.length; i++) {
			while (!stack.isEmpty() && prices[stack.peek()] >= prices[i]) {
				res[stack.pop()] -= prices[i];
			}
			stack.push(i);
		}

		return res;
	}

}


