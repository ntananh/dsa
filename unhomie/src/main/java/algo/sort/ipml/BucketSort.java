package algo.sort.ipml;

import algo.sort.Sort;

import java.util.Collections;
import java.util.LinkedList;
import java.util.List;

public class BucketSort implements Sort {
    @Override
    @SuppressWarnings("unchecked")
    public void sort(int[] source) {
        int bucketSize = source.length;
        List<Integer>[] buckets = new List[bucketSize];

        // in case collision hash
        for (int i = 0; i < bucketSize; i++) buckets[i] = new LinkedList<>();

        // put value to bucket
        for (int value : source) {
            buckets[hash(value, bucketSize)].add(value);
        }

        // sort each bucket using lib
        for (int i = 0; i < bucketSize; i++) {
            Collections.sort(buckets[i]);
        }

        int arrayIdx = 0;
        for (int i = 0; i < bucketSize; i++) {
            for (int j = 0; j < buckets[i].size(); j++) {
                source[arrayIdx++] = buckets[i].get(j);
            }
        }
    }

    private static int hash(int num, int bucketSize) {
        return num / bucketSize;
    }
}
