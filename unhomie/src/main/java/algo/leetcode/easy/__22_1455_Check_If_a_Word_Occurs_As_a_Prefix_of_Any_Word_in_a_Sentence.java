package algo.leetcode.easy;

public class __22_1455_Check_If_a_Word_Occurs_As_a_Prefix_of_Any_Word_in_a_Sentence {

	/**
	 * <p>
	 * Given a {@code sentence} contains some word seperated by <b>single space</b>.
	 * Check if {@code searchWord} is prefix of any word in {@code sentence}
	 * </p>
	 * <p>
	 * If {@code searchWord} is a prefix of more than one word, return the index of first word (<b>minimum index</b>)
	 * </p>
	 *
	 * <p><b>Constraints:</b></p>
	 * <ul>
	 *      <li>{@code 1 <= sentence.length <= 100 }</li>
	 *      <li>{@code 1 <= searchWord.length <= 10 }</li>
	 *      <li>{@code sentence } consists of <i>lowercase</i> English letters and spaces.</li>
	 *      <li>{@code searchWord } consists of <i>lowercase</i> English letters.</li>
	 * </ul>
	 *
	 * @param sentence   the input
	 * @param searchWord search word
	 * @return index of first word found in sentence
	 */
	public int isPrefixOfWord(String sentence, String searchWord) {
		final String[] words = sentence.split(" ");
		for (int i = 0; i < words.length; i++) {
			if (words[i].startsWith(searchWord)) {
				return i;
			}
		}
		return -1;
	}
}
