package Easy;

class Node {
    int val;
    int min;
    Node next;

    Node(int val, int min){this.val = val; this.min = min; }
    Node(int val, int min, Node next){this.val = val; this.min = min; this.next = next; }
}

class MinStack {
    Node head;
    /** initialize your data structure here. */
    public MinStack() {
        this.head = null;
    }

    public void push(int val) {
        if (head == null){
            head = new Node(val, val);
        }else {
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


public class __1_155_Min_Stack {
    public static void main(String[] args) {
        MinStack obj = new MinStack();
        obj.push(-2);
        obj.push(0);
        obj.push(-3);
        System.out.println(obj.getMin());
        obj.pop();
        System.out.println(obj.getMin());


    }
}
