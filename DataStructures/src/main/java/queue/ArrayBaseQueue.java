package queue;

import java.util.Iterator;
import java.util.WeakHashMap;

public class ArrayBaseQueue<T> implements Queue<T> {
    private final T[] array;
    private int front;
    private int rear;
    private final int size;

    public ArrayBaseQueue(int maxSize) {
        front = rear = 0;
        size = maxSize + 1;
        array = (T[]) new Object[size];
    }

    @Override
    public void enqueue(T element) {
        array[rear] = element;
        if (++rear == size) rear = 0;
        if (rear == front) throw new RuntimeException("Queue is full!");
    }

    @Override
    public void dequeue() {
        if (isEmpty()) throw new RuntimeException("Queue is empty!");
        if (++front == size) front = 0;
    }

    @Override
    public int size() {
        if (front > rear) return (rear + size - front);
        return rear - front;
    }

    @Override
    public boolean isEmpty() {
        return front == rear;
    }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            int index = 0;

            @Override
            public boolean hasNext() {
                return index < size;
            }

            @Override
            public T next() {
                return array[index++];
            }
        };
    }
}
