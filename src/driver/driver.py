from uuid import uuid4
import os
import errno
import subprocess
import requests
import time
import threading
import docker
import shutil
import socket
import sys
import datetime

client = docker.from_env()

WORKSPACE_DIR = "/tmp/tamedpy"
try:
    os.makedirs(WORKSPACE_DIR)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


# the daemon part - manages the pool of workers and assigns tasks
# provides interface to interact with execution
class Driver(object):
    def __init__(self):
        self.num_workers = 1
        self.worker_queue = []
        self.turndown_in_progress = False

    def __del__(self):
        print("driver exiting..")
        if self.worker_queue:
            self.turndown()

    def execute(self, source_code, input_file_paths=[]):
        # find a ready worker, and execute the source code
        worker = self.grab_ready_worker()
        for input_file_path in input_file_paths:
            worker.put(input_file_path)
        return worker.execute(source_code)

    def turnup_one_new_worker(self):
        new_worker = Worker(self)
        # synch step, long, IO bound
        new_worker.turnup()
        assert new_worker.status() == 1
        self.worker_queue.append(new_worker)

    def turnup(self):
        # initiate workers to fill up the worker queue
        for i in range(self.num_workers):
            self.turnup_one_new_worker()

    def turndown(self):
        print("driver turndown initiated")
        self.turndown_in_progress = True
        for worker in self.worker_queue:
            worker.turndown()

    def grab_ready_worker(self):
        ready_worker = None
        for i in range(len(self.worker_queue)):
            if self.worker_queue[i].status() == 1:
                ready_worker = self.worker_queue[i]
                break
        if not ready_worker:
            assert False, "out of workers"
        return ready_worker

    def on_worker_exiting(self, worker):
        assert(worker.status() == 2)
        self.worker_queue.remove(worker)
        if not self.turndown_in_progress:
            self.turnup_one_new_worker()


class ContainerThread(threading.Thread):
    def __init__(self, parent_worker, container_id):
      threading.Thread.__init__(self)
      self.container_id = container_id
      self.parent_worker = parent_worker

    def run(self):
      print "Starting " + self.name
      container = client.containers.get(self.container_id)
      print "Waiting on: " + container.short_id
      container.wait()
      print "Container stopped: " + container.short_id
      print "Cleaning up started: " + container.short_id
      # DEBUG: commenting out remove for debugging postmortems
      # container.remove()
      self.parent_worker.on_container_finished()
      print "Exiting " + self.name

# one Worker instance per containerized execution
# owns details about execution artifacts and status
class Worker(object):
    def __init__(self, parent_driver):
        self.parent_driver = parent_driver
        self.id = uuid4()
        self.execd_path = None
        self._status = 0
        self.port = None
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
        port_params = {'6110/tcp': ('127.0.0.1', 6110)}

        seccomp_policy = ""
        with open("policy.json") as f:
            seccomp_policy = f.read()

        try:
            self.container = client.containers.run(
                "tamedpy",
                volumes=volume_params,
                ports=port_params,
                detach=True,
                # security_opt=['seccomp="policy.json"']
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
        port = 6110
        while(True):
            try:
                sock = socket.create_connection((server_address, port))
                message = "HELLO"
                print('sending "%s"' % message)
                sock.sendall(message)

                data = sock.recv(5)
                print('received "%s"' % data)

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
                print("connected! and ready")
                self._status = 1
                break
            finally:
                print('closing socket')
                sock.close()
        return

    def exec_code_socket(self):
        server_address = 'localhost'
        port = 6110
        while(True):
            try:
                sock = socket.create_connection((server_address, port))
                then = datetime.datetime.now()
                message = b'START'
                print('sending "%s"' % message)
                sock.sendall(message)

                data = sock.recv(4)
                print('received "%s"' % data)

                if data.strip() == b'':
                    print("ERROR: shouldn't be getting blank from server now")
                    time.sleep(0.1)
                    continue
                if data and data.strip() == b'DONE':
                    print "Got Exec result from sandbox after ", str(datetime.datetime.now() - then)
                    print "sandbox execution success"
                else:
                    raise Exception("bad message")
            except Exception as e:
                print(e)
                time.sleep(1)
            else:
                print("connected! and ready")
                self._status = 2
                break
            finally:
                print("closing the connection, trigger sandbox cleanup")
                sock.close()

        # TODO: offload to some background thread
        self.container.stop()
        self.on_container_finished()
        return

    def turndown(self):
        print("worker {} turndown intiated".format(self.id))
        self.container.stop()

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
        # response = exec_http_req(self.port, self.id, code)
        # assert response.ok
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


class Result(object):
    # TODO: add support for result.abort() to give up on the container and shutdown
    def __init__(self, path, exec_id):
        self.path = path
        self.exec_id = exec_id

    def __repr__(self):
        return "[" + str(self.exec_id) + "] " + self.stdout()

    def stdout(self):
        stdout_path = os.path.join(self.path, "stdout.txt")
        with open(stdout_path, "r") as f:
            self._stdout = f.read()
        return self._stdout

    def readFile(self, filename):
        # FIXME: return a generator instead
        filecontent = None
        filepath = os.path.join(self.path, filename)
        with open(filepath, "r") as f:
            filecontent = f.read()
        return filecontent

    def listdir(self):
        return os.listdir(self.path)


def exec_http_req(port, execid, code):
    url = "http://127.0.0.1:{}/run/{}".format(port, execid)
    print(url)
    response = requests.post(url, json={"code": code})
    print(response.status_code)
    print(response.text)
    return response


def test_basic_arith(driver):
    code = 'print(2**4)'
    result = driver.execute(code)
    print(result)

def test_single_file_io(driver):
    code = '''with open("input.txt", "r") as f:
    with open("uppercase.txt", "w") as of:
        of.write(f.read().upper())
    '''
    ifpath = '/tmp/input.txt'
    with open(ifpath, "w") as ifp:
        ifp.write("hello world\n")
    # think about execute returning from main thread or child thread
    result = driver.execute(code, [ifpath, ])
    # think about result.join() but execute() not being blocking necessarily
    print(result)
    print(result.readFile("uppercase.txt"))

def test_seccomp_blocking_mkdir(driver):
    code = '''import os
os.makedirs('karan')'''

    result = driver.execute(code)
    print(result)
    print result.listdir()

def test_seccomp_blocking_mount(driver):
    code = '''import subprocess, os
try:
    os.makedirs("/media/cdrom")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
subprocess.call("whoami", shell=True)
subprocess.call("mount /dev/cdrom /media/cdrom", shell=True)'''
    result = driver.execute(code)
    print(result)


if __name__ == "__main__":
    # subprocess.call("docker kill $(docker ps -q)", shell=True)
    #
    driver = Driver()
    driver.turnup()
    print(driver.worker_queue)
    test_basic_arith(driver)
    driver.turndown()
    #
    driver = Driver()
    driver.turnup()
    print(driver.worker_queue)
    test_single_file_io(driver)
    driver.turndown()

    # driver = Driver()
    # driver.turnup()
    # print(driver.worker_queue)
    # test_seccomp_blocking_mount(driver)
    # driver.turndown()

    # driver = Driver()
    # driver.turnup()
    # print(driver.worker_queue)
    # test_seccomp_blocking_mkdir(driver)
    # driver.turndown()
