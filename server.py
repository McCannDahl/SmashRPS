import socket
import time
import sys
from threading import Thread

serversocket = socket.socket()
host = 'localhost'
port = 54545
clientsockets = []
t1 = None
t2 = None

serversocket.bind(('', port))
print('listening ("conrol + c" to stop)')

serversocket.listen()
def get_client_data():
    while True:
        clientsocket,addr = serversocket.accept()
        print("got a connection from %s" % str(addr))
        clientsockets.append(clientsocket)

def update_game():
    while True:
        for c in clientsockets:
            try:
                c.send('update'.encode('ascii'))
            except:
                print('could not send update')
                clientsockets.remove(c)
        time.sleep(1)

if __name__ == '__main__':
    t1 = Thread(target=get_client_data)
    t1.daemon = True
    t2 = Thread(target=update_game)
    t2.daemon = True
    t1.start()
    t2.start()
    while True:
        time.sleep(10)