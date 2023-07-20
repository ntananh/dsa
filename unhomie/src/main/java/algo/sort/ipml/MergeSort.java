package algo.sort.ipml;

import algo.sort.Sort;

public class MergeSort implements Sort {

    @Override
    public void sort(int[] source) {
        sort(source, 0, source.length - 1);
    }

    public void sort(int[] data, int left, int right) {
        if (left < right) {
            int mid = (left + right) / 2;

            sort(data, left, mid);
            sort(data, mid + 1, right);

            merge(data, left, mid, right);
        }
    }

    private void merge(int[] arr, int left, int mid, int right) {
        int lSize = mid - left + 1;
        int rSize = right - mid;

        int[] lArr = new int[lSize];
        int[] rArr = new int[rSize];
        // copy data from original array to 2 arrays
        for (int i = 0; i < lSize; i++) {
            lArr[i] = arr[left + i];
        }
        for (int i = 0; i < rSize; i++) {
            rArr[i] = arr[mid + 1 + i];
        }

        // keep track index of left array and right array
        // index of original array is left because we not always merge at start of array(0)
        int lIdx = 0, rIdx = 0, arrIdx = left;
        while (lIdx < lSize && rIdx < rSize) {
            if (lArr[lIdx] < rArr[rIdx]) {
                arr[arrIdx] = lArr[lIdx];
                lIdx++;
            } else {
                arr[arrIdx] = rArr[rIdx];
                rIdx++;
            }
            arrIdx++;
        }

        while (lIdx < lSize) {
            arr[arrIdx] = lArr[lIdx];
            arrIdx++;
            lIdx++;
        }

        while (rIdx < rSize) {
            arr[arrIdx] = rArr[rIdx];
            arrIdx++;
            rIdx++;
        }
    }
}
