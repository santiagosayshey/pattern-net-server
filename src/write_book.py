def write_book_to_file(connection_id, shared_data):
    """
    Writes the received book to a file when the connection closes.

    Args:
        connection_id (int): Identifier for the connection (book number).
        shared_data (SharedData): The shared data structure.
    """
    head = shared_data.get_book_head(connection_id)
    if head is None:
        print(f"No data for connection {connection_id}")
        return

    filename = f"book_{connection_id:02d}.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            node = head
            while node:
                f.write(node.line + '\n')
                node = node.book_next
        print(f"Book {connection_id} written to {filename}")
    except Exception as e:
        print(f"Error writing book {connection_id} to file: {e}")
