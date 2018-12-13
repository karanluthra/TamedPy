import datetime
import docker
import errno
import json
import logging
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

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(1)


'''
one Worker instance per containerized execution
owns details about execution artifacts and status
'''
class Worker(object):
    def __init__(self, parent_driver, port):
        # know thy parent to be able to call cleanup methods
        self.parent_driver = parent_driver
        self.id = uuid4()
        # path to execution directory
        self.execd_path = None
        # 0 : init, 1 : ready 2: finished
        self._status = 0
        # each worker needs a port unique in the group of worker
        self.port = port
        # ref to container object from Docker API
        self.container = None
        # FIXME: remove sock, connection
        self.sock = None
        self.connection = None

    def status(self):
        return self._status

    '''
    launch worker, check "ready", change status
    '''
    def turnup(self):
        logger.info("new worker {} coming up".format(self.id))

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

        # port port_params
        port_params = {'6110/tcp': ('127.0.0.1', self.port)}
        logger.info("Worker {}, port_params: {}".format(self.id, port_params))

        # network params
        # docker network create --internal no-internet
        # 954c36c7b483b7d7f8618d904b5bb6f4edb6e3ef9324c8d11fb4ee4590fbe0ce
        # network="no-internet"
        # FIXME: socket networking bw host and docker doesn't work with this custom nw

        # security params
        # FIXME: take path to seccomp policy as an argument to Driver and Worker
        # with open("policy.json") as f:
        #     seccomp_policy = f.read()
        # seccomp_policy_json = json.dumps(json.loads(seccomp_policy))

        try:
            self.container = client.containers.run(
                "tamedpy",
                volumes=volume_params,
                ports=port_params,
                # network=network,
                detach=True,
                # security_opt=["seccomp={}".format(seccomp_policy_json)]
            )
            logger.info("Worker {} started container {}".format(self.id, self.container))
        except docker.errors.APIError as e:
            # FIXME: ask for specific error codes / eg when port is already
            # allocated, take specific remedial action
            raise
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
                logger.info('sending "%s"' % message)
                sock.sendall(message)

                data = sock.recv(5)
                logger.info('received "%s"' % data)

                if data.strip() == b'':
                    time.sleep(0.1)
                    continue
                if data and data.strip() == b'READY':
                    logger.info("sandbox is READY")
                else:
                    raise Exception("bad message")
            except Exception as e:
                print(e)
                time.sleep(1)
            else:
                logger.info("connected! and ready")
                self._status = 1
                break
            finally:
                logger.info('closing socket')
                sock.close()
        return

    def exec_code_socket(self):
        server_address = 'localhost'
        while(True):
            try:
                sock = socket.create_connection((server_address, self.port))
                then = datetime.datetime.now()
                message = b'START'
                logger.info('sending "%s"' % message)
                sock.sendall(message)

                data = sock.recv(4)
                logger.info('received "%s"' % data)

                if data.strip() == b'':
                    logger.error("Shouldn't be getting blank from server now")
                    time.sleep(0.1)
                    continue
                if data and data.strip() == b'DONE':
                    logger.info("Got Exec result from sandbox after {}".format(
                            str(datetime.datetime.now() - then)
                        )
                    )
                else:
                    raise Exception("bad message")
            except Exception as e:
                print(e)
                time.sleep(1)
            else:
                logger.info("connected! and ready")
                self._status = 2
                break
            finally:
                logger.info("closing the connection, trigger sandbox cleanup")
                sock.close()

        WorkerCleanupThread(self).start()
        return

    def turndown(self):
        logger.info("worker {} turndown intiated".format(self.id))
        self.container.stop(timeout=0)
        # TODO: self.container.remove() too

    def get_exec_dir_path(self):
        return self.execd_path

    '''
    copies file at source into worker's exec directory
    '''
    def put(self, source):
        assert(os.path.isfile(source))
        filename = os.path.basename(source)
        ofpath = os.path.join(self.execd_path, filename)
        try:
            with open(source, "rb") as f:
                with open(ofpath, "wb") as of:
                    shutil.copyfileobj(f, of)
        except Exception as e:
            # FIXME: catch specific exceptions and act, else raise
            print(e)
        logger.info("file copied into exec directory at {}".format(ofpath))
        return ofpath

    '''
    places source code passed in code into exec directory and
    triggers container to execute the code
    waits for container to complete and returns Result object
    '''
    def execute(self, code):
        code_file_path = os.path.join(self.execd_path, "unsafe.py")
        with open(code_file_path, "w") as f:
            f.write(code)
        self.exec_code_socket()

        result = Result(self.execd_path, self.id)
        return result

    '''
    handle all tasks to be done once the container stops
    called in WorkerCleanupThread context
    '''
    def on_container_finished(self):
        self._status = 2
        logger.info("worker {} cleaning up".format(self.id))
        self.parent_driver.on_worker_exiting(self)
        logger.info("worker {} exiting".format(self.id))


'''
Separate thread to operate on a single worker for cleanup tasks
Handles stopping the container, triggering cleanup functions and
trigering worker replacement in Driver
'''
class WorkerCleanupThread(threading.Thread):
    def __init__(self, worker):
        threading.Thread.__init__(self)
        self.worker = worker

    def run(self):
        self.worker.container.stop(timeout=0)
        self.worker.on_container_finished()
        # TODO: self.container.remove() too
