
import socket
from threading import Thread
import json

class Socket:
    isconnected = False

    def __init__(self, got_data, disconnected, sock=None):
        self.got_data = got_data
        self.disconnected = disconnected
        if sock == None:
            self.sock = socket.socket()
            self.isconnected = False
        else:
            self.isconnected = True
            self.sock = sock
            self.start_listening()

    def restart(self):
        self.sock = socket.socket()
        self.isconnected = False

    def connect(self, host="localhost", port=54545):
        try:
            self.sock.connect((host, port))
            print('Established connection')
            self.isconnected = True
        except:
            print('server not active')
            self.isconnected = False
    
    def start_listening(self):
        Thread(target=self.get_data, args=[], kwargs=None, daemon=True).start()

    def send_data(self, data):
        Thread(target=self.send, args=[data], kwargs=None, daemon=True).start()

    def send(self, data):
        messagestr = '<<<'+json.dumps(data)+'>>>'
        self.sock.send(messagestr.encode('ascii'))

    def get_data(self):
        while self.isconnected:
            teststr = ''
            try:
                teststr = self.sock.recv(1024).decode("utf-8")
                new = teststr
                if '<<<' in new and '>>>' in new:
                    if new.endswith('>>>'): # last message is complete
                        new = new.split("<<<")[-1]
                    else: # last message is incomplete
                        new = new.split("<<<")[-2]
                    new = new.replace('>>>','')
                    # print(teststr)
                    try:
                        test = json.loads(new)
                        self.got_data(test)
                    except Exception as err:
                        print(teststr)
            except Exception as err:
                print(teststr)
                print(new)
                print('There was a problem getting server data. Closing socket. '+str(err))
                self.sock.close()
                self.isconnected = False
                self.disconnected()
