package algo.leetcode.easy;

public class __25_121_Best_Time_to_Buy_and_Sell_Stock {

	/**
	 * <p>
	 * Given an array prices where {@code prices[i] } is the price of a stock on the {@code ith } day.
	 * Choosing <i>a day to buy 1 stock</i> && choosing another day <b>in the future</b> to sell that stock.
	 * Buy day < Sell day.
	 * </p>
	 * <p>Return the {@code max( prices[sell] - prices[buy] ) }</p>
	 *
	 * <p><b>Constraints</b>:</p>
	 * <ul>
	 *      <li>{@code 1 <= prices.length <= 105 }</li>
	 *      <li>{@code 0 <= prices[i] <= 104 }</li>
	 * </ul>
	 *
	 * @param prices stock prices
	 * @return maximum profit
	 */
	public static int maxProfit(int[] prices) {
		int minPrice = Integer.MAX_VALUE, maxProfit = 0;
		for (int price : prices) {
			if (price < minPrice) {
				minPrice = price;
			}
			maxProfit = Math.max(price - minPrice, maxProfit);
		}
		return maxProfit;
	}

	public static int maxProfit2Pointers(int[] prices) {
		int buy = 0, sell = 1, maxProfit = 0;
		while (sell < prices.length) {
			if (prices[buy] < prices[sell]) {
				int profit = prices[sell] - prices[buy];
				maxProfit = Math.max(profit, maxProfit);
			} else {
				buy = sell;
			}
			sell++;
		}

		return maxProfit;
	}


}
