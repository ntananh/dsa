package data.linkedlist;

public class Main {
    public static void main(String[] args) {
        DoublyLinkedList<String> doublyLinkedList = new DoublyLinkedListImpl<>();
        doublyLinkedList.add("Tony");
        doublyLinkedList.add("Huy");
        doublyLinkedList.add("Think");
        doublyLinkedList.add("Tan Anh");
        System.out.println(doublyLinkedList);

        doublyLinkedList.addLast("Last");
        System.out.println(doublyLinkedList);

        doublyLinkedList.removeFirst();
        System.out.println(doublyLinkedList);
    }
}
