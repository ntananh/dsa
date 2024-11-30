package algo.leetcode.medium;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class __26_981_Time_Based_Key_Value_Store {

	/**
	 * <p>
	 * Design a <b>time-based</b> key-value data structure that can store multiple values for
	 * <i>the same key</i> at the different time stamps and retrieve the key's value at a certain
	 * timestamp
	 * </p>
	 *
	 * <ul><b>Constraints: </b>
	 *    <li>{@code 1 <= key.length }, {@code value.length <= 100 }</li>
	 *    <li>{@code key} and {@code value } consist of lowercase English letters and digits.</li>
	 *    <li>{@code 1 <= timestamp <= 10}<sup>7</sup></li>
	 *    <li>All the timestamps {@code timestamp } of set are strictly increasing.</li>
	 *    <li>At most {@code 2 * 10}<sup>5</sup> calls will be made to {@code set } and {@code get }.</li>
	 * </ul>
	 */
	static class TimeMap {

		static class Pair<K, V> {
			private final K key;
			private final V value;

			public Pair(K first, V second) {
				this.key = first;
				this.value = second;
			}

			public K getKey() {
				return key;
			}

			public V getValue() {
				return value;
			}
		}

		private final Map<String, List<Pair<Integer, String>>> map = new HashMap<>();

		public TimeMap() {
		}

		/**
		 * Store the {@code key} with the value {@code value} at the given time {@code timestamp}
		 *
		 * @param key       the key
		 * @param value     value to store
		 * @param timestamp timestamp
		 */
		public void set(String key, String value, int timestamp) {
			map.computeIfAbsent(key, k -> new ArrayList<>()).add(new Pair<>(timestamp, value));
		}

		/**
		 * <p>
		 * Returns a value such that {@link TimeMap#set} was called previously,
		 * with {@code timestamp_prev} <= {@code timestamp}.
		 * </p>
		 *
		 * <ul>
		 *      <li> The are <i>multiple values</i>, returns the value associated with the <b>largest</b>  {@code timestamp_prev} </li>
		 *      <li> there are <i>no values</i>, it return {@code ""} </li>
		 * </ul>
		 *
		 * @param key       the key
		 * @param timestamp timestamp to get value
		 * @return the value such that {@link TimeMap#set} was called previously.
		 */
		public String get(String key, int timestamp) {
			List<Pair<Integer, String>> records = map.getOrDefault(key, new ArrayList<>());

			int l = 0, r = records.size() - 1;
			String res = "";
			while (l <= r) {
				int mid = l + (r - l) / 2;
				if (records.get(mid).getKey() <= timestamp) {
					res = records.get(mid).getValue();
					l = mid + 1;
				} else {
					r = mid - 1;
				}
			}
			return res;
		}
	}
}
