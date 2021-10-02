package recursion;

public class Fibonacci {

    public static void main(String[] args) {
        System.out.println(fiboTail(6));
        System.out.println(fiboRecursion(6));


    }

    static int[] res = new int[1000];
    public static int fib(int n) {
        if (res[n] != 0) return res[n];
        System.out.println("Tinh: res[" + n + "]");
        if (n <= 2) {
            res[1] = 1;
            res[2] = 1;
            return 1;
        }
        res[n] = fib(n - 1) + fib(n - 2);
        return res[n];
    }

    public static int fiboRecursion(int n) {
        if (n <= 2) return 1;
        return fiboRecursion(n - 1) + fiboRecursion(n - 2);
    }

    public static int fiboTail(int n) {
        return foo(n, 0, 1);
    }

    public static int foo(int n, int a, int b){
        if (n == 0) return a;
        if (n == 1) return b;
        return foo(n -1, b, a + b);
    }
}
