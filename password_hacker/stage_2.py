import socket
import sys
import itertools
import string

hostname = sys.argv[1]
port = int(sys.argv[2])
characters = string.ascii_lowercase + string.digits


def unpack_tuple(p):
    un_p = ''
    for i in range(len(p)):
        un_p += p[i]
    return un_p


def generate_password():
    pas_len = 0
    while True:
        pas_len += 1
        for p in itertools.product(
                characters
                , repeat=pas_len
        ):
            p = unpack_tuple(p)
            yield p


def main():
    # for n, p in enumerate(generate_password()):
    #     print(n, p)
    #     if n == 10000:
    #         break
    with socket.socket() as client_sock:
        client_sock.connect((hostname, port))
        password_gen = generate_password()
        for i in range(1000000):
            passw = next(password_gen).encode()
            client_sock.send(passw)
            response = client_sock.recv(1024).decode()
            if response == 'Wrong password!':
                continue
            elif response == 'Connection success!':
                print(passw.decode())
                break
            elif response == 'Too many attempts':
                print(response)


if __name__ == '__main__':
    main()
