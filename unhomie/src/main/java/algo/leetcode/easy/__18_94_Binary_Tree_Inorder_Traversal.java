package algo.leetcode.easy;

import data.tree.Node;

import java.util.ArrayList;
import java.util.List;

public class __18_94_Binary_Tree_Inorder_Traversal {
	public static List<Integer> inorderTraversal(Node root) {
		final List<Integer> result = new ArrayList<>();
		helper(result, root);
		return result;
	}

	public static void helper(List<Integer> result, Node root) {
		if (root != null) {
			helper(result, root.left);
			result.add(root.value);
			helper(result, root.right);
		}
	}
}
