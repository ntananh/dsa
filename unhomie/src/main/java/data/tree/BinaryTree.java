package data.tree;

public class BinaryTree {
    Node root;

    public void insert(int value) {
        root = insertKey(root, value);
    }

    public Node insertKey(Node root, int value) {
        if (root == null) {
            return new Node(value, null, null);
        }
        if (value > root.value) {
            root.right = insertKey(root.right, value);
        } else if (value < root.value) {
            root.left = insertKey(root.left, value);
        }
        return root;
    }

    public void delete(int value) {
        root = deleteKey(root, value);
    }

    public Node deleteKey(Node root, int value) {
        if (root == null) {
            return null;
        }
        if (value < root.value) {
            root.left = deleteKey(root.left, value);
        }else if (value > root.value) {
            root.right = deleteKey(root.right, value);
        } else {
            if (root.left == null) {
                return root.right;
            } else if (root.right == null) {
                return root.left;
            }
            root.value = minVal(root.right);
            root.right = deleteKey(root.right, root.value);
        }
        return root;
    }

    public int minVal(Node root) {
        int min = root.value;
        while (root.left != null) {
            min = root.left.value;
            root = root.left;
        }
        return min;
    }

    public void inOrder() {
        traverseInOrder(root);
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
        BinaryTree tree = new BinaryTree();
        tree.insert(8);
        tree.insert(3);
        tree.insert(1);
        tree.insert(6);
        tree.insert(7);
        tree.insert(10);
        tree.insert(14);
        tree.insert(4);

        tree.inOrder();

        tree.delete(1);
    }
}
