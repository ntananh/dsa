package algo.sort.ipml;

import algo.sort.Sort;

import java.util.ArrayList;
import java.util.List;

/**
 * Idea: elements with smaller values will float to the front of the array
 */
public class BubbleSort implements Sort<Integer> {
    @Override
    public List<Integer> sort(List<Integer> source) {
        List<Integer> sorted = new ArrayList<>(source);

        for (int i = 0; i < source.size(); i++) {
            for (int j = i + 1; j < source.size(); j++) {
                if (sorted.get(i) > sorted.get(j)) {
                    swap(sorted, i, j);
                }
            }
        }
        return sorted;
    }

    public void swap(List<Integer> source, int i, int j) {
        int valueAtI  = source.get(i);
        int valueAtJ  = source.get(j);
        source.set(i, valueAtJ);
        source.set(j, valueAtI);
    }
}
