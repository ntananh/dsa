package linkedlist;

import org.junit.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DoublyLinkedListImplTest {

    @Test
    public void add() {
        DoublyLinkedList<String> doublyLinkedList = new DoublyLinkedListImpl<>();
        doublyLinkedList.add("Tony");
        doublyLinkedList.add("Huy");
        doublyLinkedList.add("Think");
        doublyLinkedList.add("Tan Anh");
        assertEquals("[Tony,Huy,Think,Tan Anh]", doublyLinkedList.toString());
    }

    @Test
    public void removeNode() {
        DoublyLinkedList<String> doublyLinkedList = new DoublyLinkedListImpl<>();
        doublyLinkedList.add("Tony");
        doublyLinkedList.add("Huy");
        doublyLinkedList.add("Think");
        doublyLinkedList.add("Tan Anh");

        boolean isRemoved = doublyLinkedList.remove("Huy");
        assertTrue(isRemoved);
    }
}