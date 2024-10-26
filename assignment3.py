#!/usr/bin/env python3

import socket
import threading
import sys
import argparse
import time


class Node:
    """Represents a node in the shared linked list."""

    def __init__(self, line):
        self.line = line
        self.has_pattern = False  # Indicates if the line contains the search pattern
        self.next = None  # Link to the next node in the shared list
        self.book_next = None  # Link to the next node in the same book
        self.next_frequent_search = None  # Link to the next node with the search pattern


class Book:
    """Represents a book received from a client."""

    def __init__(self, title, con_order):
        self.title = title
        self.con_order = con_order
        self.head = None  # Head of the book's linked list
        self.tail = None  # Tail of the book's linked list
        self.search_count = 0  # Count of lines containing the search pattern


class SharedList:
    """Manages the shared linked list across all threads."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.lock = threading.Lock()

    def add_node(self, node):
        """Adds a node to the shared list in a thread-safe manner."""
        with self.lock:
            if not self.head:
                self.head = self.tail = node
            else:
                self.tail.next = node
                self.tail = node
        print(f"Node added: {node.line}")


class BooksList:
    """Manages the list of books received by the server."""

    def __init__(self):
        self.books = []
        self.lock = threading.Lock()

    def add_book(self, book):
        """Adds a book to the books list in a thread-safe manner."""
        with self.lock:
            self.books.append(book)

    def get_books(self):
        """Returns a copy of the books list."""
        with self.lock:
            return list(self.books)


class Server:
    """The main server class that handles incoming connections and analysis."""

    def __init__(self, listen_port, search_pattern):
        self.listen_port = listen_port
        self.search_pattern = search_pattern
        self.shared_list = SharedList()
        self.books_list = BooksList()
        self.connection_counter = 0
        self.analysis_threads = []
        self.output_lock = threading.Lock()
        self.server_socket = None
        self.stop_event = threading.Event()

    def start(self):
        """Starts the server and listens for incoming connections."""
        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set socket options to reuse address
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                      1)
        # Bind to the specified port
        self.server_socket.bind(('0.0.0.0', self.listen_port))
        # Listen for incoming connections
        self.server_socket.listen(5)
        print(f"Server listening on port {self.listen_port}")

        # Start analysis threads
        for _ in range(2):
            t = threading.Thread(target=self.analysis_thread)
            t.daemon = True
            t.start()
            self.analysis_threads.append(t)

        try:
            while not self.stop_event.is_set():
                # Accept new connection
                client_socket, addr = self.server_socket.accept()
                self.connection_counter += 1
                con_order = self.connection_counter
                # Set client socket to non-blocking
                client_socket.setblocking(False)
                # Create a new thread to handle the client
                t = threading.Thread(target=self.client_handler,
                                     args=(client_socket, con_order))
                t.daemon = True
                t.start()
        except KeyboardInterrupt:
            print("Shutting down server.")
            self.stop_event.set()
            self.server_socket.close()

    def client_handler(self, client_socket, con_order):
        """Handles communication with a connected client."""
        line_buffer = ''
        first_line = True
        book_title = ''
        current_book = None
        node_prev = None

        while not self.stop_event.is_set():
            try:
                data = client_socket.recv(1024)
                if data:
                    # Decode data and split into lines
                    data = data.decode('utf-8', errors='ignore')
                    lines = data.split('\n')
                    for i, part in enumerate(lines):
                        if i == 0:
                            line_buffer += part
                        else:
                            line = line_buffer.strip()
                            line_buffer = part
                            if not line:
                                continue
                            # Create a new node
                            node = Node(line)
                            node.has_pattern = self.search_pattern in line
                            self.shared_list.add_node(node)
                            if node_prev:
                                node_prev.next = node
                            node_prev = node
                            if first_line:
                                # First line is the book title
                                book_title = line
                                current_book = Book(book_title, con_order)
                                current_book.head = node
                                current_book.tail = node
                                self.books_list.add_book(current_book)
                                first_line = False
                            else:
                                # Link nodes within the same book
                                current_book.tail.book_next = node
                                current_book.tail = node
                else:
                    # Client has closed the connection
                    print(f"Connection closed {con_order}")
                    break
            except BlockingIOError:
                # No data available, sleep briefly
                time.sleep(0.1)
            except Exception as e:
                print(f"Exception in client_handler: {e}")
                break
        # Write the received book to a file
        if current_book:
            filename = f"book_{con_order:02d}.txt"
            with open(filename, 'w') as f:
                node = current_book.head
                while node:
                    f.write(node.line + '\n')
                    node = node.book_next
        client_socket.close()

    def analysis_thread(self):
        """Performs periodic analysis of the received data."""
        while not self.stop_event.is_set():
            time.sleep(5)  # Configurable interval
            if self.output_lock.acquire(blocking=False):
                try:
                    books = self.books_list.get_books()
                    # Update search counts for each book
                    for book in books:
                        count = 0
                        node = book.head
                        while node:
                            if node.has_pattern:
                                count += 1
                            node = node.book_next
                        book.search_count = count
                    # Sort books by search count
                    books_sorted = sorted(books,
                                          key=lambda b: b.search_count,
                                          reverse=True)
                    # Output the analysis
                    print(
                        f"\nBook titles sorted by the number of lines in which the pattern \"{self.search_pattern}\" appears:"
                    )
                    for i, book in enumerate(books_sorted):
                        print(
                            f"{i+1} --> Book: {book.title}, Pattern: \"{self.search_pattern}\", Frequency: {book.search_count}."
                        )
                    print()
                finally:
                    self.output_lock.release()
            else:
                continue


def main():
    """Main entry point of the program."""
    parser = argparse.ArgumentParser(
        description='Multi-threaded Network Server for Pattern Analysis')
    parser.add_argument('-l',
                        '--listen_port',
                        type=int,
                        required=True,
                        help='Port to listen on')
    parser.add_argument('-p',
                        '--pattern',
                        type=str,
                        required=True,
                        help='Search pattern')
    args = parser.parse_args()

    if args.listen_port <= 1024:
        print("Please use a port number greater than 1024")
        sys.exit(1)

    server = Server(args.listen_port, args.pattern)
    server.start()


if __name__ == '__main__':
    main()
