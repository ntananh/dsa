package backtracking;

public class BinaryGenerator {

    public static void main(String[] args) {
        generator(1,2);
    }

    public static String result = "";
    public static void generator(int i, int number) {
        for (int j = 0; j < 2; j++) {
           result += String.valueOf(j);
            if (i == number) {
                System.out.println(result);
            } else  {
                generator(i + 1, number);
            }
            result = result.substring(0, result.length() - 1);
        }
    }

}
