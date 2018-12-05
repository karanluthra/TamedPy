import os
import subprocess
import docker
import sys
import datetime

from worker import Worker
from portmanager import PortManagerPool, PortManagerRandom

# the daemon part - manages the pool of workers and assigns tasks
# provides interface to interact with execution
class Driver(object):
    def __init__(self, num_workers=1):
        self.num_workers = num_workers
        self.worker_queue = []
        self.turndown_in_progress = False
        self.port_manager = PortManagerRandom()
        # pass size = twice as many worker when implementing multi-threaded cleanup
        # self.port_manager = PortManagerPool(size = self.num_workers)

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
        port = self.port_manager.grab_free_port()
        new_worker = Worker(self, port)
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
        # TODO: brainstorm about other threads that might be doing worker cleanups
        self.turndown_in_progress = True
        for worker in self.worker_queue:
            worker.turndown()

    def grab_ready_worker(self):
        ready_worker = None
        while(ready_worker is None):
            for worker in self.worker_queue:
                if worker.status() == 1:
                    ready_worker = worker
                    break
        # if not ready_worker:
        #     assert False, "out of workers"
        return ready_worker

    def on_worker_exiting(self, worker):
        assert(worker.status() == 2)
        self.worker_queue.remove(worker)
        self.port_manager.release_port(worker.port)
        if not self.turndown_in_progress:
            self.turnup_one_new_worker()

def test_basic_arith(driver):
    code = 'print(2**4)'
    result = driver.execute(code)
    assert(result.stdout().strip() == "16")
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
#     code = '''import os
# os.makedirs('karan')'''
    code = '''import subprocess
subprocess.call("mkdir karan", shell=True)'''

    result = driver.execute(code)
    print(result)
    print(result.stderr())
    print result.listdir()


# test works correctly but not the most demonstrative
def test_seccomp_blocking_chown(driver):
    code = '''import subprocess
#print(str(subprocess.check_output("ls -l /tmp/py", shell=True)))
returncode = subprocess.call("chown sandboxuser /tmp/py", shell=True)
print(returncode)
#print(str(subprocess.check_output("ls -l /tmp/py", shell=True)))
'''
    result = driver.execute(code)
    print(result)
    print(result.stderr())
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
    print(result.stderr())


if __name__ == "__main__":
    # subprocess.call("docker kill $(docker ps -q)", shell=True)
    #
    start = datetime.datetime.now()
    driver = Driver(num_workers=1)
    driver.turnup()
    print(driver.worker_queue)
    ready = datetime.datetime.now()
    test_basic_arith(driver)
    done = datetime.datetime.now()
    driver.turndown()
    down = datetime.datetime.now()

    print("to ready: {}".format(ready - start))
    print("ready to done: {}".format(done - ready))
    print("done to exit: {}".format(down - done))

    #
    driver = Driver()
    driver.turnup()
    print(driver.worker_queue)
    test_single_file_io(driver)
    driver.turndown()

    driver = Driver()
    driver.turnup()
    print(driver.worker_queue)
    test_seccomp_blocking_mount(driver)
    driver.turndown()

    driver = Driver()
    driver.turnup()
    print(driver.worker_queue)
    test_seccomp_blocking_mkdir(driver)
    # test_seccomp_blocking_chown(driver)
    driver.turndown()
