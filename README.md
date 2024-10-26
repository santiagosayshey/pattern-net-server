# README

## Multi-Threaded Network Server for Pattern Analysis

### Running the Server:

Start the server using the following command:

```bash
python3 assignment3.py -l <port> -p "<pattern>"
```

- `<port>`: The port number to listen on (must be greater than 1024).
- `<pattern>`: The search pattern to analyze in the incoming data.

**Example:**

```bash
python3 assignment3.py -l 12345 -p "happy"
```

### Running Clients:

Use `netcat` to send text files to the server.

```bash
nc localhost <port> -q 0 < <file.txt>
```

- `<port>`: The same port number the server is listening on.
- `<file.txt>`: Path to the text file you want to send.

**Example:**

```bash
nc localhost 12345 -q 0 < book1.txt
```

To simulate multiple clients, run the command in separate terminals or background processes.

**Example with Multiple Clients:**

```bash
nc localhost 12345 -q 0 < book1.txt &
nc localhost 12345 -q 0 < book2.txt &
nc localhost 12345 -q 0 < book3.txt &
```

### Notes:

- Ensure the first line of each text file is the title of the book.
- The server will create output files named `book_01.txt`, `book_02.txt`, etc., corresponding to each client connection.
- The server outputs analysis results every 5 seconds, displaying the frequency of the search pattern in each book.

### Stopping the Server:

Press `Ctrl + C` in the terminal where the server is running.
