package algo.leetcode.medium;

import java.util.HashMap;

public class __36_138_Copy_List_with_Random_Pointer {
    public static class Node {
        int val;
        Node next;
        Node random;

        public Node(int val) {
            this.val = val;
            this.next = null;
            this.random = null;
        }
    }

    // Using HashMap to create a copy while maintaining mapping
    public Node copyRandomList(final Node head) {
        if (head == null) return null; // Handle null case

        final HashMap<Node, Node> oldToCopy = new HashMap<>();
        Node cur = head;

        // First pass: Create a copy of each node and store in map
        while (cur != null) {
            oldToCopy.put(cur, new Node(cur.val));
            cur = cur.next;
        }

        cur = head;
        // Second pass: Assign next and random pointers
        while (cur != null) {
            final Node copiedNode = oldToCopy.get(cur);
            copiedNode.next = oldToCopy.get(cur.next); // Copy next pointer
            copiedNode.random = cur.random != null ? oldToCopy.get(cur.random) : null; // Copy random pointer
            cur = cur.next;
        }

        return oldToCopy.get(head);
    }
}
