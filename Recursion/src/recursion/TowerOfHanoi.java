package recursion;

public class TowerOfHanoi {

    public static void main(String[] args) {
        solver(3, 'A', 'B', 'C');
    }

    static void solver(int n, char begin, char middle, char end){
        if (n == 1) {
            System.out.println("Move " + begin + " to "  + end);
        }
        else {
            solver(n - 1, begin, end, middle);
            solver(1, begin, middle , end);
            solver(n - 1, middle, begin, end);
        }
    }


}
