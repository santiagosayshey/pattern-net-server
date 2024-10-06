class Node:
    """
    Represents a node in the shared linked list.

    Attributes:
        line (str): The line of text read from a client.
        connection_id (int): Identifier for the connection (book number).
        next (Node): Pointer to the next element in the shared list.
        book_next (Node): Pointer to the next item in the same book.
        next_frequent_search (Node): Pointer to the next item containing the search pattern.
    """
    def __init__(self, line, connection_id):
        self.line = line
        self.connection_id = connection_id
        self.next = None
        self.book_next = None
        self.next_frequent_search = None
