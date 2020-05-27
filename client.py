from threading import Thread
import socket
import sys
import time

s = None

class MySocket:
    def __init__(self,host="localhost",port=54545):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        print('Established connection')
        self.t1 = Thread(target=self.get_data)
        self.t1.daemon = True
        self.t1.start()

    def get_data(self):
        while True:
            try:
                print(self.sock.recv(1024).decode("utf-8"))
            except:
                self.sock.close()

if __name__ == '__main__':
    s = MySocket()
    while True:
        time.sleep(10)