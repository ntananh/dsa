package algo.leetcode.medium;

import data.dto.ListNode;

public class __40_2_Add_Two_Numbers {
    public static ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        final ListNode dummy = new ListNode(0);
        ListNode current = dummy;
        int carry = 0;

        while (l1 != null || l2 != null || carry != 0) {
            final int x = (l1 != null) ? l1.val : 0;
            final int y = (l2 != null) ? l2.val : 0;

            final int sum = x + y + carry;
            carry = sum / 10;

            current.next = new ListNode(sum % 10);
            current = current.next;

            if (l1 != null) l1 = l1.next;
            if (l2 != null) l2 = l2.next;
        }
        return dummy.next;
    }
}
