import socket
import sys
import time

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
# server_address = './uds_socket'
server_address = '/tmp/tamedpy/9afffd0f-85f6-4ae1-bdf5-2a7870ec58f9/ctrl_pane.sock'
print >>sys.stderr, 'connecting to %s' % server_address
#
# while(True):
#     try:
#         sock.connect(server_address)
#     except socket.error, msg:
#         # print >>sys.stderr, msg
#         # sys.exit(1)
#         pass
#     else:
#         break

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
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    data = sock.recv(5)
    print >>sys.stderr, 'received "%s"' % data

    if data and data == "START":
        print "sandbox got exec request, starting.."
    else:
        raise Exception("bad message")

    code_exec_duration = 15
    print "going to execute for {} second, busy waiting".format(code_exec_duration)
    time.sleep(code_exec_duration)

    # Send data
    message = "DONE"
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
