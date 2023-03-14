package medium;


// * Definition for singly-linked list.
class ListNode {
      int val;
      ListNode next;
      ListNode() {}
      ListNode(int val) { this.val = val; }
      ListNode(int val, ListNode next) { this.val = val; this.next = next; }


}

class Solution {
    public ListNode swapPairs(ListNode head) {
        if (head == null) return null;
        if (head.next == null) return head;

        // THTQ
        ListNode nextNode = head.next;

        // Swap
        head.next = nextNode.next;
        nextNode.next = head;

        ListNode newNode = swapPairs(head.next);

        head.next = newNode;

        return nextNode;

    }

    public void printList(ListNode head){
        while (head != null){
            System.out.print(head.val + " ");
            head = head.next;
        }
        System.out.println();
    }
}

public class __2_24_Swap_Nodes_in_Pairs {
    public static void main(String[] args) {
        Solution s = new Solution();

        ListNode n1 = new ListNode(1);
        ListNode n2 = new ListNode(2);
        ListNode n3 = new ListNode(3);
        ListNode n4 = new ListNode(4);
        n1.next = n2; n2.next = n3; n3.next = n4;

        s.printList(n1);

        ListNode newList = s.swapPairs(n1);

        s.printList(newList);

    }

}
