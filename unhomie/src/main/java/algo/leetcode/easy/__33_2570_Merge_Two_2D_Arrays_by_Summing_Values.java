package algo.leetcode.easy;

import java.util.ArrayList;
import java.util.List;

public class __33_2570_Merge_Two_2D_Arrays_by_Summing_Values {
    public int[][] mergeArrays(int[][] nums1, int[][] nums2) {
         int i = 0, j = 0, n1 = nums1.length, n2 = nums2.length;

        final List<int[]> res = new ArrayList<>();
        while (i < n1 && j < n2) {
            int id1 = nums1[i][0], val1 = nums1[i][1];
            int id2 = nums2[j][0], val2 = nums2[j][1];

            if (id1 == id2) {
                res.add(new int[] { id1, val1 + val2 });
                i++;
                j++;
            } else if (id1 < id2) {
                res.add(nums1[i++]);
            } else {
                res.add(nums2[j++]);
            }

        }

        while (i < n1) res.add(nums1[i++]);

        while (j < n2) res.add(nums2[j++]);

        return res.toArray(new int[res.size()][]);
    }
}
