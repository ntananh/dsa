package algo.leetcode.easy;

import data.dto.ListNode;

public class __28_206_Reverse_Linked_List {

    /**
     * <p>
     * Given the beginning of a singly linked list head,
     * reverse the list, and return the new beginning of the list.
     * </p>
     *
     * @param head the linked list head node
     * @return the new head
     */
    public static ListNode reverseList(ListNode head) {
        if (head == null || head.next == null) return head;

        final ListNode newList = reverseList(head.next);
        head.next.next = head;
        head.next = null;

        return newList;
    }
}
