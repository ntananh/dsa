package algo.leetcode.medium;

import java.util.ArrayList;
import java.util.List;

/*
 * Idea:
 * - Use 2 stack inside to keep track min value
 * - Use node with min value
 */
public class __11_155_Min_Stack {
    static class MinStack {

        private final List<Integer> stack;
        private final List<Integer> minStack;

        public MinStack() {
            stack = new ArrayList<>();
            minStack = new ArrayList<>();
        }

        public void push(int val) {
            this.stack.add(val);
            int min = val;
            if (minStack.size() > 0) {
                min = Math.min(val, minStack.get(minStack.size() - 1));
            }
            this.minStack.add(min);
        }

        public void pop() {
            if (this.stack.size() > 0) {
                this.stack.remove(this.stack.size() - 1);
            }
            if (this.minStack.size() > 0) {
                this.minStack.remove(this.minStack.size() - 1);
            }
        }

        public int top() {
            if (this.stack.size() == 0) {
                return 0;
            }
            return this.stack.get(this.stack.size() - 1);
        }

        public int getMin() {
            if (this.minStack.size() == 0) {
                return 0;
            }
            return this.minStack.get(this.minStack.size() - 1);
        }
    }

    static class MinStackWithNode {
        Node head;

        public MinStackWithNode() {
            this.head = null;
        }

        public void push(int val) {
            if (head == null) {
                head = new Node(val, val);
            } else {
                head = new Node(val, Math.min(val, head.min), head);
            }
        }

        public void pop() {
            head = head.next;
        }

        public int top() {
            return head.val;
        }

        public int getMin() {
            return head.min;
        }
    }

    static class Node {
        int val;
        int min;
        Node next;

        Node(int val, int min) {
            this.val = val;
            this.min = min;
        }

        Node(int val, int min, Node next) {
            this.val = val;
            this.min = min;
            this.next = next;
        }
    }

    public static void main(String[] args) {
        MinStackWithNode minStack = new MinStackWithNode();
        minStack.push(-2);
        minStack.push(0);
        minStack.push(-3);
        System.out.println(minStack.getMin()); // return -3
        minStack.pop();
        System.out.println(minStack.top());    // return 0
        System.out.println(minStack.getMin()); // return -2
    }
}
