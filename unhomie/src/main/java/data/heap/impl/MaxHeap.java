package data.heap.impl;

import data.heap.Heap;

public class MaxHeap extends Heap {

    @Override
    public int peek() {
        if (size == 0) throw new IllegalStateException();
        return items[0];
    }

    @Override
    public int poll() {
        if (size == 0) throw new IllegalStateException();
        int item = items[0];
        items[0] = items[size - 1];
        items[size - 1] = 0;
        size--;
        heapifyDown();
        return item;
    }

    @Override
    public void add(int item) {
        ensureExtraCapacity();
        items[size] = item;
        size++;
        heapifyUp();
    }

    @Override
    public void heapifyUp() {
        int index = size - 1;
        while (hasParent(index) && parent(index) < items[index]) {
            swap(getParentIndex(index), index);
            index = getParentIndex(index);
        }
    }

    @Override
    public void heapifyDown() {
        int index = 0;
        // start with left child because this is complete binary tree
        // no left child means no right child also
        while (hasLeftChild(index)) {
            int biggerChildIndex = getLeftChildIndex(index);
            if (hasRightChild(index) && rightChild(index) > leftChild(index)) {
                biggerChildIndex = getRightChildIndex(index);
            }

            if (items[index] > items[biggerChildIndex]) {
                break;
            } else {
                swap(index, biggerChildIndex);
            }
            index = biggerChildIndex;
        }
    }
}
