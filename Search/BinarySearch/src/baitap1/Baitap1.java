/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package baitap1;
import java.util.Scanner;
/**
 *
 * @author Tony
 */
public class Baitap1 {
    
    
    int a[];
    
    public void nhapMang(){
            Scanner sn = new Scanner(System.in);
            System.out.print("Nhập số phần tử của mảng: ");
            int n = sn.nextInt();
            // khởi tạo mảng arr
            a = new int[n];
            System.out.print("Nhập các phần tử của mảng: \n");
            for (int i = 0; i < n; i++) {
                System.out.printf("a[%d] = ", i);
                a[i] = sn.nextInt();
            }
    }
    
    public void xuatMang(){
        for (int i = 0;i < a.length; i++){
            System.out.print(a[i] + "\t");
        }
        System.out.println();
    }
    
    public boolean kemTraNguyenTo(int n){
        if(n < 2)
            return false;
        for(int i = 2;i <= Math.sqrt(n); i++){
            if(n%i == 0){
                return false;
            }
        }
        return true;
    }
   
    public void xuatSoNguyenTo(){
        for (int i=0;i < a.length;i++){
            if(kemTraNguyenTo(a[i])){
                System.out.print(a[i]+ "\t");
            }
        }  
        System.out.println();
    }
    
    public void sapXepMang(){
        for(int i = 0; i < a.length - 1; i++){
            for(int j = i + 1; j < a.length ; j++){
                if(a[i] > a[j]){
                    int temp = a[i];
                    a[i] = a[j];
                    a[j] = temp; 
                }      
            }  
        }
    }    
    //
    public void timkiem(){
        int l =  0;
        int r = a.length -1 ;
        Scanner sn = new Scanner(System.in);
        System.out.print("Nhập giá trị cần tìm:  ");
        int value = sn.nextInt();
        if (r >= l) {
            int mid = l + (r - l) / 2;
            
            if (a[mid] == value){
                System.out.println("Giá trị "+ value + " nằm ở vị trí thứ " + mid);
            } 
            if (a[mid] > value){
                l = 1;
                r = mid -1;
                
            }else{
                l = mid + 1;
            }
        }else{
            System.out.println("Khong co gia tri trong mang");
        }        
    }
    
    public static void main(String[] args) {
        Baitap1 bt = new Baitap1();
        bt.nhapMang();

        bt.sapXepMang();
  
        System.out.println("Mang da sap xep: ");
        bt.xuatMang();
        
       // System.out.print("Cac so nguyen to trong mang da nhap la :  ");
       //bt.xuatSoNguyenTo();
        
        bt.timkiem();
      
    }
   
}



