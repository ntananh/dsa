package recursion;

public class TailRecursion {


    public static int facNonTail(int n) {
        if (n == 1) return 1;
        return n  * facNonTail(n - 1);
    }

    public static int helper(int n, int a) {
        if (n ==1) return a;
        return  helper(n -1, n * a);
    }
    public static int facTail(int n) {
        return helper(n, 1);
    }

    public static void main(String[] args) {
        System.out.printf("%d ", facTail(5));
    }


}
