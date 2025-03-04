package algo.leetcode.medium;

import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.TreeSet;

public class __38_2349_Design_a_Number_Container_System {
    static class NumberContainersMap {
        private final Map<Integer, Integer> indexToNumbers;
        private final Map<Integer, TreeSet<Integer>> numberToIndices;

        public NumberContainersMap() {
            this.indexToNumbers = new HashMap<>();
            this.numberToIndices = new HashMap<>();
        }

        public void change(int index, int number) {
            if (indexToNumbers.containsKey(index)) {
                int prevNum = indexToNumbers.get(index);
                numberToIndices.get(prevNum).remove(index);
                if (numberToIndices.get(prevNum).isEmpty()) {
                    numberToIndices.remove(prevNum);
                }
            }

            indexToNumbers.put(index, number);
            numberToIndices.putIfAbsent(number, new TreeSet<>());
            numberToIndices.get(number).add(index);
        }

        public int find(int number) {
            if (numberToIndices.containsKey(number)) {
                return numberToIndices.get(number).first();
            }
            return -1;
        }
    }

    static class NumberContainers {
        private final Map<Integer, Integer> indexToNumbers;
        private final Map<Integer, PriorityQueue<Integer>> numberToIndices;

        public NumberContainers() {
            this.indexToNumbers = new HashMap<>();
            this.numberToIndices = new HashMap<>();
        }

        public void change(int index, int number) {
            if (indexToNumbers.containsKey(index)) {
                int oldNumber = indexToNumbers.get(index);
                if (oldNumber == number) return;

                numberToIndices.get(oldNumber).remove(index);
            }

            indexToNumbers.put(index, number);
            numberToIndices.computeIfAbsent(number, k -> new PriorityQueue<>()).offer(index);
        }

        public int find(int number) {
            if (!numberToIndices.containsKey(number)) {
                return -1;
            }

            final PriorityQueue<Integer> heap = numberToIndices.getOrDefault(number, new PriorityQueue<>());
            while (!heap.isEmpty() && number != indexToNumbers.get(heap.peek())) {
                heap.poll();
            }

            return heap.isEmpty() ? -1 : heap.peek();
        }
    }
}
