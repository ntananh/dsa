/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package bubblesort;

import java.util.Arrays;

/**
 *
 * @author Dell
 */
public class BubbleSort {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        int[] arr = {64, 25, 12, 22, 11}; 
        System.out.println("Mảng chưa sắp xếp: " + Arrays.toString(arr));
        bubbleSort(arr);
        System.out.println("Mảng đã sắp xếp: " + Arrays.toString(arr));
    }

    private static void bubbleSort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[j] < arr[i]) {
                    int temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                }       
            }
        }   
    }

}
