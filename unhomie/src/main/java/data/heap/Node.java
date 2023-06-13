package data.heap;

public class Node {
    public int data;
    public Node left;
    public Node right;

    @Override
    public String toString() {
        return "Node[" + data + ", " + left + ", " + right + ']';
    }
}
