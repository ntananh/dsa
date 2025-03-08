package algo.leetcode.easy;

public class __34_2379_Minimum_Recolors_to_Get_K_Consecutive_Black_Blocks {
    public static int minimumRecolors(String blocks, int k) {
        int res, w = 0;
        for (int i = 0; i < k; i++) {
            if (blocks.charAt(i) == 'W') w++;
        }

        res = w;
        for (int i = k; i < blocks.length(); i++) {
            if (blocks.charAt(i) == 'W') w++;
            if (blocks.charAt(i - k) == 'W') w--;
            res = Math.min(w, res);
        }

        return res;
    }
}
