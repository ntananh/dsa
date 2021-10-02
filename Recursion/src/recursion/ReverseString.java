package recursion;

import java.util.WeakHashMap;

public class ReverseString {
    public static void main(String[] args) {
        char[] s = {'T', 'a', 'n', 'A', 'n', 'h'};
        char[] s1 = {'h', 'e', 'l', 'l', 'o'};
        reverseString(s1);
    }

    public static void reverseString(char[] s) {
        helper(s, 0);
    }

    public static void helper(char[] s, int index) {
        if (s == null || index >= s.length ) return;
        helper(s, index + 1);
        System.out.print(s[index] + " ");
    }
}
