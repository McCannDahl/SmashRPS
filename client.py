from threading import Thread
import socket

class MySocket:
    def __init__(self,host="localhost",port=54545):
        self.sock = socket.socket()
        self.sock.connect((host, port))

    def get_data(self):
        return self.sock.recv(1024).decode("utf-8") 

class Base():
    def __init__(self):
        print('Base constructor')
        self.sock = MySocket()
        Thread(target=self.get_data).start()

    def get_data(self):
        while True:
            self.text = self.sock.get_data()

    def launch(self):
        print('Base launch')


if __name__ == '__main__':
    Base().launch()