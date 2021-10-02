package recursion;

public class ReverseLinkedList {

    public static ListNode reverseList(ListNode head) {
        if (head == null || head.next == null) return head;

        ListNode newList = reverseList(head.next);

        ListNode nextNode = head.next;
        nextNode.next = head;
        head.next = null;
        return newList;
    }

    public static ListNode nonRecur(ListNode head) {
        ListNode curNode = head;

        while (curNode != null && curNode.next != null) {
            ListNode nextNode = curNode.next;
            curNode.next =  nextNode.next;
            nextNode.next = head;
            head = nextNode;
        }
        return head;
    }

    public static void printLinkedList(ListNode head) {
        while (head != null) {
            System.out.print(head.val + " ");
            head = head.next;
        }
    }

    public static void main(String[] args) {
        ListNode n1 = new ListNode(1);
        ListNode n2 = new ListNode(2);
        ListNode n3 = new ListNode(3);
        ListNode n4 = new ListNode(4);
        ListNode n5 = new ListNode(5);
        ListNode n6 = new ListNode(6);
        n1.next = n2;
        n2.next = n3;
        n3.next = n4;
        n4.next = n5;
        n5.next = n6;

        printLinkedList(n1);
        ListNode newList = reverseList(n1);
        System.out.println();
        printLinkedList(newList);

    }
}

