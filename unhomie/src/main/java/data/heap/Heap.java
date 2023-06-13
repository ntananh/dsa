package data.heap;

public interface Heap<T> {

    void heapify(int[] data);

    void insertion(T node);

    void deletion(T node);

    T peek();
}
