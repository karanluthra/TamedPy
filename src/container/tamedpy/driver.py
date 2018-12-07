import subprocess
import os
import socket
import sys
import time

def runcode():
    try:
        with open('stdout.txt', 'wb', 0) as stdout_file, \
            open('stderr.txt', 'wb', 0) as stderr_file :
            completedProc = subprocess.run(
                ["python", "unsafe.py"],
                stdout=stdout_file,
                stderr=stderr_file,
                # TODO: parameterize timeout
                timeout=10
            )
    except subprocess.TimeoutExpired as e:
        with open('stderr.txt', 'a') as stderr_file:
            stderr_file.write(str(e))
        return

    output = ''
    if completedProc.returncode == 0:
        output = completedProc.stdout
    else:
        output = "Error: {}".format(completedProc.returncode)
        output += str(completedProc.stdout)
    return output


if __name__ == '__main__':
    print(os.listdir("/tmp/py"))
    os.chdir("/tmp/py")


    server_address = "0.0.0.0"
    port = 6110
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    print('starting up on %s' % server_address)
    sock.bind((server_address, port))

    # Listen for incoming connections
    sock.listen(5)
    while(True):
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from' + str(client_address))

            data = connection.recv(5)
            print('received "%s"' % data)

            # respond to HELLO
            if data and data.strip() == b'HELLO':
                print("host says hello")
                message = b'READY'
                print('sending "%s"' % message)
                connection.sendall(message)
            # respond to START
            elif data and data.strip() == b'START':
                print("host says start")
                ##### DO CODE EXEC HERE ######
                runcode()
                message = b'DONE'
                print('sending "%s"' % message)
                connection.sendall(message)
            else:
                raise Exception("bad message")
        except Exception as e:
            print(e)
            exit(1)
        finally:
            connection.close()
    print("normal exit")
