import socket
import sys
import os
import time
import datetime

server_address = './uds_socket'

# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the port
print >>sys.stderr, 'starting up on %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()
try:
    print >>sys.stderr, 'connection from', client_address

    data = connection.recv(5)
    print >>sys.stderr, 'received "%s"' % data

    if data and data == "READY":
        print "sandbox is ready, adding to ready queue"
    else:
        raise Exception("bad message")

    exec_req_wait_time = 10
    print "{} secs busy waiting for driver to get a execution request".format(exec_req_wait_time)
    time.sleep(exec_req_wait_time)

    then = datetime.datetime.now()
    print "Got Exec request, requesting sandbox to exec"
    connection.sendall("START")
    print "Sent START"
    data = connection.recv(4)
    print "Got Exec result from sandbox after ", str(datetime.datetime.now() - then)

    if data and data == "DONE":
        print "sandbox execution success"
    else:
        raise Exception("bad message")

finally:
    # Clean up the connection
    print("closing the connection, trigger sandbox cleanup")
    connection.close()
