import datetime
import docker
import errno
import json
import os
import socket
import threading
import time

from uuid import uuid4

from result import Result

client = docker.from_env()

WORKSPACE_DIR = "/tmp/tamedpy"
try:
    os.makedirs(WORKSPACE_DIR)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


# one Worker instance per containerized execution
# owns details about execution artifacts and status
class Worker(object):
    def __init__(self, parent_driver, port):
        self.parent_driver = parent_driver
        self.id = uuid4()
        self.execd_path = None
        self._status = 0
        self.port = port
        self.container = None
        self.sock = None
        self.connection = None

    def status(self):
        return self._status

    def turnup(self):
        # launch worker, check "ready", change status
        print("new worker {} coming up".format(self.id))

        execd_path = os.path.join(WORKSPACE_DIR, str(self.id))
        try:
            os.makedirs(execd_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        self.execd_path = execd_path

        # volume params
        mnt_pnt = "/tmp/py"
        volume_params = {execd_path: {"bind": mnt_pnt, "mode": "rw"}}
        port_params = {'6110/tcp': ('127.0.0.1', self.port)}
        print("Worker {}, port_params: {}".format(self.id, port_params))
        seccomp_policy = ""
        with open("policy.json") as f:
            seccomp_policy = f.read()
        seccomp_policy_json = json.dumps(json.loads(seccomp_policy))
        # print(seccomp_policy_json)
        try:
            self.container = client.containers.run(
                "tamedpy",
                volumes=volume_params,
                ports=port_params,
                detach=True,
                # security_opt=["seccomp={}".format(seccomp_policy_json)]
            )
            print(self.container)
        except docker.errors.APIError as e:
            # FIXME: ask for specific error codes / eg when port is already allocated, take specific remedial action
            print(e)
            exit(-1)

        # start socket connection
        self.hello_socket()
        assert(self._status == 1)
        return


    def hello_socket(self):
        server_address = 'localhost'
        while(True):
            try:
                sock = socket.create_connection((server_address, self.port))
                message = "HELLO"
                # print('sending "%s"' % message)
                sock.sendall(message)

                data = sock.recv(5)
                # print('received "%s"' % data)

                if data.strip() == b'':
                    time.sleep(0.1)
                    continue
                if data and data.strip() == b'READY':
                    print("sandbox is READY")
                else:
                    raise Exception("bad message")
            except Exception as e:
                print(e)
                time.sleep(1)
            else:
                # print("connected! and ready")
                self._status = 1
                break
            finally:
                # print('closing socket')
                sock.close()
        return

    def exec_code_socket(self):
        server_address = 'localhost'
        while(True):
            try:
                sock = socket.create_connection((server_address, self.port))
                then = datetime.datetime.now()
                message = b'START'
                # print('sending "%s"' % message)
                sock.sendall(message)

                data = sock.recv(4)
                # print('received "%s"' % data)

                if data.strip() == b'':
                    print("ERROR: shouldn't be getting blank from server now")
                    time.sleep(0.1)
                    continue
                if data and data.strip() == b'DONE':
                    pass
                    # print "Got Exec result from sandbox after ", str(datetime.datetime.now() - then)
                    # print "sandbox execution success"
                else:
                    raise Exception("bad message")
            except Exception as e:
                print(e)
                time.sleep(1)
            else:
                # print("connected! and ready")
                self._status = 2
                break
            finally:
                # print("closing the connection, trigger sandbox cleanup")
                sock.close()

        WorkerCleanupThread(self).start()
        return

    def turndown(self):
        print("worker {} turndown intiated".format(self.id))
        self.container.stop(timeout=0)

    def get_exec_dir_path(self):
        return self.execd_path

    def put(self, source):
        assert(os.path.isfile(source))
        filename = os.path.basename(source)
        ofpath = os.path.join(self.execd_path, filename)
        try:
            with open(source, "rb") as f:
                with open(ofpath, "wb") as of:
                    shutil.copyfileobj(f, of)
        except Exception as e:
            print(e)
        print(ofpath)
        return ofpath

    def execute(self, code):
        code_file_path = os.path.join(self.execd_path, "unsafe.py")
        with open(code_file_path, "w") as f:
            f.write(code)
        self.exec_code_socket()

        result = Result(self.execd_path, self.id)
        return result

    def on_container_finished(self):
        print("worker {} cleaning up".format(self.id))
        # do cleanup stuff
        self._status = 2
        print("worker {} exiting".format(self.id))
        self.parent_driver.on_worker_exiting(self)
        print("worker {} exited".format(self.id))



class WorkerCleanupThread(threading.Thread):
    def __init__(self, worker):
        threading.Thread.__init__(self)
        self.worker = worker

    def run(self):
        then = datetime.datetime.now()
        self.worker.container.stop(timeout=0)
        print("took {} for container.stop()".format(datetime.datetime.now() - then))
        self.worker.on_container_finished()
