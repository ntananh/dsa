package algo.leetcode.medium;

/*
 * Idea: Use two pointer to calculate
 * The key is: we always want to have max height and max width
 * If the height in left less than right side, move the left forward.
 * Otherwise, move the right pointer.
 */
public class __10_11_Container_With_Most_Water {
    public static int maxArea(int[] height) {
        int left = 0, right = height.length - 1;
        int curArea, res = 0;

        while (left < right) {
            curArea = (right - left) * Math.min(height[left], height[right]);
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
            res = Math.max(res, curArea);
        }
        return res;
    }

    public static int maxAreaBruteForce(int[] height) {
        int res = 0;
        for (int i = 0; i < height.length - 1; i++) {
            for (int j = i + 1; j < height.length; j++) {
                int w = j - i, h = Math.min(height[i], height[j]);
                int area = w * h;
                res = Math.max(res, area);
            }
        }
        return res;
    }
}
