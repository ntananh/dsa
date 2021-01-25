/*
 * 
 * Insertion Sort
 * 
 */
package insertsort;

import java.util.Arrays;

/**
 * @author Tony
 */
public class Sort {
    
    //Normal insertion sort
    public void sortInsertion(int [] sort_arr){
        for (int i = 1; i < sort_arr.length; i++) {
            int current = sort_arr[i]; //Choose value 
            int idx = i - 1;
            
            while (idx >= 0 && sort_arr[idx] > current) {                
                sort_arr[idx + 1] = sort_arr[idx];
                idx--;
            }
            sort_arr[++idx] = current;
        }
    }
    
    //Recursive insertion sort
    public void reInsSort(int[] a, int n){
        if (n > 1)  reInsSort(a, n - 1);
        int i = n - 1;
        int x = a[n];
        while (i >= 0 && a[i] > x) {            
            a[i + 1] = a[i];
            i--;
            
            System.out.println("\t\t Sort :" +Arrays.toString(a));
        }
        a[i+1] = x;
    }
    

}
