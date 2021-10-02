package stack;

import java.util.ArrayList;
import java.util.EmptyStackException;
import java.util.Iterator;
import java.util.List;

public class ArrayBaseStack<T> implements StackADT<T> {

    private final List<T> array;
    private int top = -1;

    public ArrayBaseStack(int initSize) {
        array = new ArrayList<>(initSize);
    }

    @Override
    public void push(T element) {
        top++;
        array.add(element);
    }

    @Override
    public void pop() {
        if (isEmpty()) throw new EmptyStackException();
        else {
            array.remove(top);
            top--;
        }
    }

    @Override
    public T top() {
        return array.get(top);
    }

    @Override
    public int size() {
        return array.size();
    }

    @Override
    public boolean isEmpty() {
        return array.isEmpty();
    }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            int index = 0;

            @Override
            public boolean hasNext() {
                return index < array.size();
            }

            @Override
            public T next() {
                return array.get(index++);
            }
        };
    }

    @Override
    public String toString() {
        if (isEmpty()) return "[]";
        else {
            StringBuilder sb = new StringBuilder(array.size());
            sb.append("[");

            for (T t : array) {
                sb.append(t).append(",");
            }
            sb.append("]");
            return sb.toString();
        }
    }
}
