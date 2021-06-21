import socket

# Define socket host and port
HOST, PORT = '', 8888


def handle_request(client_connection):
    # Get the client request
    request_data = client_connection.recv(1024)
    decoded_data = request_data.decode()
    print(decoded_data)

    # Parse HTTP headers
    headers = decoded_data.split('\r\n')
    filename = headers[0].split()[1]

    # Get the content of the file
    if filename == '/':
        filename = '/index.html'

    try:
        fin = open('htdocs' + filename)
        content = fin.read()
        fin.close()

        http_response = 'HTTP/1.0 200 OK\n\n' + content
    except FileNotFoundError:

        http_response = 'HTTP/1.0 404 Not Found\n\nRequested file path is not valid.'

    # Send the HTTP response
    client_connection.sendall(http_response.encode())


def serve_forever():
    # Create the socket
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)

    # Output that the server is active
    print(f'Serving HTTP on port {PORT}...')
    while True:
        # Wait for client connections
        client_connection, client_address = listen_socket.accept()
        handle_request(client_connection)
        client_connection.close()


if __name__ == '__main__':
    serve_forever()
