package algo.leetcode.easy;

import data.dto.ListNode;

public class __29_21_Merge_Two_Sorted_Lists {
    /**
     * <p>
     * You are given the heads of two sorted linked lists list1 and list2.
     * Merge the two lists into one sorted linked list and return the head of the new sorted linked list.
     * The new list should be made up of nodes from list1 and list2.
     * </p>
     *
     * @param list1 first list
     * @param list2 second list
     * @return the merged list
     */
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode();
        ListNode cur = dummy;

        while (list1 != null && list2 != null) {
            if (list1.val > list2.val) {
                cur.next = list2;
                list2 = list2.next;
            } else {
                cur.next = list1;
                list1 = list1.next;
            }
            cur = cur.next;
        }

        cur.next = (list1 != null) ? list1 : list2;

        return dummy.next;
    }
}
