from driver import Driver

class SandboxedContext(object):
    def __init__(self, num_workers=1):
        self.driver = Driver(num_workers)

    def __enter__(self):
        self.driver.turnup()
        return self.driver

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        self.driver.turndown()
