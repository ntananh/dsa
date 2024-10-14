package algo.leetcode.hard;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class __3_51_N_Queens {

	public List<List<String>> solveNQueens(int n) {
		List<List<String>> res = new ArrayList<>();

		char[][] board = new char[n][n];
		for (char[] row : board) Arrays.fill(row, '.');


		backtrack(res, board, n, 0);

		return res;
	}

	private void backtrack(List<List<String>> res, char[][] board, int n, int row) {
		if (row == n) {
			res.add(toBoard(board));
			return;
		}

		for (int col = 0; col < n; col++) {
		}
	}

	private List<String> toBoard(char[][] board) {
		List<String> newBoard = new ArrayList<>();
		for (char[] row : board) newBoard.add(new String(row));
		return newBoard;
	}

	public static void main(String[] args) {

	}
}
