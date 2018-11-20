import subprocess
import os
import socket
import sys
import time

def runcode():
    with open('stdout.txt', 'wb', 0) as stdout_file, \
        open('stderr.txt', 'wb', 0) as stderr_file :
        completedProc = subprocess.run(
            ["python", "unsafe.py"],
            stdout=stdout_file,
            stderr=stderr_file,
        )
    output = ''
    if completedProc.returncode == 0:
        output = completedProc.stdout
    else:
        output = "Error: {}".format(completedProc.returncode)
        output += str(completedProc.stdout)
    return output


if __name__ == '__main__':
    print(os.listdir("/tmp/py"))

    # app.run(host="0.0.0.0", port=3000)

    # UNIX socket based client
    os.chdir("/tmp/py")

    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = 'ctrl_pane.sock'
    print('connecting to %s' % server_address)

    subprocess.call("ls -lt", shell=True)
    # repeatedly attempts to connect to socket until succeeded
    while(True):
        try:
            sock.connect(server_address)
        except Exception as e:
            print(e)
            time.sleep(1)
        else:
            print("connected!")
            break


    try:
        # Send data
        message = "READY"
        print('sending "%s"' % message)
        sock.sendall(message)

        data = sock.recv(5)
        print('received "%s"' % data)

        if data and data == "START":
            print("sandbox got exec request, starting..")
            runcode()
        else:
            raise Exception("bad message")

        # Send data
        message = "DONE"
        print('sending "%s"' % message)
        sock.sendall(message)

    finally:
        print('closing socket')
        sock.close()
