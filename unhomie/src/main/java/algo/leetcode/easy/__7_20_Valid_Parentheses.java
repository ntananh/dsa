package algo.leetcode.easy;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

public class __7_20_Valid_Parentheses {
    public static boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();
        Map<Character, Character> pair = new HashMap<>();
        pair.put(')', '(');
        pair.put(']', '[');
        pair.put('}', '{');

        for (char c : s.toCharArray()) {
            if (!pair.containsKey(c)) {
                stack.push(c);
                continue;
            }
            if (stack.isEmpty() || stack.pop() != pair.get(c)) {
                return false;
            }
        }

        return stack.isEmpty();
    }
}
