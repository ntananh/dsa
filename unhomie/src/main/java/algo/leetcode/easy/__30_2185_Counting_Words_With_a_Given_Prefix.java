package algo.leetcode.easy;

import java.util.Arrays;

public class __30_2185_Counting_Words_With_a_Given_Prefix {

    /**
     * @param words list of string
     * @param pref  a string
     * @return the number of string in {@code words} contains {@code pref} as a prefix.
     */
    public int prefixCount(String[] words, String pref) {
        int res = 0;
        for (String word: words) {
            if (word.startsWith(pref)) {
                res++;
            }
        }
        return res;
    }

    public int oneLine(String[] words, String pref) {
        return (int) Arrays.stream(words)
                .filter(w -> w.startsWith(pref))
                .count();
    }
}
