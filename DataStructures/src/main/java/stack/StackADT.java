package stack;

public interface StackADT<T> extends Iterable<T> {
    void push(T element);
    void pop();
    T top();
    int size();
    boolean isEmpty();
}

