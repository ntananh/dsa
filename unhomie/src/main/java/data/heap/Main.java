package data.heap;

import java.util.Arrays;
import java.util.PriorityQueue;

public class Main {
    public static void main(String[] args) {
        MinHeap minHeap = new MinHeap();

        int[] unsortedArray = {10, 9, 8, 6, 7, 5, 4, 3, 2, 1};

        for (int n : unsortedArray) minHeap.add(n);

        int[] sortedArray = new int[unsortedArray.length];

        for (int i = 0; i < unsortedArray.length; i++) {
            sortedArray[i] = minHeap.poll();
        }

        System.out.println(Arrays.toString(unsortedArray));
        System.out.println(Arrays.toString(sortedArray));
    }
}
