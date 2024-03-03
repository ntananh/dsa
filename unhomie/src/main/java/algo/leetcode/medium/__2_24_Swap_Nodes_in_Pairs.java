package algo.leetcode.medium;


import algo.utils.Utils;
import data.dto.ListNode;

public class __2_24_Swap_Nodes_in_Pairs {

	public ListNode swapPairs(ListNode head) {
		if (head == null) return null;
		if (head.next == null) return head;

		// THTQ
		ListNode nextNode = head.next;

		// Swap
		head.next = nextNode.next;
		nextNode.next = head;

		head.next = swapPairs(head.next);

		return nextNode;

	}

	public static void main(String[] args) {
		__2_24_Swap_Nodes_in_Pairs s = new __2_24_Swap_Nodes_in_Pairs();

		ListNode n1 = new ListNode(1);
		ListNode n2 = new ListNode(2);
		ListNode n3 = new ListNode(3);
		ListNode n4 = new ListNode(4);
		n1.next = n2;
		n2.next = n3;
		n3.next = n4;


        ListNode newList = s.swapPairs(n1);

		Utils.printList(newList);
	}

}
