package algo.leetcode.hard;

public class __2_42_Trapping_Rain_Water {

    public static int trapOnSpace(int[] height) {
        int size = height.length;
        int[] maxLeft = new int[size];
        int[] maxRight = new int[size];

        int total = 0, maxLeftValue = 0, maxRightValue = 0;
        for (int i = 0; i < size; i++) {
            if (maxLeftValue < height[i]) {
                maxLeftValue = height[i];
            }

            if (maxRightValue < height[size - 1 - i]) {
                maxRightValue = height[size - 1 - i];
            }

            maxLeft[i] = maxLeftValue;
            maxRight[size - 1 - i] = maxRightValue;
        }

        for (int i = 0; i < size; i++) {
            int trapped = Math.min(maxLeft[i], maxRight[i]) - height[i];
            if (trapped > 0) {
                total += trapped;
            }
        }
        return total;
    }

    public static int trap(int[] height) {
        int left = 0, right = height.length - 1;
        int total = 0, maxLeft = height[left], maxRight = height[right];

        while (left < right) {
            if (maxLeft < maxRight) {
                left++;
                maxLeft = Math.max(maxLeft, height[left]);
                total += maxLeft - height[left];
            } else {
                right--;
                maxRight = Math.max(maxRight, height[right]);
                total += maxRight - height[right];
            }
        }

        return total;
    }
}
