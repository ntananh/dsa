package data.tree;

public class Node {
    int data;
    Node leftNode;
    Node rightNode;

    public Node(int data, Node leftNode, Node rightNode) {
        this.data = data;
        this.leftNode = leftNode;
        this.rightNode = rightNode;
    }
}
