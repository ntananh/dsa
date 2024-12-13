package algo.leetcode.medium;

public class __28_2109_Adding_Spaces_to_a_String {

	/**
	 * <p>
	 * Given a <b>0-indexed</b> string {@code s} and a <b>0-indexed</b> integer arrays {@code spaces}.
	 * </p>
	 * <p>
	 * {@code spaces} describes the <i>indices</i> in the {@code s} where spaces will be added.
	 * Each space should be inserted <b>before</b> the character at the given index.
	 * </p>
	 *
	 * <p>
	 * Example:
	 * {@code s ="EnjoyYourCoffee"} and {@code spaces = [5, 9]}. Insert spaces before <i>Y</i> and <i>C</i>.
	 * The return value: {@code "Enjoy Your Coffee" }
	 * </p>
	 *
	 * <ul><b>Constraints:</b>
	 *     <li>{@code 1 <= s.length <= 3 * 10}<sup>5</sup></li>
	 *     <li>{@code s} contains only lowercase and uppercase english</li>
	 *     <li>{@code 1 <= spaces.length <= 3 * 10}<sup>5</sup></li>
	 *     <li>{@code 0 <= spaces[i] <= s.length - 1}</li>
	 *     <li>All the values of {@code spaces} are <b>strictly increasing</b></li>
	 * </ul>
	 * </ul>
	 *
	 * @param s      the original space.
	 * @param spaces array of space index should add space.
	 * @return the modified string after the spaces have been added.
	 */
	public static String addSpaces(String s, int[] spaces) {
		if (s == null || s.isEmpty() || spaces == null || spaces.length == 0) {
			return s;
		}

		final StringBuilder result = new StringBuilder(s.length() + spaces.length);
		int charIdx = 0, appendIdx = 0;
		while (charIdx < s.length()) {
			if (appendIdx < spaces.length && charIdx == spaces[appendIdx]) {
				result.append(' ');
				appendIdx++;
			}
			result.append(s.charAt(charIdx));
			charIdx++;
		}

		return result.toString();
	}
}
