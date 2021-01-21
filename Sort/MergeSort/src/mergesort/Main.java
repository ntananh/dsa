/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package mergesort;
import java.util.Arrays;

/**
 *
 * @author Dell
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        //define array to be sorted
        MergeSort mergesort = new MergeSort();
        int[] intArray = { 10,23,-11,54,2,9,-10,45 };
        //print the original array
        System.out.println("Original Array : " + Arrays.toString(intArray));
        //call mergeSort routine
        mergesort.mergeSort(intArray);
        //print the sorted array
        System.out.println("Sorted Array : " + Arrays.toString(intArray));
    }
    
}
