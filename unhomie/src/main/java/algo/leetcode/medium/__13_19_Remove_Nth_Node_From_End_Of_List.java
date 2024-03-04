package algo.leetcode.medium;

import algo.utils.Utils;
import data.dto.ListNode;

public class __13_19_Remove_Nth_Node_From_End_Of_List {

	public ListNode removeNthFromEnd(ListNode head, int n) {
		ListNode fast = head, slow = head;

		for (int i = 0; i < n; i++) {
			fast = fast.next;
		}

		if (fast == null) {
			return head.next;
		}

		while (fast.next != null) {
			fast = fast.next;
			slow = slow.next;
		}

        return head;
	}

	public static void main(String[] args) {
		ListNode n1 = new ListNode(1);
		ListNode n2 = new ListNode(2);
		ListNode n3 = new ListNode(3);
		ListNode n4 = new ListNode(4);
		n1.next = n2;
		n2.next = n3;
		n3.next = n4;

		__13_19_Remove_Nth_Node_From_End_Of_List s = new __13_19_Remove_Nth_Node_From_End_Of_List();

		s.removeNthFromEnd(n1, 2);

		Utils.printList(n1);
	}
}

