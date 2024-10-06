# Multi-Threaded Network Server for Pattern Analysis

## Overview

This project implements a multi-threaded network server that accepts multiple client connections, processes text data, and analyzes patterns within the data.

## File Structure

- `assignment3.py`: The main script to start the server.
- `client_handler.py`: Handles client connections.
- `analysis_thread.py`: Contains the analysis thread.
- `shared_data.py`: Manages the shared linked list.
- `node.py`: Defines the `Node` class.
- `write_book.py`: Writes received books to files.
- `README.md`: This file.
- `Makefile`: For running the server (optional).

## How to Run the Server

Make sure you have Python 3 installed.

```bash
chmod +x assignment3.py
./assignment3.py -l <listen_port> -p "<search_pattern>"
```
