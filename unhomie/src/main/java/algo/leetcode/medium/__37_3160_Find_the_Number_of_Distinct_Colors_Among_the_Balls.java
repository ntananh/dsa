package algo.leetcode.medium;

import java.util.HashMap;
import java.util.Map;

public class __37_3160_Find_the_Number_of_Distinct_Colors_Among_the_Balls {

    public int[] queryResults(int limit, int[][] queries) {
        final int n = queries.length;
        final int[] res = new int[n];
        final Map<Integer, Integer> ballMap = new HashMap<>();
        final Map<Integer, Integer> colorMap = new HashMap<>();

        for (int[] query : queries) {
            final int ball = query[0];
            final int color = query[1];

            if (ballMap.containsKey(ball)) {
                final int prevColor = ballMap.get(ball);
                colorMap.put(prevColor, colorMap.get(prevColor) - 1);

                if (colorMap.get(prevColor) == 0) {
                    colorMap.remove(prevColor);
                }
            }

            ballMap.put(ball, color);
            colorMap.put(color, colorMap.getOrDefault(color, 0) + 1);
        }

        return res;
    }

    public static void main(String[] args) {

    }
}
