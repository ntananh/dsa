package algo.leetcode.easy;

import data.tree.TreeNode;

import java.util.ArrayList;
import java.util.List;

public class __18_94_Binary_Tree_Inorder_Traversal {
	public static List<Integer> inorderTraversal(TreeNode root) {
		final List<Integer> result = new ArrayList<>();
		helper(result, root);
		return result;
	}

	public static void helper(List<Integer> result, TreeNode root) {
		if (root != null) {
			helper(result, root.left);
			result.add(root.val);
			helper(result, root.right);
		}
	}
}
