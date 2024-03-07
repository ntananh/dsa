package algo.leetcode.easy;

import data.dto.ListNode;

public class __12_876_Middle_of_the_Linked_List {

	public ListNode middleNode(ListNode head) {
		// While slow moves one step forward, fast moves two steps forward.
        // Finally, when fast reaches the end, slow happens to be in the middle of the linked list

		ListNode slow = head, fast = head;

		while (fast != null && fast.next != null) {
			slow = slow.next;
			fast = fast.next.next;
		}

		return slow;
	}
}
