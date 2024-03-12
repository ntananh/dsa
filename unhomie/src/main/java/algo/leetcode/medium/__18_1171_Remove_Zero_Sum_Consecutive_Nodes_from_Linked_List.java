package algo.leetcode.medium;

import algo.utils.Utils;
import data.dto.ListNode;

import java.util.HashMap;
import java.util.Map;

public class __18_1171_Remove_Zero_Sum_Consecutive_Nodes_from_Linked_List {

	public ListNode removeZeroSumSublists(ListNode head) {
		ListNode dummyNode = new ListNode(0, head);

		Map<Integer, ListNode> prefixSumMap = new HashMap<>();

		int sum = 0;
		ListNode current = dummyNode;
		while (current != null) {
			sum += current.val;
			prefixSumMap.put(sum, current);
			current = current.next;
		}

		sum = 0;
		current = dummyNode;
		while (current != null) {
			sum += current.val;
			current.next = prefixSumMap.get(sum).next;
			current = current.next;
		}

		return dummyNode.next;
	}

	public static void main(String[] args) {
		ListNode n1 = new ListNode(1);
		ListNode n2 = new ListNode(2);
		ListNode n3 = new ListNode(3);
		ListNode n4 = new ListNode(-3);
		ListNode n5 = new ListNode(-2);
		n1.next = n2;
		n2.next = n3;
		n3.next = n4;
		n4.next = n5;

		new __18_1171_Remove_Zero_Sum_Consecutive_Nodes_from_Linked_List().removeZeroSumSublists(n1);

		Utils.printLinkedList(n1);
	}
}
