from uuid import uuid4
import os
import errno
import subprocess
import requests
import time

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

    def execute(self, source_code):
        # find a ready worker, and execute the source code
        worker = self.grab_ready_worker()
        worker.execute(source_code)

    def turnup(self):
        # initiate workers to fill up the worker queue
        for i in range(self.num_workers):
            new_worker = Worker()

            # synch step, long, IO bound
            new_worker.turnup()
            assert new_worker.status() == 1
            self.worker_queue.append(new_worker)

    def grab_ready_worker(self):
        ready_worker = None
        for i in range(len(self.worker_queue)):
            if self.worker_queue[i].status() == 1:
                ready_worker = self.worker_queue[i]
                break
        if not ready_worker:
            assert False, "out of workers"
        return ready_worker


# one Worker instance per containerized execution
# owns details about execution artifacts and status
class Worker(object):
    def __init__(self):
        # super.__init__()
        self.id = uuid4()
        self.execd_path = None
        self._status = 0
        self.port = None

    def status(self):
        return self._status

    def turnup(self):
        # launch worker, check "ready", change status

        import docker

        client = docker.from_env()
        # print(client.containers.run("tamedpy"))
        # docker run -v /Users/luthrak/Projects/611/TamedPy/src/exec1:/tmp/py tamedpy
        host_path = "/Users/luthrak/Projects/611/TamedPy/src/exec1"
        self.execd_path = host_path

        # TODO: [DONE] Create new folder with exec id and mount *that* to this container.
        execd_path = os.path.join(WORKSPACE_DIR, str(self.id))
        try:
            os.makedirs(execd_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        self.execd_path = execd_path
        mnt_pnt = "/tmp/py"
        volume_params = {execd_path: {"bind": mnt_pnt, "mode": "rw"}}

        # TODO: grab a port number from free pool
        port = 3000
        self.port = port
        port_params = {"3000": port}
        try:
            container = client.containers.run(
                "tamedpy", volumes=volume_params, ports=port_params, detach=True
            )
            print(container)
            # FIXME: instead of sleeping, implement container sending a notif that it is ready
            time.sleep(1)
            self._status = 1
        except docker.errors.APIError as e:
            # FIXME: ask for specific error codes / eg when port is already allocated, take specific remedial action
            print(e)
            exit(-1)

    def get_exec_dir_path(self):
        return self.execd_path

    def execute(self, code):
        # FIXME: container attached to this worker must stop, cleaned up and replaced
        response = exec_http_req(self.port, self.id, code)
        assert response.ok


def exec_http_req(port, execid, code):
    url = "http://127.0.0.1:{}/run/{}".format(port, execid)
    print(url)
    response = requests.post(url, json={"code": code})
    print(response.status_code)
    print(response.text)
    return response


if __name__ == "__main__":
    subprocess.call("docker kill $(docker ps -q)", shell=True)

    driver = Driver()
    driver.turnup()
    print(driver.worker_queue)

    driver.execute("print(2**4)")
