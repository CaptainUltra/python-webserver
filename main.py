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
    decodedData = requestData.decode()
    print(decodedData)

    # Parse HTTP headers
    headers = decodedData.split('\r\n')
    filename = headers[0].split()[1]

    # Get the content of the file
    if filename == '/':
        filename = '/index.html'

    try:
        fin = open('htdocs' + filename)
        content = fin.read()
        fin.close()

        httpResponse = 'HTTP/1.0 200 OK\n\n' + content
    except FileNotFoundError:

        httpResponse = 'HTTP/1.0 404 Not Found\n\nRequested file path is not valid.'

    # Send the HTTP response
    clientConnection.sendall(httpResponse.encode())
    clientConnection.close()
