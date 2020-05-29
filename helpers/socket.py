
import socket
from threading import Thread

class Socket:
    isconnected = False

    def __init__(self):
        self.sock = socket.socket()

    def connect(self, host="localhost", port=54545):
        try:
            self.sock.connect((host, port))
            print('Established connection')
            self.isconnected = True
        except:
            print('server not active')
            self.isconnected = False
    
    def start(self):
        self.t1 = Thread(target=self.get_data)
        self.t1.daemon = True
        self.t1.start()

    def get_data(self):
        while self.isconnected:
            try:
                print(self.sock.recv(1024).decode("utf-8"))
            except:
                self.sock.close()
                self.isconnected = False