import socket
from .node import Node
from .write_book import write_book_to_file


def handle_client(conn, connection_id, shared_data):
    """
    Handles client communication in a separate thread.

    Args:
        conn (socket.socket): The client socket.
        connection_id (int): Identifier for the connection (book number).
        shared_data (SharedData): The shared data structure.
    """
    conn.setblocking(False)
    buffer = ''
    try:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    # Client has closed the connection
                    break
                buffer += data.decode('utf-8')
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    node = Node(line, connection_id)
                    shared_data.add_node(node)
                    print(f"Added node from connection {connection_id}: {line}")
            except BlockingIOError:
                continue
    except Exception as e:
        print(f"Error handling client {connection_id}: {e}")
    finally:
        conn.close()
        print(f"Connection {connection_id} closed.")
        write_book_to_file(connection_id, shared_data)
