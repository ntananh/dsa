package problem_namson_yt;

import java.util.Scanner;

/* 1^2 + 2^2 + ... + 2^n
 * (n = 1) => 1
 */

public class Problem_731 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        sc.nextLine();
        System.out.println(sumS(n));
        System.out.println(sumTailRecursion(n, 1));
    }

    public static int sumS(int n) {
        if (n == 1) return 1;
        return sumS(n - 1) + n * n;
    }

    public static int sumTailRecursion(int n, int sum) {
        if (n == 1) return sum;
        return sumTailRecursion(n - 1, sum + n * n);
    }

    public static int sum(int n) {
        int result = 1;

        for (int i = 2; i <= n; i++) {
            result += i;
        }
        return result;
    }
}
