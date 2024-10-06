#!/usr/bin/env python3

import argparse
import socket
import threading
from src.client_handler import handle_client
from src.analysis_thread import analysis_thread
from src.shared_data import SharedData


def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments with 'listen_port' and 'pattern' attributes.
    """
    parser = argparse.ArgumentParser(description='Multi-Threaded Network Server for Pattern Analysis')
    parser.add_argument('-l', '--listen-port', type=int, required=True, help='Port number to listen on (>1024)')
    parser.add_argument('-p', '--pattern', type=str, required=True, help='Search pattern to analyze')
    args = parser.parse_args()

    if args.listen_port <= 1024:
        parser.error("Listen port must be greater than 1024.")
    return args

def main():
    """
    The main function that starts the server and handles incoming connections.
    """
    args = parse_arguments()
    listen_port = args.listen_port
    pattern = args.pattern

    shared_data = SharedData(pattern)
    output_lock = threading.Lock()
    connection_id_counter = threading.Lock()
    connection_id = [0]  # Mutable integer for connection IDs

    # Start analysis threads
    for _ in range(2):  # Starting two analysis threads as per assignment
        thread = threading.Thread(target=analysis_thread, args=(shared_data, output_lock))
        thread.daemon = True
        thread.start()

    # Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', listen_port))
    server_socket.listen()
    print(f"Server listening on port {listen_port}...")

    try:
        while True:
            conn, addr = server_socket.accept()
            with connection_id_counter:
                connection_id[0] += 1
                cid = connection_id[0]
            print(f"Accepted connection {cid} from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(conn, cid, shared_data))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
