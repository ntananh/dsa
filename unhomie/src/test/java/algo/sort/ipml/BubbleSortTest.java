package algo.sort.ipml;

import org.junit.Before;
import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.assertEquals;

public class BubbleSortTest {

    private BubbleSort bubbleSort;

    @Before
    public void setUp() {
        bubbleSort = new BubbleSort();
    }

    @Test
    public void shouldSortSourceCorrectly() {
        List<Integer> input = Arrays.asList(1, 5, 2, 4, 3, 9, 8, 7, 6);
        List<Integer> expected = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9);
        assertEquals(expected, bubbleSort.sort(input));
    }
}