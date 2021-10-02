package problem_namson_yt;

import java.util.Scanner;

public class Problem_730 {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(); sc.nextLine();
        System.out.println(sumS(n));

    }

    public static int sumS(int n)  {
        if (n == 1) return 1;
        return  sumS(n - 1) + n;
    }

    public static int sum(int n) {
        int result = 1;

        for (int i = 2; i <= n; i++) {
            result += i;
        }
        return result;
    }
}
