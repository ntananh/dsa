/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package heapsort;

/**
 *
 * @author Tony
 */

public class HeapSort {
    
    /*
    *   Size = arr.length;
    *
    *   Left child = 2 * i;
    *   Right child = (2 * i) + 1;
    *   Parent = (i - 1) / 2;
    *   Last parent = (size / 2) - 1;
    *
    */
    
    //Hiển thị mảng
    public void displayHeap(int[] arr){
        
        System.out.print("[ ");
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i] + ", ");
        }
        System.out.print("]");
        
    }
    
    
    // Sắp xếp
    public void sort(int[] arr){
        
        int size = arr.length;
        
        //Bắt đầu từ last parent node
        for(int i = (size / 2) - 1; i >= 0; i--){
            heapify(arr, size, i);
        }
        
        //Lên parent node trước
        for (int i = size - 1; i > 0; i--) {
            
            // Di chuyển root hiện tại đến end
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            
            heapify(arr, i, 0);
            
        }
    } 
    
    //Vun đống bắt đầu từ index = i
    public void heapify(int[] arr, int n, int i){
        
        int largest = i;            //Khởi tạo largest như gốc
        int left = (2 * i);     // Khởi tạo left child
        int right = (2 * i) + 1;    // Khởi tạo right child
        
         // Nếu nút con bên trái lớn hơn largest
        if ((left < n) && (arr[left] > arr[largest]))  {
            largest = left;
        }
        
        // Nếu nút con bên phải lớn hơn largest
        if ((right < n) && (arr[right] > arr[largest]))  {
            largest = right;
        }
        
         // Nếu largest không phải là root (max heap ==> root max)
        if(largest != i){
            
            //Nếu largest không phải là gốc thì chuyển 
            swap(arr, i, largest);
            
            //Vun đống lại các cây con phía dưới bị ảnh hưởng
            heapify(arr, n, largest);
        }
        
    }    
    
    public void swap(int[] arr, int i, int largest){
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
    }
   
}
