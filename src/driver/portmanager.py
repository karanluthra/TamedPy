import socket


class PortManagerRandom(object):
    '''
    from https://gist.github.com/gabrielfalcao/20e567e188f588b65ba2
    This has a race condition, since another process may grab that port after
    tcp.close(). This might be ok, if you simply catch the exception and try
    again, although it strikes me as possibly insecure to do so.
    '''
    def grab_free_port(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        addr, port = tcp.getsockname()
        tcp.close()
        return port

    def release_port(self, port):
        pass

class PortManagerPool(object):
    def __init__(self, size, starting_port=6110):
        self.port_pool = [None] * (size)
        self.init_port_pool(starting_port)

    def init_port_pool(self, starting_port):
        for i in range(len(self.port_pool)):
            self.port_pool[i] = starting_port + i
        print(self.port_pool)

    def grab_free_port(self):
        port = None
        for i in range(len(self.port_pool)):
            if not self.port_pool[i] is None:
                port = self.port_pool[i]
                self.port_pool[i] = None
                break
        assert(port != None), "free port unavailable"
        return port

    def release_port(self, port):
        for i in range(len(self.port_pool)):
            if self.port_pool[i] is None:
                self.port_pool[i] = port
