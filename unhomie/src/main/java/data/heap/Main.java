package data.heap;

import data.heap.impl.MaxHeap;
import data.heap.impl.MinHeap;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        Heap minHeap = new MinHeap();
        Heap maxHeap = new MaxHeap();

        int[] unsortedArray = {10, 9, 8, 6, 7, 5, 4, 3, 2, 1};
        int[] unsortedArrayForMax = {2, 1, 4, 3, 6, 7, 5, 8, 9, 10};

        for (int n : unsortedArray) minHeap.add(n);

        for (int n : unsortedArrayForMax) maxHeap.add(n);

        int[] sortedArray = new int[unsortedArray.length];
        int[] sortedArrayForMax = new int[unsortedArrayForMax.length];

        for (int i = 0; i < unsortedArray.length; i++) {
            sortedArray[i] = minHeap.poll();
        }

        for (int i = 0; i < unsortedArrayForMax.length; i++) {
            sortedArrayForMax[i] = maxHeap.poll();
        }

        System.out.println("Min heap");
        System.out.println(Arrays.toString(unsortedArray));
        System.out.println(Arrays.toString(sortedArray));
        System.out.println("---------------------------------");
        System.out.println("Max heap");
        System.out.println(Arrays.toString(unsortedArrayForMax));
        System.out.println(Arrays.toString(sortedArrayForMax));
    }
}
