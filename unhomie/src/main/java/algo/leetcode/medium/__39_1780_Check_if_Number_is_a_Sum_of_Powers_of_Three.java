package algo.leetcode.medium;

public class __39_1780_Check_if_Number_is_a_Sum_of_Powers_of_Three {
    public static boolean checkPowersOfThree(int n) {
        while (n > 1) {
            if (n % 3 == 2) {
                return false;
            }
            n /= 3;
        }
        return true;
    }
}
