import os


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

    def stderr(self):
        stderr_path = os.path.join(self.path, "stderr.txt")
        with open(stderr_path, "r") as f:
            self._stderr = f.read()
        return self._stderr

    def readFile(self, filename):
        # FIXME: return a generator instead
        filecontent = None
        filepath = os.path.join(self.path, filename)
        with open(filepath, "r") as f:
            filecontent = f.read()
        return filecontent

    def listdir(self):
        return os.listdir(self.path)
