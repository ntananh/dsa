package recursion;

import org.w3c.dom.ls.LSOutput;

import java.util.Arrays;

public class ExponentialRecursion {
    public static void main(String[] args) {
        int[] arr = {5,6,3,7,2,1,4};

        Arrays.stream(arr).forEach(n -> System.out.print(n + " "));
        System.out.println();
        sort(arr, arr.length, 0);
        Arrays.stream(arr).forEach(n -> System.out.print(n + " "));
    }

    public static void sort(int[] arr, int n, int i){
        int j, swap;

        for (j = i + 1; j < n; j++) {
            if (arr[j] < arr[i]) {
                swap = arr[i];
                arr[i] = arr[j];
                arr[j] = swap;
            }
            sort(arr, n, i + 1);
        }
        
    }
}
