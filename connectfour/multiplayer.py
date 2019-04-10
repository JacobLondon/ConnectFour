from threading import Thread

from .window import Window
from .client import Client

class MultiFour:

    def __init__(self, interface, host_ip="localhost"):

        self.window = Window(interface)
        
        self.client = Client()
        def send():
            return self.window.tx
        self.client.send = send

        Thread(target=self.client.listen, args=(host_ip,)).start()
        self.window.run()


