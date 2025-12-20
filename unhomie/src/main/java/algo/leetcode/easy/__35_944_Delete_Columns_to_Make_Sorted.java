package algo.leetcode.easy;


public class __35_944_Delete_Columns_to_Make_Sorted {
    public static int minDeletionSize(final String[] strs) {
        int deletions = 0;
        final int numRows = strs.length;
        final int numCols = strs[0].length();

        for (int col = 0; col < numCols; col++) {
            for (int row = 0; row < numRows - 1; row++) {
                if (strs[row].charAt(col) > strs[row + 1].charAt(col)) {
                    deletions++;
                    break;
                }
            }
        }

        return deletions;
    }
}

