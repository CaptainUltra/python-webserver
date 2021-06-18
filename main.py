import socket

# Define socket host and port
HOST, PORT = '', 8888

# Create the socket
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((HOST, PORT))
listenSocket.listen(1)

# Output that the server is active
print(f'Serving HTTP on port {PORT}...')
while True:
    # Wait for client connections
    clientConnection, clientAddress = listenSocket.accept()

    # Get the client request
    requestData = clientConnection.recv(1024)
    decodedData = requestData.decode('utf-8')
    print(decodedData)

    # Prepare and send the response
    httpResponse = b"""\
    HTTP/1.1 200 OK

    Hello, World!
    """

    clientConnection.sendall(httpResponse)
    clientConnection.close()
