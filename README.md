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
nc localhost 12345 -q 0 < data/frankenstein.txt
```

To simulate multiple clients, run the command in separate terminals or as background processes.

**Example with Multiple Clients:**

```bash
nc localhost 12345 -q 0 < data/frankenstein.txt &
nc localhost 12345 -q 0 < data/littlewomen.txt &
nc localhost 12345 -q 0 < data/mobydick.txt &
```

### Frequency Analysis:

The server performs frequency analysis every 5 seconds, outputting the frequency of the search pattern in each book.

- **How It Works:**

  - **Counting Lines with the Pattern:** The server counts the number of lines in each book that contain the specified search pattern.
  - **Periodic Output:** Every 5 seconds, one of the analysis threads outputs the books sorted by the frequency of the pattern.
  - **Sorting Books:** Books are sorted in descending order based on the number of lines containing the pattern.

  #### **Pattern Matching Details:**

- **Case-Sensitive Matching:** The search is case-sensitive. The pattern must match the exact casing.
- **Substring Matching:** The pattern can be part of a larger word.

**Examples with the search pattern `"happy"`:**

- **Will match:**
  - `"happy"`
  - `"unhappy"` (contains `"happy"` as a substring)
  - `"happyness"` (contains `"happy"` as a substring)
- **Will NOT match:**

  - `"Happy"` (does not match due to case sensitivity)
  - `"HAPPY"`
  - `"Happily"`

  - **Book 01 ("Alice in Wonderland")**: 5 lines containing "happy"
  - **Book 02 ("Pride and Prejudice")**: 10 lines containing "happy"
  - **Book 03 ("Moby Dick")**: 3 lines containing "happy"

  The output will be:

  ```
  Book titles sorted by the number of lines in which the pattern "happy" appears:
  1 --> Book: Pride and Prejudice, Pattern: "happy", Frequency: 10.
  2 --> Book: Alice in Wonderland, Pattern: "happy", Frequency: 5.
  3 --> Book: Moby Dick, Pattern: "happy", Frequency: 3.
  ```

### Notes:

- Ensure the **first line** of each text file is the **title** of the book.
- The server will create output files named `book_01.txt`, `book_02.txt`, etc., corresponding to each client connection.
- The server outputs analysis results every 5 seconds, displaying the frequency of the search pattern in each book.

### Stopping the Server:

Press `Ctrl + C` in the terminal where the server is running.
