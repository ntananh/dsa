package algo.leetcode.medium;

public class __22_174_Search_a_2D_Matrix {
	public static boolean searchMatrix(int[][] matrix, int target) {
		return binarySearch(matrix, target);
	}

	private static boolean binarySearch(int[][] matrix, int target) {
		// edge case
		if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
			return false;
		}

		final int ROWS = matrix.length, COLS = matrix[0].length, MAX_IDX = COLS - 1, MIN_IDX = 0;
		int top = 0, bot = ROWS - 1;

		while (top <= bot) {
			int row = (top + bot) / 2;
			if (target < matrix[row][MIN_IDX]) {
				bot = row - 1;
			} else if (target > matrix[row][MAX_IDX]) {
				top = row + 1;
			} else {
				break;
			}
		}

		if (!(top <= bot)) return false;
		int foundRow = (top + bot) / 2;
		int l = 0, r = COLS - 1;
		while (l <= r) {
			int mid = (l + r) / 2;
			if (target < matrix[foundRow][mid]) {
				r = mid - 1;
			} else if (target > matrix[foundRow][mid]) {
				l = mid + 1;
			} else {
				return true;
			}
		}

		return false;
	}

	private static boolean bruteForce(int[][] matrix, int target) {
		for (int i = 0; i < matrix.length; i++) {
			int l = 0, r = matrix[i].length - 1;
			for (int j = 0; j < matrix[i].length; j++) {
				if (matrix[i][j] == target) return true;
			}
		}
		return false;
	}

	public static void main(String[] args) {
		int[][] matrix = {{1, 3, 5, 7}, {10, 11, 16, 20}, {23, 30, 34, 60}};
		int[][] matrix2 = {{1, 3}};

		int target = 3;

		System.out.print(searchMatrix(matrix, target));
	}

}
