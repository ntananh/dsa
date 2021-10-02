package recursion;

public class PascalTriangle {

    public static int calculator(int i, int j) {
        if (i == 1 || j == 1) return 1;
        return calculator(i - 1, j - 1) + calculator(i - 1, j);
    }


    public static void main(String[] args) {
        System.out.println(calculator(5,3));
    }



}
