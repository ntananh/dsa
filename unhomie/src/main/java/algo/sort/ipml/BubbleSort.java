package algo.sort.ipml;

import algo.sort.Sort;

/**
 * Idea: elements with smaller values will float to the front of the array
 */
public class BubbleSort implements Sort {
    @Override
    public void sort(int[] source) {
        for (int i = 0; i < source.length; i++) {
            for (int j = i + 1; j < source.length; j++) {
                if (source[i] > source[j]) {
                    swap(source, i, j);
                }
            }
        }
    }

    public void swap(int[] source, int i, int j) {
        int tmp = source[i];
        source[i] = source[j];
        source[j] = tmp;
    }
}
