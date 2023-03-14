package medium;

// Your MyCircularQueue object will be instantiated and called as such:

public class __1_622_Design_Circular_Queue {
    int front;
    int rear;
    int size;
    int count;
    int[] queue;

    public __1_622_Design_Circular_Queue(int k) {
        this.size = k;
        this.queue = new int[this.size];
        this.front = this.rear = -1;
        this.count = 0;

    }

    public boolean enQueue(int value) {
        if (isFull()) return false;

        // If not full
        this.rear++;
        if (this.rear == this.size){ // If rear out of end, move rear to 0 .EX: [0, 0, 4, 5, 6]
            this.rear = 0;
        }else if (isEmpty()){ // If empty front == rear
            this.front = this.rear;
        }

        // Add value
        this.queue[rear] = value;
        this.count++; // Increase count variable
        return true;

    }

    public boolean deQueue() {
        if (isEmpty()) return false;

        this.front++;
        if (this.front == this.size){
            this.front = 0;
        }

        count--;
        return true;

    }

    public int Front() {
        if (isEmpty()) {
            return -1;
        }
        else{
            return this.queue[front];
        }
    }

    public int Rear() {
        if (isEmpty()) {
            return -1;
        }
        else{
            return this.queue[rear];
        }
    }

    public boolean isEmpty() {
        // If count == 0 of queue return true else false
        return this.count == 0;
    }

    public boolean isFull() {
        // If count == size of queue return false else true
        return this.count == this.size;
    }

    public static void main(String[] args) {
        int k = 2;

        __1_622_Design_Circular_Queue obj = new __1_622_Design_Circular_Queue(k);
         boolean param_1 = obj.enQueue(2);
         boolean param_2 = obj.enQueue(2);
         boolean param_3 = obj.deQueue();
         boolean param_4 = obj.enQueue(3);
         boolean param_5 = obj.deQueue();
         boolean param_6 = obj.enQueue(3);
         boolean param_7 = obj.deQueue();
         boolean param_8 = obj.enQueue(3);
         boolean param_9 = obj.deQueue();
         int param_10 = obj.Front();



         System.out.println(param_1);
         System.out.println(param_2);
         System.out.println(param_3);
         System.out.println(param_4);
         System.out.println(param_5);
         System.out.println(param_6);
         System.out.println(param_7);
         System.out.println(param_8);
         System.out.println(param_9);
         System.out.println(param_10);
    }
}
