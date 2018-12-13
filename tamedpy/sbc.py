from driver import Driver

class SandboxedContext(object):
    def __init__(self, num_workers=1):
        self.driver = Driver(num_workers)
        self.driver.turnup()

    def __enter__(self):
        return self.driver

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        self.driver.turndown()

    def execute(self, *args, **kwargs):
        return self.driver.execute(*args, **kwargs)

    def close(self):
        self.driver.turndown()
