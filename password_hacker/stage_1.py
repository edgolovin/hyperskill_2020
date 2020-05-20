import socket
import sys

hostname = sys.argv[1]
port = int(sys.argv[2])

with socket.socket() as client_sock:
    address = (hostname, port)

    client_sock.connect(address)

    data = sys.argv[3].encode()

    client_sock.send(data)

    response = client_sock.recv(1024)
    response = response.decode()
    print(response)
