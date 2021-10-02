package recursion;

public class PrintEl {

    public static void main(String[] args) {
        int[] arr = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        printElement(arr, 0);
    }


    public static void printElement(int[] arr, int index) {
        if (index < 0 | index >= arr.length)
            return;
        System.out.print(arr[index] + " ");
        printElement(arr, index + 1);
    }
}
