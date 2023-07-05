package algo.leetcode.medium;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/*
 * Idea: store length of string before each string and delimiter like '#';
 *
 * Why we need to store the length of string before each string ?
 * Because strs[i] contains any possible character out of 256 valid ASCII characters.
 * And ASCII also contains special character like ?!@#$(, we cannot use the delimiter only.
 */
public class __7_271_Encode_and_Decode_String {

    private static final char DELIMITER = '#';

    /*
     * @param strs: a list of strings
     * @return: encodes a list of strings to a single string.
     */
    public static String encode(List<String> strs) {
        StringBuilder sb = new StringBuilder();
        for (String s : strs) {
            sb.append(s.length());
            sb.append(DELIMITER);
            sb.append(s);
        }
        return sb.toString();
    }

    /*
     * @param str: A string
     * @return: decodes a single string to a list of strings
     */
    public static List<String> decode(String str) {
        List<String> decodeValues = new ArrayList<>();
        if (str == null || str.isEmpty()) {
            return decodeValues;
        }

        char[] chars = str.toCharArray();
        for (int i = 0; i < chars.length; i++) {
            StringBuilder sb = new StringBuilder();

            // Find number of chars
            while (chars[i] != DELIMITER) {
                sb.append(chars[i++]);
            }
            i++;

            // iteration the enter string to add to result list
            int numOfChars = Integer.parseInt(sb.toString());
            int end = i + numOfChars;
            sb = new StringBuilder();
            while (i < end) {
                sb.append(chars[i++]);
            }
            i--;

            decodeValues.add(sb.toString());
        }

        return decodeValues;
    }

    public static void main(String[] args) {
        List<String> input = Arrays.asList("Hello", "World");
        System.out.println(encode(input));
        System.out.println(decode(encode(input)));
    }
}
