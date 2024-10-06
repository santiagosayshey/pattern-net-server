**Plan for Assignment 3: Multi-Threaded Network Server for Pattern Analysis in Python**

---

### **Overview**

The goal is to develop a high-performance multi-threaded network server in Python that:

1. Accepts multiple simultaneous connections.
2. Reads data from clients non-blockingly and stores it in a shared data structure.
3. Manages a shared linked list with multiple links per node.
4. Keeps track of each book's data separately.
5. Implements analysis threads that search for a specific pattern within the data.
6. Periodically outputs analysis results to the console.

---

### **File Structure**

- **`assignment3.py`**: The main Python script containing the server code.
- **`README.md`**: Instructions on how to run the server and any additional details.

---

### **Command-Line Arguments**

The server should be started with:

```bash
./assignment3.py -l 12345 -p "happy"
```

- `-l` or `--listen-port`: Port number to listen on (e.g., `12345`).
- `-p` or `--pattern`: The search pattern to analyze (e.g., `"happy"`).
- `-i` or `--interval`: (Optional) Interval in seconds for analysis output (default is 5 seconds).

---

### **Key Components**

1. **Main Function (`main`)**

   - Parses command-line arguments.
   - Initializes the server socket.
   - Starts listener for incoming connections.
   - Manages the acceptance of new connections and the creation of client handler threads.
   - Starts analysis threads.

2. **Client Handler (`handle_client`)**

   - Handles communication with a connected client.
   - Reads data non-blockingly and processes lines.
   - Updates the shared data structure with new nodes.
   - Writes the received book to a file when the connection closes.

3. **Shared Data Structure (`SharedData`)**

   - Manages the shared linked list accessed by multiple threads.
   - Ensures thread-safe operations using locks.
   - Stores the main list, per-book lists, and pattern occurrence data.

4. **Node Class (`Node`)**

   - Represents a node in the shared linked list.
   - Contains multiple pointers (`next`, `book_next`, `next_frequent_search`).
   - Stores the line of text and associated metadata.

5. **Analysis Thread (`analysis_thread`)**

   - Periodically analyzes the shared data.
   - Computes the frequency of the search pattern in each book.
   - Outputs the sorted list of book titles based on pattern frequency.
   - Ensures only one thread outputs during each interval.

6. **Synchronization Mechanisms**
   - Uses threading locks to prevent race conditions.
   - Manages access to shared resources among multiple threads.

---

### **Detailed Component Plan**

#### **1. Main Function (`main`)**

```python
def main():
    """
    The main entry point of the server application.

    - Parses command-line arguments.
    - Initializes the server socket and binds to the specified port.
    - Starts threads for handling incoming client connections.
    - Starts analysis threads for pattern analysis.
    - Handles graceful shutdown of the server.
    """
```

- **Steps:**
  - Use `argparse` to parse command-line arguments.
  - Initialize a `SharedData` instance with the search pattern.
  - Create a server socket and bind it to the specified listen port.
  - Listen for incoming connections.
  - For each new connection:
    - Increment a global `connection_id` counter.
    - Start a new thread (`handle_client`) with the client socket.
  - Start multiple analysis threads (`analysis_thread`).
  - Keep the main thread alive to accept new connections or handle signals.

#### **2. Command-Line Argument Parser (`parse_arguments`)**

```python
def parse_arguments():
    """
    Parses the command-line arguments provided to the script.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
```

- **Arguments:**
  - `-l`, `--listen-port` (int): The port number to listen on.
  - `-p`, `--pattern` (str): The search pattern to analyze.
  - `-i`, `--interval` (int, optional): The analysis interval in seconds (default: 5).

#### **3. Client Handler Function (`handle_client`)**

```python
def handle_client(conn, addr, connection_id, shared_data):
    """
    Handles client communication in a separate thread.

    Args:
        conn (socket.socket): The client socket object.
        addr (tuple): The client address.
        connection_id (int): The unique identifier for the connection/book.
        shared_data (SharedData): The shared data structure instance.
    """
```

- **Responsibilities:**
  - Set the client socket to non-blocking mode.
  - Initialize a buffer to accumulate data.
  - Loop to read data from the client:
    - Handle `BlockingIOError` exceptions when no data is available.
    - Append received data to the buffer.
    - Split the buffer into complete lines.
    - Create `Node` instances for each complete line.
    - Update the shared data structure with new nodes.
    - Print a log message for each added node.
  - Detect when the client closes the connection.
  - Call `write_book_to_file` to save the received book.
  - Close the client socket.

#### **4. Node Class (`Node`)**

```python
class Node:
    """
    Represents a node in the shared linked list.

    Attributes:
        line (str): The line of text read from the client.
        connection_id (int): The identifier for the connection/book.
        next (Node): Pointer to the next node in the shared list.
        book_next (Node): Pointer to the next node in the same book.
        next_frequent_search (Node): Pointer to the next node containing the search pattern.
    """

    def __init__(self, line, connection_id):
        # Initialize node attributes
        pass
```

- **Attributes:**
  - `line`: The text content of the node.
  - `connection_id`: Used to associate the node with a specific book.
  - `next`: Link to the next node in the shared list.
  - `book_next`: Link to the next node in the same book.
  - `next_frequent_search`: Link to the next node containing the search pattern.

#### **5. Shared Data Structure (`SharedData` Class)**

```python
class SharedData:
    """
    Manages the shared data structure accessed by multiple threads.

    Attributes:
        head (Node): Head of the shared linked list.
        tail (Node): Tail of the shared linked list.
        books (dict): Maps connection_id to book data (title, head, tail).
        pattern (str): The search pattern to analyze.
        pattern_counts (dict): Counts of pattern occurrences per book.
        lock (threading.Lock): Lock to synchronize access to shared data.
    """

    def __init__(self, pattern):
        # Initialize shared data attributes
        pass

    def add_node(self, node):
        """
        Adds a node to the shared linked list and the corresponding book list.

        Args:
            node (Node): The node to be added.
        """
        pass

    def get_books_sorted_by_pattern_count(self):
        """
        Retrieves a list of books sorted by the frequency of the search pattern.

        Returns:
            list of tuples: Each tuple contains (connection_id, title, pattern_count).
        """
        pass
```

- **Methods:**
  - `add_node(node)`: Adds a node to the shared list and updates per-book lists.
    - Updates `head` and `tail` for the shared list.
    - Updates `book_head` and `book_tail` for the specific book.
    - Increments pattern count if the line contains the search pattern.
  - `get_books_sorted_by_pattern_count()`: Returns books sorted by pattern frequency.

#### **6. Write Book to File (`write_book_to_file`)**

```python
def write_book_to_file(connection_id, shared_data):
    """
    Writes the contents of a book to a file when the client connection closes.

    Args:
        connection_id (int): The identifier of the book.
        shared_data (SharedData): The shared data structure instance.
    """
```

- **Steps:**
  - Retrieve the head node of the book's linked list.
  - Open a file named `book_xx.txt`, where `xx` is the zero-padded connection ID.
  - Traverse the book's linked list using `book_next` and write each line to the file.

#### **7. Analysis Thread Function (`analysis_thread`)**

```python
def analysis_thread(shared_data, interval, output_lock):
    """
    Performs periodic analysis of the shared data and outputs results.

    Args:
        shared_data (SharedData): The shared data structure instance.
        interval (int): The interval in seconds between analyses.
        output_lock (threading.Lock): Lock to ensure only one thread outputs at a time.
    """
```

- **Responsibilities:**
  - Run an infinite loop with sleep intervals.
  - Attempt to acquire the `output_lock` non-blockingly.
    - If acquired:
      - Retrieve and sort the books by pattern frequency.
      - Output the sorted list of book titles and counts to the console.
      - Release the `output_lock`.
    - If not acquired:
      - Skip outputting in this interval.

#### **8. Synchronization Mechanisms**

- **Shared Data Lock (`shared_data.lock`):**

  - Protects access to the shared data structure during modifications.
  - Ensures that adding nodes and updating counts are thread-safe.

- **Output Lock (`output_lock`):**
  - Ensures that only one analysis thread outputs results during each interval.
  - Prevents interleaved outputs from multiple threads.

#### **9. Non-Blocking I/O Handling**

- **Client Socket:**

  - Set to non-blocking mode using `conn.setblocking(False)`.
  - Reads data using `conn.recv()`.
  - Handles `BlockingIOError` exceptions when no data is available.

- **Data Buffering:**
  - Maintains a per-connection buffer to accumulate incoming data.
  - Splits buffer content into lines based on newline characters.
  - Handles partial lines by retaining incomplete data in the buffer.

#### **10. Logging and Output**

- **Node Addition Logging:**

  - Each time a node is added to the shared list, print a message:
    ```
    "Added node from connection {connection_id}: {line_content}"
    ```

- **Analysis Output:**
  - Periodically outputs the sorted list of book titles and pattern frequencies:
    ```
    "Analysis Results at {timestamp}:
    1. '{book_title_1}' - {count_1} occurrences
    2. '{book_title_2}' - {count_2} occurrences
    ...
    "
    ```

---

### **Testing Plan**

1. **Initial Testing:**

   - Test with a single client connection.
   - Use `nc` (netcat) to send a small text file to the server.
   - Verify that the book is saved correctly and nodes are added to the shared list.

2. **Concurrent Connections:**

   - Simulate multiple clients (at least 10) sending data simultaneously.
   - Ensure that the server handles all connections without errors.
   - Check for correct logging and book file outputs.

3. **Pattern Analysis:**

   - Use text files containing known occurrences of the search pattern.
   - Verify that the analysis threads correctly count pattern occurrences.
   - Check that the analysis output is accurate and sorted correctly.

4. **Thread Safety:**

   - Use tools or modules (e.g., `threading` module debug features) to detect race conditions.
   - Review code to ensure all shared resources are properly synchronized.

5. **Performance Testing:**
   - Measure the server's responsiveness under high load.
   - Check CPU and memory usage to ensure scalability.

---

### **Example Function and Class Definitions with Docstrings**

#### **`parse_arguments` Function**

```python
def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments with 'listen_port', 'pattern', and 'interval' attributes.
    """
    # Implementation using argparse
    pass
```

#### **`Node` Class**

```python
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
```

#### **`SharedData` Class**

```python
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
        self.books = {}
        self.pattern = pattern
        self.pattern_counts = {}
        self.lock = threading.Lock()
```

#### **`handle_client` Function**

```python
def handle_client(conn, addr, connection_id, shared_data):
    """
    Handles client communication in a separate thread.

    Args:
        conn (socket.socket): The client socket.
        addr (tuple): The client address.
        connection_id (int): Identifier for the connection (book number).
        shared_data (SharedData): The shared data structure.
    """
    # Set socket to non-blocking mode
    # Initialize buffer for accumulating data
    # Loop to read data and process lines
    # Handle client disconnection
    pass
```

#### **`analysis_thread` Function**

```python
def analysis_thread(shared_data, interval, output_lock):
    """
    Periodically analyzes the shared data and outputs book titles sorted by pattern frequency.

    Args:
        shared_data (SharedData): The shared data structure.
        interval (int): The interval in seconds between analyses.
        output_lock (threading.Lock): Lock to ensure single-threaded output.
    """
    # Infinite loop with sleep(interval)
    # Attempt to acquire output_lock
    # If acquired, perform analysis and output results
    # Release output_lock
    pass
```

#### **`write_book_to_file` Function**

```python
def write_book_to_file(connection_id, shared_data):
    """
    Writes the received book to a file when the connection closes.

    Args:
        connection_id (int): Identifier for the connection (book number).
        shared_data (SharedData): The shared data structure.
    """
    # Retrieve the book's head node
    # Open the file with the appropriate name
    # Traverse the book's linked list and write lines to the file
    pass
```

#### **`main` Function**

```python
def main():
    """
    The main function that starts the server and handles incoming connections.
    """
    # Parse arguments
    # Initialize shared data and output lock
    # Set up server socket
    # Accept connections in a loop
    # Start analysis threads
    # Handle graceful shutdown
    pass
```

---

### **Additional Notes**

- **Thread Lifecycle Management:**

  - Ensure that threads are properly terminated when the server shuts down.
  - Use daemon threads or implement a shutdown mechanism.

- **Exception Handling:**

  - Handle possible exceptions, such as socket errors or interrupted system calls.
  - Ensure that the server remains robust under unexpected conditions.

- **Performance Considerations:**

  - Avoid holding locks longer than necessary to reduce contention.
  - Use efficient data structures and algorithms for analysis.

- **Code Documentation:**
  - Include docstrings and comments for all functions and classes.
  - Provide clear explanations of logic and reasoning.

---

### **README Content**

- **How to Run the Server:**

  ```bash
  python3 assignment3.py -l <listen_port> -p "<search_pattern>" [-i <interval>]
  ```

  Example:

  ```bash
  python3 assignment3.py -l 12345 -p "happy" -i 5
  ```

- **Dependencies:**

  - Python 3.x
  - Standard Python libraries (`socket`, `threading`, `argparse`, etc.)

- **How to Send Data to the Server:**

  ```bash
  nc localhost 12345 -i <delay> < file.txt
  ```

  - Replace `<delay>` with the desired delay between packets (e.g., `1` for 1 second).
  - Replace `file.txt` with the path to your text file.

- **Testing with Multiple Clients:**

  - Open multiple terminal windows or use background processes to start several `nc` clients simultaneously.

- **Expected Outputs:**
  - Log messages for each node added to the shared list.
  - Periodic analysis outputs showing books sorted by pattern occurrence.

---

This comprehensive plan outlines the structure and functionality required to successfully complete the assignment using Python. By following this plan, you will implement a multi-threaded network server that meets all specified requirements and is robust, scalable, and maintainable.
