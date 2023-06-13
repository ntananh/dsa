package data.tree;

public class BinaryTree {
    Node root;

    public Node insert(Node root, int value) {
        if (root == null) return new Node(value, null, null);
        if (value > root.value) root.right = insert(root.right, value);
        else if (value < root.value) root.left = insert(root.left, value);
        return root;
    }

    // Traverse Inorder
    public void traverseInOrder(Node node) {
        if (node != null) {
            traverseInOrder(node.left);
            System.out.print(" " + node.value);
            traverseInOrder(node.right);
        }
    }

    public void traversePreOrder(Node node) {
        if (node != null) {
            System.out.print(" " + node.value);
            traversePreOrder(node.left);
            traversePreOrder(node.right);
        }
    }

    public void traversePostOrder(Node node) {
        if (node != null) {
            traversePostOrder(node.left);
            traversePostOrder(node.right);
            System.out.print(" " + node.value);
        }
    }

    public static void main(String[] args) {
        BinaryTree binaryTree = new BinaryTree();
        binaryTree.root = new Node(3, null, null);
        binaryTree.insert(binaryTree.root, 5);
        binaryTree.insert(binaryTree.root, 6);
        binaryTree.insert(binaryTree.root, 4);
        binaryTree.insert(binaryTree.root, 7);
        binaryTree.insert(binaryTree.root, 2);
        binaryTree.insert(binaryTree.root, 1);

        binaryTree.traverseInOrder(binaryTree.root);
    }
}
