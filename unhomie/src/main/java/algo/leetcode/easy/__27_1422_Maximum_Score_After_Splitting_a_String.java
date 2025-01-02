package algo.leetcode.easy;

public class __27_1422_Maximum_Score_After_Splitting_a_String {
    /**
     * <p>
     * Given a string s of zeros and ones.
     * Return the maximum score after splitting the string into two non-empty substrings
     * (i.e. left substring and right substring).
     * </p>
     * <p>
     * The score after splitting a string is the number of zeros in the left substring
     * plus (+) the number of ones in the right substring.
     * </p>
     *
     * <p><b>Constraints</b>:</p>
     * <ul>
     *    <li> 2 <= s.length <= 500 </li>
     *    <li> The string s consists of characters '0' and '1' only. </li>
     * </ul>
     *
     * @param s a string of zeros and ones ("011")
     * @return the maximum score.
     */
    public static int maxScore(String s) {
        int totalOnes = 0;
        int countZeros = 0;
        int maxScore = 0;

        for (char c : s.toCharArray()) {
            if (c == '1') {
                totalOnes++;
            }
        }

        for (int i = 0; i < s.length() - 1; i++) {
            if (s.charAt(i) == '0') {
                countZeros++;
            } else {
                totalOnes--;
            }

            int currentScore = countZeros + totalOnes;
            maxScore = Math.max(maxScore, currentScore);
        }

        return maxScore;
    }
}
