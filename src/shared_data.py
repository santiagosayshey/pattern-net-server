import threading
from .node import Node

class SharedData:
    """
    Manages the shared data structure accessed by multiple threads.

    Attributes:
        head (Node): Head of the shared linked list.
        tail (Node): Tail of the shared linked list.
        books (dict): Maps connection_id to a dictionary with 'title', 'head', and 'tail' keys.
        pattern (str): The search pattern to look for.
        pattern_counts (dict): Maps connection_id to the count of the pattern in that book.
        lock (threading.Lock): Lock to synchronize access to shared data.
    """
    def __init__(self, pattern):
        self.head = None
        self.tail = None
        self.books = {}  # {connection_id: {'title': str, 'head': Node, 'tail': Node}}
        self.pattern = pattern
        self.pattern_counts = {}  # {connection_id: int}
        self.lock = threading.Lock()

    def add_node(self, node):
        """
        Adds a node to the shared linked list and the corresponding book list.

        Args:
            node (Node): The node to be added.
        """
        with self.lock:
            # Add to the shared linked list
            if self.head is None:
                self.head = node
                self.tail = node
            else:
                self.tail.next = node
                self.tail = node

            # Add to the per-book linked list
            book = self.books.get(node.connection_id)
            if book is None:
                # First node for this book
                book = {'title': node.line.strip(), 'head': node, 'tail': node}
                self.books[node.connection_id] = book
                self.pattern_counts[node.connection_id] = 0  # Initialize pattern count
            else:
                book['tail'].book_next = node
                book['tail'] = node

            # Check for pattern in the line
            if self.pattern in node.line:
                self.pattern_counts[node.connection_id] += 1

    def get_books_sorted_by_pattern_count(self):
        """
        Retrieves a list of books sorted by the frequency of the search pattern.

        Returns:
            list of tuples: Each tuple contains (connection_id, title, pattern_count).
        """
        with self.lock:
            result = []
            for cid, book in self.books.items():
                count = self.pattern_counts.get(cid, 0)
                title = book['title']
                result.append((cid, title, count))
            # Sort by count in descending order
            result.sort(key=lambda x: x[2], reverse=True)
            return result

    def get_book_head(self, connection_id):
        """
        Retrieves the head node of a specific book.

        Args:
            connection_id (int): The identifier of the book.

        Returns:
            Node: The head node of the book's linked list.
        """
        with self.lock:
            book = self.books.get(connection_id)
            if book:
                return book['head']
            else:
                return None
