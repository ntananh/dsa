package course.educative.dsawithgeneric.arraybaselist;

import java.util.AbstractList;

public class ArrayStack<T> extends AbstractList<T> {

    private T[] a;
    private int n = 0;

    public int size() {
        return n;
    }

    public T get(int i) {
        return a[i];
    }

    public T set(int i, T x) {
        T y = a[i];
        a[i] = x;
        return y;
    }

    public void add(int i, T x) {
        if (n + 1 > a.length) resize();
        for (int j = n; j > i; j--)
            a[j] = a[j - i];
        a[i] = x;
        n++;
    }

    private void resize() {
        // TODO: add implementation
    }

}
