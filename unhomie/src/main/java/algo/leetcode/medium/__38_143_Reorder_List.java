package algo.leetcode.medium;

import data.dto.ListNode;

public class __38_143_Reorder_List {

    /**
     * Reorders the given linked list in-place by alternating nodes from the beginning
     * and the reversed second half of the list.
     *
     * @param head The head of the linked list.
     */
    public void reorderList(ListNode head) {
        if (head == null || head.next == null) return;

        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        ListNode secondHalfHead = reverseList(slow.next);
        slow.next = null;

        ListNode firstHalfPointer = head, secondHalfPointer = secondHalfHead;
        while (firstHalfPointer != null && secondHalfPointer != null) {
            ListNode temp1 = firstHalfPointer.next;
            ListNode temp2 = secondHalfPointer.next;

            firstHalfPointer.next = secondHalfPointer;
            secondHalfPointer.next = temp1;

            firstHalfPointer = temp1;
            secondHalfPointer = temp2;
        }
    }

    /**
     * Reverses the given linked list.
     *
     * @param head The head of the linked list to be reversed.
     * @return The new head of the reversed linked list.
     */
    private ListNode reverseList(ListNode head) {
        ListNode prev = null;
        while (head != null) {
            ListNode nextNode = head.next;
            head.next = prev;
            prev = head;
            head = nextNode;
        }
        return prev;
    }
}
