/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package insertsort;

import java.util.Arrays;

/**
 *
 * @author Dell
 */
public class InsertSort {

    /**
     * @param args the command line arguments
     */
    
    public static void main(String[] args) {
        // TODO code application logic here
        Sort s = new Sort();
        int[] arr = {5,2,23,56,7,34};
        System.out.println("Mang chua sap xep: " + Arrays.toString(arr));
        s.sortInsertion(arr);
        //s.insertSort(arr);
        //s.reInsSort(arr, 5);
        System.out.println("Mang da sap xep:   " + Arrays.toString(arr));
    }
     
}
