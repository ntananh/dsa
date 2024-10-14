package data.tree;

public class BinaryTree {
    TreeNode root;

    public void insert(int value) {
        root = insertKey(root, value);
    }

    public TreeNode insertKey(TreeNode root, int value) {
        if (root == null) {
            return new TreeNode(value, null, null);
        }
        if (value > root.val) {
            root.right = insertKey(root.right, value);
        } else if (value < root.val) {
            root.left = insertKey(root.left, value);
        }
        return root;
    }

    public void delete(int value) {
        root = deleteKey(root, value);
    }

    public TreeNode deleteKey(TreeNode root, int value) {
        if (root == null) {
            return null;
        }
        if (value < root.val) {
            root.left = deleteKey(root.left, value);
        } else if (value > root.val) {
            root.right = deleteKey(root.right, value);
        } else {
            if (root.left == null) {
                return root.right;
            } else if (root.right == null) {
                return root.left;
            }
            root.val = minVal(root.right);
            root.right = deleteKey(root.right, root.val);
        }
        return root;
    }

    public int minVal(TreeNode root) {
        int min = root.val;
        while (root.left != null) {
            min = root.left.val;
            root = root.left;
        }
        return min;
    }

    public void inOrder() {
        traverseInOrder(root);
    }
    // Traverse Inorder
    public void traverseInOrder(TreeNode treeNode) {
        if (treeNode != null) {
            traverseInOrder(treeNode.left);
            System.out.print(" " + treeNode.val);
            traverseInOrder(treeNode.right);
        }
    }

    public void traversePreOrder(TreeNode treeNode) {
        if (treeNode != null) {
            System.out.print(" " + treeNode.val);
            traversePreOrder(treeNode.left);
            traversePreOrder(treeNode.right);
        }
    }

    public void traversePostOrder(TreeNode treeNode) {
        if (treeNode != null) {
            traversePostOrder(treeNode.left);
            traversePostOrder(treeNode.right);
            System.out.print(" " + treeNode.val);
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
