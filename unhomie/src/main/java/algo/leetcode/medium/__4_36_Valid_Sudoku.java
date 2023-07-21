package algo.leetcode.medium;

import java.util.HashSet;
import java.util.Set;


/*
 * Idea     : add seen values to set for column and row
 * For cube : get cube idx by current column idx / 3 and current row idx /3.
 * Example  : row idx (5) and column idx (5) => cube is (1,1)
 *            row idx (7) and column idx (8) => cube is (2,2)
 */
public class __4_36_Valid_Sudoku {

    public static boolean isValidSudoku(char[][] board) {
        Set<String> seen = new HashSet<>();

        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                String col = "c" + c + "[" + board[r][c] + "]";
                String row = "r" + r + "[" + board[r][c] + "]";
                String cube = r / 3 + "[" + board[r][c] + "]" + c / 3;
                if (board[r][c] != '.') {
                    if (!seen.add(col) || !seen.add(row) || !seen.add(cube)) {
                        return false;
                    }
                }
            }
        }

        return true;
    }

    public static void main(String[] args) {
        char[][] valid = {
                {'5', '3', '.', '.', '7', '.', '.', '.', '.'},
                {'6', '.', '.', '1', '9', '5', '.', '.', '.'},
                {'.', '9', '8', '.', '.', '.', '.', '6', '.'},

                {'8', '.', '.', '.', '6', '.', '.', '.', '3'},
                {'4', '.', '.', '8', '.', '3', '.', '.', '1'},
                {'7', '.', '.', '.', '2', '.', '.', '.', '6'},

                {'.', '6', '.', '.', '.', '.', '2', '8', '.'},
                {'.', '.', '.', '4', '1', '9', '.', '.', '5'},
                {'.', '.', '.', '.', '8', '.', '.', '7', '9'}};

        char[][] wrong = {
                {'.', '.', '4', '.', '.', '.', '6', '3', '.'},
                {'.', '.', '.', '.', '.', '.', '.', '.', '.'},
                {'5', '.', '.', '.', '.', '.', '.', '9', '.'},

                {'.', '.', '.', '5', '6', '.', '.', '.', '.'},
                {'4', '.', '3', '.', '.', '.', '.', '.', '1'},
                {'.', '.', '.', '7', '.', '.', '.', '.', '.'},

                {'.', '.', '.', '5', '.', '.', '.', '.', '.'},
                {'.', '.', '.', '.', '.', '.', '.', '.', '.'},
                {'.', '.', '.', '.', '.', '.', '.', '.', '.'}};

        boolean expected = isValidSudoku(valid);
        boolean invalid = isValidSudoku(wrong);
        System.out.println(expected);
        System.out.println(invalid);
    }
}
