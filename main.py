import socket

HOST, PORT = '', 8888

listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((HOST, PORT))
listenSocket.listen(1)

# Output that the server is active
print(f'Serving HTTP on port {PORT}...')
while True:
    clientConnection, clientAddress = listenSocket.accept()
    requestData = clientConnection.recv(1024)
    print(requestData.decode('utf-8'))

    httpResponse = b"""\
    HTTP/1.1 200 OK

    Hello, World!
    """

    clientConnection.sendall(httpResponse)
    clientConnection.close()
