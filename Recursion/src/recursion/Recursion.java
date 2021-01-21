/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package recursion;

/**
 *
 * @author Dell
 */
public class Recursion {
    
    static int n1= 0, n2 = 1, n3;
    
    public static int GT(int n){
        if (n == 1) {
            return 1;
        }else{
            return n*GT(n-1);
        }
    }   
    
    public static int fibo(int n){
        if (n == 0) {
            return 0;
        }else if(n ==1){
            return 1;
        }
        else{
            return fibo(n-1)+ fibo(n-2);
        }
    }   
    
    public static void fiboPr (int count){
          if (count > 0) {
            n3 = n1 + n2;
            n1 = n2;
            n2 = n3;
            System.out.println(n3);
            fiboPr(count - 1);
          } 
    } 
    
    public static int power2th (int n){
        return switch (n) {
            case 0 -> 1;
            case 1 -> 2;
            default -> 2 * power2th (n-1);
        };
    }   
    
    public static int tong (int n){
        return switch (n) {
            case 0 -> 0;
            case 1 -> 1;
            default -> n + tong(n - 1);
        };
    }
    
    public static void dectoBin (int k){
        int quotient = k/2;
        int remainder = k%2;
        if (quotient > 0) {
            dectoBin(quotient);
        }
        System.out.print(remainder + " ");
    }
    
    public static int factorial(int n) {
        if (n == 1) {                       // base case
            return 1;
        } else {
            return n * factorial(n - 1);   // function calls itself
        }
      }
    
    public static void main(String[] args) {

        //System.out.println( "Giai thua: " + power2th (8));
        //System.out.println("Tong: "+ tong(10));
        //dectoBin(10);
        for (int i = 0; i < 5; i++) {
            System.out.println("2   mũ " + i + " = " +power2th(i));
        }
        //System.out.println("Factorial of 4 = " +factorial(4));
    }
    
    
}
