/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package heapsort;

/**
 *
 * @author Tấn Anh
 */
public class Main {
    public static void main(String[] args) {
        
        HeapSort hs = new HeapSort();
        
        int[] arr = { 4, 10, 3, 5, 1 };

        
        hs.displayHeap(arr);
        hs.sort(arr);
        System.out.println("\n\nMảng sau khi sắp xếp: ");
        hs.displayHeap(arr);
        
    }
}
