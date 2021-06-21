import errno
import os
import signal
import socket

# Define constant configuration variables
SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5


def grim_reaper(signum, frame):
    pid, status = os.wait()

def handle_request(client_connection):
    # Get the client request
    request_data = client_connection.recv(1024)
    decoded_data = request_data.decode()
    print(decoded_data)

    # Print PIDs
    print(
        'Child PID: {pid}. Parent PID {ppid}'.format(
            pid=os.getpid(),
            ppid=os.getppid(),
        )
    )

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
    print('Parent PID (PPID): {pid}\n'.format(pid=os.getpid()))

    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        try:
            # Wait for client connections
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            # Restart accept() if it was interrupted
            if code == errno.EINTR:
                continue
            else:
                raise

        pid = os.fork()  # Returns 0 in the child and the child's process id in the parent.
        if pid == 0:  # child
            listen_socket.close()  # Close child's duplicate of the socket as it's not needed.
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)  # Child exit
        else:  # parent
            client_connection.close()  # Close parent process


if __name__ == '__main__':
    serve_forever()
