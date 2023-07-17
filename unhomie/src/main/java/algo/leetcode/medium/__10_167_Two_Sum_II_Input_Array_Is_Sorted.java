package algo.leetcode.medium;

public class __10_167_Two_Sum_II_Input_Array_Is_Sorted {

    // Two pointer
    public static int[] twoSum(int[] numbers, int target) {
        int left = 0, right = numbers.length - 1;

        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if (sum > target) {
                right--;
            }
            if (sum < target) {
                left++;
            }
            if (sum == target) {
                return new int[]{left + 1, right + 1};
            }
        }
        return new int[0];
    }

    // Brute force solution O(n²) time complexity
    public static int[] twoSumBruteForce(int[] numbers, int target) {
        for (int i = 0; i < numbers.length; i++) {
            for (int j = i + 1; j < numbers.length; j++) {
                int sum = numbers[i] + numbers[j];
                if (sum > target) {
                    break;
                }
                if (sum == target) {
                    return new int[]{i + 1, j + 1};
                }
            }
        }
        return new int[0];
    }
}
