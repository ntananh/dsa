package algo.leetcode.medium;

import data.dto.ListNode;

public class __39_19_Remove_Nth_Node_From_End_of_List {
    public ListNode removeNthFromEnd(ListNode head, int n) {

        ListNode dummy = new ListNode(0);
        dummy.next = head;

        ListNode slow = dummy, fast = dummy;
        for (int i = 0; i <= n; i++) {
            fast = fast.next;
        }

        while (fast != null) {
            slow = slow.next;
            fast = fast.next;
        }

        ListNode target = slow.next;
        slow.next = target.next;
        target.next = null;

        return dummy.next;
    }
}
