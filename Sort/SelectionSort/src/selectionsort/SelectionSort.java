/*
 * 
 * Selection Sort
 * 
 */
package selectionsort;

import java.util.Arrays;

/**
 *
 * @author Tony
 */
public class SelectionSort {
    
    public static void main(String[] args) {
        int[] arr = {64, 25, 12, 22, 11}; 
        System.out.println("Mảng chưa sắp xếp: " + Arrays.toString(arr));
        //selectSort(arr);
        recursionSelectSort(arr, arr.length, 0);
        System.out.println("Mảng đã sắp xếp: " + Arrays.toString(arr));
        
    }
    
    // Swap the found minimum element with the first 
    public static void swap(int arr[], int i, int min_idx){
        int temp = arr[i];
        arr[i] = arr[min_idx];
        arr[min_idx] = temp;
    }
    
    public static void selectSort(int[] arr){
        int min_value, min_idx;
        
        for (int i = 0; i < arr.length - 1; i++) {
            min_idx = i;
            min_value = arr[i];
            
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[j] < arr[min_idx]) {
                    min_idx = j;
                    min_value = arr[min_idx];
                }
            }
            
            if (min_idx != i) {
                swap(arr, i, min_idx);
            } 
        }
    }
    
    // Return minimum index
    static int recurFindMinIdx(int[] arr, int i, int j){
        if (i == j) return j;
        
        int min_idx = recurFindMinIdx(arr, i + 1, j);
        
        return (arr[i] < arr[min_idx]) ? i : min_idx;  
    }
    
    //Recursive selection sort
    public static void recursionSelectSort(int[] arr, int n, int idx){
        if (idx == n) return;
        
        int min_idx = recurFindMinIdx(arr, idx, n - 1);
        if (min_idx != idx){
            swap(arr, idx, min_idx);
        }
        
        recursionSelectSort(arr, n, idx + 1);
        
    }
    
    
    
}
