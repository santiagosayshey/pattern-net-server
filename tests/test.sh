#!/bin/bash

# Usage: ./test_server.sh <server_host> <server_port> <pattern> <num_clients> <delay>
# Example: ./test_server.sh localhost 12345 "happy" 10 0

# Check if the correct number of arguments is provided
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <server_host> <server_port> <pattern> <num_clients> <delay>"
    echo "Example: $0 localhost 12345 \"happy\" 10 0"
    exit 1
fi

SERVER_HOST=$1
SERVER_PORT=$2
PATTERN=$3
NUM_CLIENTS=$4
DELAY=$5

# Start the server in the background
echo "Starting server on $SERVER_HOST:$SERVER_PORT with pattern \"$PATTERN\"..."
./assignment3.py -l $SERVER_PORT -p "$PATTERN" &
SERVER_PID=$!


# Give the server a moment to start
sleep 2

# Array of text files to send (adjust paths as needed)
# Array of text files to send (adjust paths as needed)
TEXT_FILES=(
    "data/book1.txt"
    "data/book2.txt"
    "data/book3.txt"
    "data/book4.txt"
    "data/book5.txt"
    # ill add more later
)


# Ensure there are enough text files
if [ "$NUM_CLIENTS" -gt "${#TEXT_FILES[@]}" ]; then
    echo "Error: Not enough text files for the number of clients requested."
    exit 1
fi

echo "Simulating $NUM_CLIENTS clients..."

# Function to send data using nc
send_data() {
    FILE=$1
    nc $SERVER_HOST $SERVER_PORT -i $DELAY < "$FILE" &
}

# Loop to start multiple clients
for (( i=0; i<$NUM_CLIENTS; i++ ))
do
    FILE=${TEXT_FILES[$i]}
    if [ ! -f "$FILE" ]; then
        echo "Error: File $FILE does not exist."
        continue
    fi
    echo "Client $((i+1)): Sending $FILE"
    send_data "$FILE"
done

# Wait for all background jobs to finish
wait

# Stop the server
echo "Stopping server..."
kill $SERVER_PID

echo "Test completed."
