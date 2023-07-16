package algo.leetcode.medium;

import java.util.*;

public class __9_347_Top_K_Frequent_Elements {

    /*
     * Idea: Add the array to map<value, frequent>
     * Conduct max heap with priority queue<value, priority-frequent>
     * Poll the max heap <k> times
     */
    public static List<Integer> topKFrequentMaxHeap(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int n : nums) {
            map.put(n, map.getOrDefault(n, 0) + 1);
        }

        PriorityQueue<Map.Entry<Integer, Integer>> maxHeap = new PriorityQueue<>((a, b) -> (b.getValue() - a.getValue()));
        maxHeap.addAll(map.entrySet());

        List<Integer> res = new ArrayList<>();
        while (res.size() < k) {
            Map.Entry<Integer, Integer> entry = maxHeap.poll();
            if (entry != null) res.add(entry.getKey());
        }

        return res;
    }

    /*
     * Idea: Add the array's values to map<value, frequency>
     * Create bucket with frequency is index and value is key
     * e.g:
     * input: [1, 1, 1, 2, 2, 3]
     * index: | 0  |  1  |  2  |  3  | 4  | 5  | 6  |
     * value: | [] | [3] | [2] | [1] | [] | [] | [] |
     */
    @SuppressWarnings("unchecked")
    public static List<Integer> topKFrequentBucketSort(int[] nums, int k) {
        Map<Integer, Integer> frequentMap = new HashMap<>();
        for (int n : nums) frequentMap.put(n, frequentMap.getOrDefault(n, 0) + 1);

        List<Integer>[] bucket = new List[nums.length + 1];
        for (int key : frequentMap.keySet()) {
            int frequency = frequentMap.get(key);
            if (bucket[frequency] == null) {
                bucket[frequency] = new ArrayList<>();
            }
            bucket[frequency].add(key);
        }

        List<Integer> res = new ArrayList<>();
        for (int pos = bucket.length - 1; pos >= 0 && res.size() < k; pos--) {
            if (bucket[pos] != null) {
                res.addAll(bucket[pos]);
            }
        }

        return res;
    }

    public static void main(String[] args) {
        int[] nums = {1, 1, 1, 2, 2, 3};
        int k = 2;
        System.out.println(Arrays.toString(topKFrequentMaxHeap(nums, k).toArray()));
        System.out.println(Arrays.toString(topKFrequentBucketSort(nums, k).toArray()));
    }
}
