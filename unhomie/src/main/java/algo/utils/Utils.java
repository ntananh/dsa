package algo.utils;

import data.dto.ListNode;

public class Utils {

	public static void printLinkedList(ListNode head) {
		while (head != null) {
			System.out.print(head.val + " -> ");
			head = head.next;
		}
		System.out.println("null");
	}
}
