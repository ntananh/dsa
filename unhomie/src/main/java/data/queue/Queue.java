package data.queue;

public interface Queue<T> extends Iterable<T> {
    void enqueue(T element);
    void dequeue();
    int size();
    boolean isEmpty();
}
